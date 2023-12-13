from llama.runners.llama_v2_runner import LlamaV2Runner

DEFAULT_SYSTEM_PROMPT = "Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."


class MistralRunner(LlamaV2Runner):
    """A class for running and training a Mistral model, using system and user prompts"""

    def __init__(
        self,
        model_name: str = "mistralai/Mistral-7B-Instruct-v0.1",
        system_prompt: str = None,
        config: dict = {},
    ):
        super().__init__(
            model_name=model_name,
            system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
            config=config,
        )
