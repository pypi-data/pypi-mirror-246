import time
import logging

from typing import List, Optional, Union
from lamini.api.inference_queue import InferenceQueue
from lamini.api.train import Train
from lamini.api.lamini_config import get_config

logger = logging.getLogger(__name__)


class Lamini:
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        config: dict = {},
    ):
        self.config = get_config(config)
        self.model_name = model_name
        self.inference_queue = InferenceQueue(api_key, config=config)
        self.trainer = Train(api_key, config=config)
        self.upload_file_path = None
        self.model_config = self.config.get("model_config", None)

    def generate(
        self,
        prompt: Union[str, List[str]],
        model_name: Optional[str] = None,
        output_type: Optional[dict] = None,
        max_tokens: Optional[int] = None,
        stop_tokens: Optional[List[str]] = None,
    ):
        req_data = self.make_llm_req_map(
            prompt=prompt,
            model_name=model_name or self.model_name,
            output_type=output_type,
            max_tokens=max_tokens,
            stop_tokens=stop_tokens,
        )
        result = self.inference_queue.submit(req_data)
        if isinstance(prompt, str) and len(result) == 1:
            return result[0]["output"]
        return result

    def upload_data(self, data_pairs, azure_dir_name="default"):
        self.trainer.upload_data(data_pairs, azure_dir_name)

    def upload_file(self, data_path, azure_dir_name="default"):
        self.trainer.upload_file(data_path, azure_dir_name)

    # just submit the job, no polling
    def train(
        self,
        data: Optional[List] = None,
        finetune_args: Optional[dict] = None,
        enable_peft: Optional[bool] = None,
        peft_args: Optional[dict] = None,
        is_public: Optional[bool] = None,
        use_cached_model: Optional[bool] = None,
    ):
        return self.trainer.train(
            data,
            self.model_name,
            finetune_args,
            enable_peft,
            peft_args,
            is_public,
            use_cached_model,
        )

    # continuously poll until the job is completed
    def train_and_wait(
        self,
        data: Optional[List] = None,
        finetune_args: Optional[dict] = None,
        enable_peft: Optional[bool] = None,
        peft_args: Optional[dict] = None,
        is_public: Optional[bool] = None,
        use_cached_model: Optional[bool] = None,
        **kwargs,
    ):
        job = self.train(
            data,
            finetune_args=finetune_args,
            enable_peft=enable_peft,
            peft_args=peft_args,
            is_public=is_public,
            use_cached_model=use_cached_model,
        )

        try:
            status = self.check_job_status(job["job_id"])
            if status["status"] == "FAILED":
                print(f"Job failed: {status}")
                return status

            while status["status"] not in ("COMPLETED", "FAILED", "CANCELLED"):
                if kwargs.get("verbose", False):
                    print(f"job not done. waiting... {status}")
                time.sleep(30)
                status = self.check_job_status(job["job_id"])
                if status["status"] == "FAILED":
                    print(f"Job failed: {status}")
                    return status
                elif status["status"] == "CANCELLED":
                    print(f"Job canceled: {status}")
                    return status
            print(
                f"Finetuning process completed, model name is: {status['model_name']}"
            )
        except KeyboardInterrupt as e:
            print("Cancelling job")
            return self.cancel_job(job["job_id"])

        return status

    def cancel_job(self, job_id=None):
        return self.trainer.cancel_job(job_id)

    def cancel_all_jobs(
        self,
    ):
        return self.trainer.cancel_all_jobs()

    def check_job_status(self, job_id=None):
        return self.trainer.check_job_status(job_id)

    def get_jobs(self):
        return self.trainer.get_jobs()

    def evaluate(self, job_id=None):
        return self.trainer.evaluate(job_id)

    def make_llm_req_map(
        self,
        model_name,
        prompt,
        output_type,
        stop_tokens,
        max_tokens,
    ):
        req_data = {}
        req_data["model_name"] = model_name
        req_data["prompt"] = prompt
        req_data["out_type"] = output_type
        if stop_tokens is not None:
            req_data["stop_tokens"] = stop_tokens
        if max_tokens is not None:
            req_data["max_tokens"] = max_tokens
        if self.model_config:
            req_data["model_config"] = self.model_config.as_dict()
        return req_data
