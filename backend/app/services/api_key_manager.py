import threading

from google import genai
from google.genai.errors import ClientError

from app.core.config import (
    GEMINI_API_KEYS,
    GEMINI_MODEL,
)


class APIKeyManager:

    def __init__(self):

        self.api_keys = GEMINI_API_KEYS

        if not self.api_keys:
            raise ValueError(
                "No Gemini API keys found. Please configure GEMINI_API_KEYS in your .env file."
            )

        self.current_index = 0

        self.exhausted_keys = set()

        self.lock = threading.Lock()

    def _get_client(self):

        with self.lock:
            api_key = self.api_keys[self.current_index]

        return genai.Client(
            api_key=api_key,
        )

    def _move_to_next_key(self):

        with self.lock:

            self.exhausted_keys.add(
                self.current_index
            )

            for index in range(len(self.api_keys)):

                if index not in self.exhausted_keys:

                    self.current_index = index

                    print(
                        f"\nSwitched to Gemini API Key #{index + 1}"
                    )

                    return

            raise RuntimeError(
                "All configured Gemini API keys have exhausted their daily quota."
            )

    def generate_content(
        self,
        prompt: str,
    ):

        while True:

            client = self._get_client()

            try:

                return client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                )

            except ClientError as error:

                if getattr(error, "status_code", None) == 429:

                    print(
                        f"\nGemini API Key #{self.current_index + 1} quota exhausted."
                    )

                    print(error)

                    self._move_to_next_key()

                    continue

                raise

    def get_client(self):

        return self._get_client()