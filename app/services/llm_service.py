
from google import genai
from google.genai import types

from app.config import Settings


class LLMService:
    def __init__(self, settings: Settings):
        self.settings = settings

        api_key = settings.gemini_api_key.get_secret_value()
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=30000,
                retry_options=types.HttpRetryOptions(
                    attempts=1,
                ),
            ),
        )

    def generate(self, prompt: str) -> dict:
        models = [
            self.settings.gemini_primary_model,
            self.settings.gemini_fallback_model,
        ]

        errors = []

        for model in models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                usage = response.usage_metadata

                return {
                    "model": model,
                    "answer": response.text or "",
                    "usage": {
                        "prompt_tokens": (
                            usage.prompt_token_count if usage else 0
                        ),
                        "response_tokens": (
                            usage.candidates_token_count if usage else 0
                        ),
                        "thoughts_tokens": (
                            usage.thoughts_token_count if usage else 0
                        ),
                        "total_tokens": (
                            usage.total_token_count if usage else 0
                        ),
                    },
                }

            except Exception as exc:
                print(
                    f"Gemini model failed: {model} | "
                    f"{type(exc).__name__}: {exc}",
                    flush=True,
                )
                errors.append(f"{model}: {exc}")

        raise RuntimeError(
            "All configured Gemini models failed: " + " | ".join(errors)
        )
