import os
from pathlib import Path
from typing import Type

from backend.utils.llm import generate_structured_output
from backend.config.settings import logger


PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    """
    Load a system prompt from the prompts directory.
    """

    filepath = PROMPTS_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {filepath}"
        )

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()

    except Exception as e:
        logger.exception(
            f"Failed to load prompt '{filename}'"
        )
        raise e


class BaseAgent:
    """
    Base class for all LLM agents.

    Responsibilities:
    - Load system prompt
    - Execute LLM request
    - Return structured response
    """

    def __init__(
        self,
        prompt_filename: str,
        name: str
    ):

        self.name = name
        self.system_prompt = load_prompt(prompt_filename)

        logger.info(
            f"{self.name} initialized."
        )

    def execute(
        self,
        prompt: str,
        response_model: Type
    ):
        """
        Execute the LLM with the agent's system prompt.
        """

        logger.info(
            f"{self.name} execution started."
        )

        try:

            result = generate_structured_output(
                prompt=prompt,
                system_prompt=self.system_prompt,
                response_model=response_model
            )

            logger.info(
                f"{self.name} execution completed."
            )

            return result

        except Exception as e:

            logger.exception(
                f"{self.name} execution failed."
            )

            raise e