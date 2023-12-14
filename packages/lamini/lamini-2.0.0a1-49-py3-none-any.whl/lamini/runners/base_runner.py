from typing import List, Optional, Union
from lamini.api.lamini import Lamini


class BaseRunner:
    def __init__(self, model_name, system_prompt, prompt_template, api_key, config):
        self.config = config
        self.model_name = model_name
        self.lamini_api = Lamini(
            model_name=model_name, api_key=api_key, config=self.config
        )
        self.prompt_template = prompt_template
        self.system_prompt = system_prompt

    def call(
        self,
        prompt: Union[str, List[str]],
        system_prompt: Optional[str] = None,
        output_type: Optional[dict] = None,
        max_tokens: Optional[int] = None,
    ):
        input_objects = self.create_final_prompts(prompt, system_prompt)

        return self.lamini_api.generate(
            prompt=input_objects,
            model_name=self.model_name,
            max_tokens=max_tokens,
            output_type=output_type,
        )

    def create_final_prompts(self, prompt: Union[str, List[str]], system_prompt: str):
        if isinstance(prompt, str):
            return self.prompt_template.format(
                system=system_prompt or self.system_prompt, user=prompt
            )

        final_prompts = [
            self.prompt_template.format(
                system=system_prompt or self.system_prompt, user=p
            )
            for p in prompt
        ]

        return final_prompts
