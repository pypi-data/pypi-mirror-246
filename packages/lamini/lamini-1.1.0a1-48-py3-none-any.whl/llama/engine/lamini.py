from typing import List, Optional, Union
import time
import json
from llama.program.util.run_ai import (
    get_configured_url,
    get_ui_url,
    get_model_config,
    make_web_request,
)
from llama.program.util.config import edit_config
from concurrent.futures import ThreadPoolExecutor
import logging
import lamini

logger = logging.getLogger(__name__)


class Lamini:
    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        config: dict = {},
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.config = edit_config(config)
        url = get_configured_url()
        self.model_config = get_model_config()
        self.api_prefix = url + "/v2/lamini/"
        self.job_id = None
        self.upload_file_path = None

    def __call__(
        self,
        prompt: Union[str, List[str]],
        output_type=None,
        stop_tokens: Union[str, List[str]] = None,
        model_name=None,
        max_tokens=None,
        streaming=None,
    ):
        if isinstance(stop_tokens, str):
            stop_tokens = [stop_tokens]
        if isinstance(input, List):
            if len(input) > 2000:
                raise Exception(
                    status_code=429,
                    detail=f"Too many requests. Please reduce the batch size to 2000 or less.",
                )

            results = []
            batch_size = lamini.batch_size

            def work(chunk):
                req_data = self.make_llm_req_map(
                    model_name or self.model_name,
                    chunk,
                    output_type,
                    stop_tokens,
                    max_tokens,
                    streaming,
                )
                url = self.api_prefix + "completions"
                return make_web_request("post", url, self.api_key, req_data)

            with ThreadPoolExecutor(max_workers=lamini.max_workers) as executor:
                chunks = [
                    input[i : i + batch_size] for i in range(0, len(input), batch_size)
                ]
                results = executor.map(work, chunks)
                results = [item for sublist in results for item in sublist]

            return results

        req_data = self.make_llm_req_map(
            model_name or self.model_name,
            prompt,
            output_type,
            stop_tokens,
            max_tokens,
            streaming,
        )
        url = self.api_prefix + "completions"
        return make_web_request("post", url, self.api_key, req_data)

    def upload_data(self, data_pairs, azure_dir_name="default"):
        url = self.api_prefix + "upload_data"
        self.upload_file_path = make_web_request(
            "post",
            url,
            self.api_key,
            {"azure_dir_name": azure_dir_name, "data": data_pairs},
        )

    def upload_file(self, data_path, azure_dir_name="default"):
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        f.close()
        self.upload_file_path = self.upload_data(data, azure_dir_name)

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
        req_data = {"model_name": self.model_name}
        if data is not None:
            req_data["data"] = data
        if self.upload_file_path is not None:
            req_data["upload_file_path"] = self.upload_file_path
        if finetune_args is not None:
            req_data["finetune_args"] = finetune_args
        if enable_peft is not None:
            req_data["enable_peft"] = enable_peft
        if peft_args is not None:
            req_data["peft_args"] = peft_args
        if is_public is not None:
            req_data["is_public"] = is_public
        if use_cached_model is not None:
            req_data["use_cached_model"] = use_cached_model
        if self.model_config:
            req_data["model_config"] = self.model_config.as_dict()
        url = self.api_prefix + "train"

        job = make_web_request("post", url, self.api_key, req_data)
        self.job_id = job["job_id"]
        ui_url = get_ui_url()
        print(
            f"Training job submitted! Check status of job {self.job_id} here: {ui_url}/train/{self.job_id}"
        )

        return job

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

    # https://lamini-ai.github.io/API/train_job_cancel/
    def cancel_job(self, job_id=None):
        if job_id is None:
            job_id = self.job_id
        url = self.api_prefix + "train/jobs/" + str(job_id) + "/cancel"

        return make_web_request("post", url, self.api_key, {})

    def cancel_all_jobs(
        self,
    ):
        url = self.api_prefix + "train/jobs/cancel"

        return make_web_request("post", url, self.api_key, {})

    # https://lamini-ai.github.io/API/train_job_status/
    def check_job_status(self, job_id=None):
        if job_id is None:
            job_id = self.job_id
        url = self.api_prefix + "train/jobs/" + str(job_id)

        return make_web_request("get", url, self.api_key, {})

    def get_jobs(self):
        url = self.api_prefix + "train/jobs"

        return make_web_request("get", url, self.api_key, {})

    # https://lamini-ai.github.io/API/eval_results/#request
    def evaluate(self, job_id=None):
        if job_id is None:
            job_id = self.job_id
        url = self.api_prefix + "train/jobs/" + str(job_id) + "/eval"

        return make_web_request("get", url, self.api_key, {})

    # check if two maps have the same keys and value types
    def same_type(self, t1, t2):
        if t1.keys() != t2.keys():
            return False

        for k in t1.keys():
            if type(t1[k]) != type(t2[k]):
                return False

        return True

    def is_correct_type(self, t):
        return isinstance(t, dict)

    def make_llm_req_map(
        self,
        model_name,
        prompt,
        output_type,
        stop_tokens,
        max_tokens,
        streaming,
    ):
        req_data = {}
        req_data["model_name"] = model_name
        req_data["prompt"] = prompt
        req_data["out_type"] = output_type
        if streaming is not None:
            req_data["streaming"] = streaming
        if stop_tokens is not None:
            req_data["stop_tokens"] = stop_tokens
        if max_tokens is not None:
            req_data["max_tokens"] = max_tokens
        if self.model_config:
            req_data["model_config"] = self.model_config.as_dict()
        return req_data
