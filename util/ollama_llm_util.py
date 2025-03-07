# llm_util.py

import requests
from const.vectordb_const import DEFAULT_EMBEDDINGS_API_URL, DEFAULT_LLM_API_URL, DEFAULT_EMBEDDING_MODEL, \
    DEFAULT_LLM_MODEL


class OllamaLLMUtil:
    def __init__(self, ollama_embedding_endpoint=DEFAULT_EMBEDDINGS_API_URL,
                 ollama_llm_endpoint=DEFAULT_LLM_API_URL):
        self.ollama_embedding_endpoint = ollama_embedding_endpoint
        self.ollama_llm_endpoint = ollama_llm_endpoint

    def get_embedding(self, prompt, model_name=DEFAULT_EMBEDDING_MODEL):
        """
        获取 prompt 的向量表示，返回一个浮点数列表
        """
        payload = {
            "model": model_name,
            "prompt": prompt
        }
        response = requests.post(
            self.ollama_embedding_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get embedding. Status code: {response.status_code}")

        json_response = response.json()
        embedding_list = json_response.get("embedding", [])
        # 转换为浮点数列表
        return [float(item) for item in embedding_list]

    def get_llm_response(self, prompt, model_name=DEFAULT_LLM_MODEL):
        """
        获取 LLM 对 prompt 的回复
        """
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
        response = requests.post(
            self.ollama_llm_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get LLM response. Status code: {response.status_code}")

        json_response = response.json()
        message = json_response.get("message", {})
        return message.get("content", "")
