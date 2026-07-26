import json
import time
from json import JSONDecodeError
from typing import Type, TypeVar

from groq import Groq
from pydantic import BaseModel, ValidationError

from backend.config.settings import settings, logger

T = TypeVar("T", bound=BaseModel)

_client = None


def get_client() -> Groq:
    global _client

    if _client is None:

        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not configured."
            )

        _client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    return _client


def generate_structured_output(
    prompt: str,
    system_prompt: str,
    response_model: Type[T],
    max_retries: int = 3,
) -> T:

    client = get_client()

    for attempt in range(max_retries):

        try:

            start = time.time()

            completion = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={
                    "type": "json_object"
                },
                temperature=0.2,
            )

            elapsed = round(
                time.time() - start,
                2
            )

            logger.info(
                f"LLM completed in {elapsed}s"
            )

            if completion.usage:

                logger.info(
                    f"Prompt Tokens : {completion.usage.prompt_tokens}"
                )

                logger.info(
                    f"Completion Tokens : {completion.usage.completion_tokens}"
                )

                logger.info(
                    f"Total Tokens : {completion.usage.total_tokens}"
                )

            response = completion.choices[0].message.content

            if not response:
                raise ValueError(
                    "LLM returned empty response."
                )

            parsed = json.loads(response)

            return response_model.model_validate(
                parsed
            )

        except (
            JSONDecodeError,
            ValidationError,
            ValueError,
        ) as e:

            logger.error(str(e))

            if attempt == max_retries - 1:
                raise

            time.sleep(2 ** attempt)

        except Exception as e:

            logger.exception(
                "Unexpected LLM error."
            )

            if attempt == max_retries - 1:
                raise

            time.sleep(2 ** attempt)