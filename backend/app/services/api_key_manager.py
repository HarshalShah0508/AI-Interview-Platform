import contextvars
import threading
import time

from google import genai
from google.genai.errors import APIError

from app.core.config import (
    GEMINI_API_KEYS,
    GEMINI_MODEL,
)


# ============================================================
# Per-analysis Gemini call telemetry
#
# Lets the resume-analysis worker tag every Gemini call with
# the analysis it belongs to and count calls per analysis,
# WITHOUT threading an analysis_id parameter through every
# service function. Never logs prompt content or API keys.
# ============================================================

_analysis_id_var: contextvars.ContextVar = contextvars.ContextVar(
    "gemini_analysis_id",
    default=None,
)

_call_count_var: contextvars.ContextVar = contextvars.ContextVar(
    "gemini_call_count",
    default=0,
)


def set_gemini_context(analysis_id) -> None:
    """
    Associate all subsequent Gemini calls made on this thread
    with the given analysis id, and reset the call counter.
    """

    _analysis_id_var.set(analysis_id)
    _call_count_var.set(0)


def clear_gemini_context() -> None:

    _analysis_id_var.set(None)
    _call_count_var.set(0)


def get_gemini_call_count() -> int:

    return _call_count_var.get()


class APIKeyManager:
    """
    Centralized Gemini API key manager.

    Responsibilities:
    - Maintain multiple Gemini API keys.
    - Rotate to the next key when Gemini returns 429.
    - Retry with bounded exponential backoff when Gemini
      returns 503 (model temporarily unavailable/overloaded).
    - Support both simple prompts and structured
      google-genai requests.
    - Share the same rotation state across the application.
    - Log per-analysis Gemini call telemetry (call number,
      purpose, model, success/failure) without ever logging
      API keys or raw prompt/response content.

    The manager does NOT make decisions about prompts,
    schemas, or application logic. It only manages
    Gemini API access.
    """

    # Bounded retry behavior for transient 503 errors.
    # This is intentionally small — a persistent outage
    # should surface as a clear failure, not retry forever.
    MAX_UNAVAILABLE_RETRIES = 3
    BASE_BACKOFF_SECONDS = 1.0
    MAX_BACKOFF_SECONDS = 8.0

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
    # Telemetry
    # ========================================================

    def _log_call_start(
        self,
        purpose: str,
        model: str,
    ) -> tuple[int, object]:

        analysis_id = _analysis_id_var.get()

        call_number = (
            _call_count_var.get()
            + 1
        )

        _call_count_var.set(
            call_number
        )

        label = (
            f"[ResumeAnalysis {analysis_id}]"
            if analysis_id is not None
            else "[Gemini]"
        )

        print(
            f"{label} Gemini Call {call_number} "
            f"-> {purpose} (model={model})"
        )

        return call_number, analysis_id

    @staticmethod
    def _log_call_result(
        analysis_id,
        call_number: int,
        purpose: str,
        outcome: str,
    ) -> None:

        label = (
            f"[ResumeAnalysis {analysis_id}]"
            if analysis_id is not None
            else "[Gemini]"
        )

        print(
            f"{label} Gemini Call {call_number} "
            f"({purpose}) -> {outcome}"
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
        purpose="unspecified",
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

        `purpose` is a short human-readable label used only
        for telemetry (e.g. "jd_structuring",
        "batched_recommendations") — it never affects the
        request sent to Gemini.
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

        call_number, analysis_id = (
            self._log_call_start(
                purpose,
                model,
            )
        )

        unavailable_attempts = 0

        while True:

            client = self._get_client()

            try:

                if config is None:

                    response = (
                        client.models.generate_content(
                            model=model,
                            contents=contents,
                        )
                    )

                else:

                    response = (
                        client.models.generate_content(
                            model=model,
                            contents=contents,
                            config=config,
                        )
                    )

                self._log_call_result(
                    analysis_id,
                    call_number,
                    purpose,
                    "success",
                )

                return response

            except APIError as error:

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

                    try:
                        self._move_to_next_key()

                    except RuntimeError:

                        self._log_call_result(
                            analysis_id,
                            call_number,
                            purpose,
                            "failed (all API keys rate-limited)",
                        )

                        raise

                    continue

                if self._is_unavailable_error(
                    error
                ):

                    unavailable_attempts += 1

                    if (
                        unavailable_attempts
                        > self.MAX_UNAVAILABLE_RETRIES
                    ):

                        self._log_call_result(
                            analysis_id,
                            call_number,
                            purpose,
                            "failed (503 retries exhausted)",
                        )

                        raise

                    delay = min(
                        self.BASE_BACKOFF_SECONDS
                        * (2 ** (unavailable_attempts - 1)),
                        self.MAX_BACKOFF_SECONDS,
                    )

                    print(
                        "\n[Gemini API] "
                        "Model temporarily unavailable (503). "
                        f"Retrying in {delay:.1f}s "
                        f"(attempt {unavailable_attempts}/"
                        f"{self.MAX_UNAVAILABLE_RETRIES})."
                    )

                    time.sleep(delay)

                    continue

                self._log_call_result(
                    analysis_id,
                    call_number,
                    purpose,
                    f"failed ({type(error).__name__})",
                )

                raise

            except Exception as error:

                self._log_call_result(
                    analysis_id,
                    call_number,
                    purpose,
                    f"failed ({type(error).__name__})",
                )

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
    # Availability detection (503 / model overloaded)
    # ========================================================

    @staticmethod
    def _is_unavailable_error(
        error,
    ):
        """
        Detect transient "model unavailable / overloaded"
        errors so they can be retried with bounded backoff,
        separately from rate-limit (429) handling.
        """

        status_code = getattr(
            error,
            "status_code",
            None,
        )

        if status_code == 503:
            return True

        code = getattr(
            error,
            "code",
            None,
        )

        if code == 503:
            return True

        message = str(
            error
        ).lower()

        return any(
            phrase in message
            for phrase in (
                "503",
                "unavailable",
                "overloaded",
                "high demand",
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
