import threading

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from app.core.config import GEMINI_API_KEYS


class APIKeyManager:

    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self):

        self.api_keys = GEMINI_API_KEYS

        if not self.api_keys:
            raise ValueError(
                "No Gemini API keys found. Please configure GEMINI_API_KEYS in your .env file."
            )

        self.current_index = 0

        self.exhausted_keys = set()

        self.lock = threading.Lock()

    def _get_model(self):

        with self.lock:
            api_key = self.api_keys[self.current_index]

        genai.configure(
            api_key=api_key
        )

        return genai.GenerativeModel(
            self.MODEL_NAME
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
        prompt: str
    ):

        while True:

            model = self._get_model()

            try:

                return model.generate_content(
                    prompt
                )

            except ResourceExhausted as e:

                print(
                    f"\nGemini API Key #{self.current_index + 1} quota exhausted."
                )

                print(e)

                self._move_to_next_key()

    def get_model(self):

        return self._get_model()