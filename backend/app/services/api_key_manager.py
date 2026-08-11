import threading

from google import genai
from google.genai.errors import ClientError

from app.core.config import (
    GEMINI_API_KEYS,
    GEMINI_MODEL,
)


class APIKeyManager:
    """
    Centralized Gemini API key manager.

    Responsibilities:
    - Maintain multiple Gemini API keys.
    - Rotate to the next key when Gemini returns 429.
    - Support both simple prompts and structured
      google-genai requests.
    - Share the same rotation state across the application.

    The manager does NOT make decisions about prompts,
    schemas, or application logic. It only manages
    Gemini API access.
    """

    def __init__(self):

        self.api_keys = list(
            dict.fromkeys(
                GEMINI_API_KEYS
            )
        )

        if not self.api_keys:
            raise ValueError(
                "No Gemini API keys found. "
                "Please configure GEMINI_API_KEYS "
                "in your .env file."
            )

        self.current_index = 0

        self.exhausted_keys = set()

        self.lock = threading.Lock()

    # ========================================================
    # Client handling
    # ========================================================

    def _get_client(self):
        """
        Return a Gemini client for the currently
        active API key.
        """

        with self.lock:

            api_key = self.api_keys[
                self.current_index
            ]

        return genai.Client(
            api_key=api_key,
        )

    # ========================================================
    # Key rotation
    # ========================================================

    def _move_to_next_key(self):
        """
        Mark the current key as exhausted and
        move to the next available key.
        """

        with self.lock:

            exhausted_index = (
                self.current_index
            )

            self.exhausted_keys.add(
                exhausted_index
            )

            for index in range(
                len(self.api_keys)
            ):

                if index in self.exhausted_keys:
                    continue

                self.current_index = index

                print(
                    "\n[Gemini API] "
                    f"Switched to API Key #{index + 1}"
                )

                return

        raise RuntimeError(
            "All configured Gemini API keys "
            "have exhausted their available quota."
        )

    # ========================================================
    # Gemini generation
    # ========================================================

    def generate_content(
        self,
        prompt=None,
        *,
        contents=None,
        config=None,
        model=None,
    ):
        """
        Generate Gemini content.

        Backwards compatible with the existing usage:

            manager.generate_content(
                prompt="..."
            )

        Also supports the newer google-genai API:

            manager.generate_content(
                contents=prompt,
                config=...
            )

        This is important because resume analysis uses
        structured JSON responses.
        """

        if contents is None:

            if prompt is None:
                raise ValueError(
                    "Either 'prompt' or 'contents' "
                    "must be provided."
                )

            contents = prompt

        model = (
            model
            or GEMINI_MODEL
        )

        while True:

            client = self._get_client()

            try:

                if config is None:

                    return (
                        client.models.generate_content(
                            model=model,
                            contents=contents,
                        )
                    )

                return (
                    client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config,
                    )
                )

            except ClientError as error:

                if self._is_rate_limit_error(
                    error
                ):

                    current_key_number = (
                        self.current_index + 1
                    )

                    print(
                        "\n[Gemini API] "
                        f"API Key #{current_key_number} "
                        "received a 429 response."
                    )

                    self._move_to_next_key()

                    continue

                raise

    # ========================================================
    # Rate-limit detection
    # ========================================================

    @staticmethod
    def _is_rate_limit_error(
        error,
    ):
        """
        Detect Gemini rate-limit/quota errors.

        The google-genai SDK can expose the status
        differently depending on version, so we
        check both the explicit status and the
        error message.
        """

        status_code = getattr(
            error,
            "status_code",
            None,
        )

        if status_code == 429:
            return True

        code = getattr(
            error,
            "code",
            None,
        )

        if code == 429:
            return True

        message = str(
            error
        ).lower()

        return any(
            phrase in message
            for phrase in (
                "429",
                "resource exhausted",
                "rate limit",
                "quota exceeded",
                "quota",
                "too many requests",
            )
        )

    # ========================================================
    # Client access
    # ========================================================

    def get_client(self):
        """
        Return a Gemini client using the currently
        active API key.

        Use generate_content() whenever possible so
        automatic key rotation is preserved.
        """

        return self._get_client()


# ============================================================
# Shared application-level manager
# ============================================================

api_key_manager = APIKeyManager()