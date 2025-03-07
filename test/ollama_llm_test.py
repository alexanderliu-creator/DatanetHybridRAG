from util.ollama_llm_util import OllamaLLMUtil


def test_get_embedding():
    llm_util = OllamaLLMUtil()
    prompt = "你好，测试一下接口。"
    embedding = llm_util.get_embedding(prompt)
    print("Embedding:", embedding)


if __name__ == '__main__':
    test_get_embedding()
