import re

from const.vectordb_const import DEFAULT_EMBEDDINGS_API_URL, DEFAULT_LLM_API_URL, DEFAULT_MILVUS_SERVICE_URL
from util.milvus_vectordb_util import MilvusVectorDBUtil
from util.ollama_llm_util import OllamaLLMUtil
from langchain_text_splitters import CharacterTextSplitter


class VectorDBService:
    def __init__(self,
                 chunk_size=2048,
                 chunk_overlap=64,
                 ollama_embedding_endpoint=DEFAULT_EMBEDDINGS_API_URL,
                 ollama_llm_endpoint=DEFAULT_LLM_API_URL,
                 milvus_db_uri=DEFAULT_MILVUS_SERVICE_URL):
        """
        如果提供了 ollama_embedding_endpoint 与 ollama_llm_endpoint，则使用指定的端点，
        否则使用 OllamaLLMUtil 默认配置；同理 milvus_db_uri 为空时使用默认配置。
        """
        self.splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        if ollama_embedding_endpoint.strip() and ollama_llm_endpoint.strip():
            self.llm_util = OllamaLLMUtil(ollama_embedding_endpoint, ollama_llm_endpoint)
        else:
            self.llm_util = OllamaLLMUtil()
        if milvus_db_uri.strip():
            self.milvus_vector_db_util = MilvusVectorDBUtil(milvus_db_uri)
        else:
            self.milvus_vector_db_util = MilvusVectorDBUtil()

    def embed_text(self, text: str) -> list:
        """
        对输入文本进行切分，并对每个文本块调用 embedding 接口获取对应的向量表示，
        返回一个浮点数列表的列表。
        """
        chunks = self.splitter.split_text(text)
        embeddings = []
        for chunk in chunks:
            embedding = self.llm_util.get_embedding(chunk)
            embeddings.append(embedding)
        return embeddings

    def embed_text_with_model(self, text: str, model_name: str) -> list:
        """
        与 embed_text 类似，不过可以指定模型名称。
        """
        chunks = self.splitter.split_text(text)
        embeddings = []
        for chunk in chunks:
            embedding = self.llm_util.get_embedding(chunk, model_name)
            embeddings.append(embedding)
        return embeddings

    def setup_vector_db(self, collection_name: str, dimension: int):
        client = self.milvus_vector_db_util.get_native_client()

        if not client.has_collection(collection_name=collection_name):
            client.create_collection(
                collection_name=collection_name,
                dimension=dimension,
                vector_field_name="embedding",
                auto_id=True,
            )

        return client.get_collection_stats(collection_name=collection_name)

    def embed_and_save(self, collection_name: str, doid: str, dpml: str):
        """
        将文本 dpml 切分后获取 embedding，
        若 collection 不存在则创建，并将 doid、dpml 及 embedding 以行的方式插入 Milvus 中。
        注意：这里假设 MilvusVectorDBUtil 中实现了 insert_data 方法。
        """
        embeddings = self.embed_text(dpml)
        if not embeddings:
            raise Exception("Cannnot generate embeddings from input.")
        dimension = len(embeddings[0])

        collection_stats = self.setup_vector_db(collection_name, dimension)
        print("Collection stats:\n", collection_stats)

        rows = []
        for embedding in embeddings:
            row = {
                "doid": doid,
                "dpml": dpml,
                "embedding": embedding
            }
            rows.append(row)

        return self.milvus_vector_db_util.get_native_client().insert(collection_name, rows)

    def filter_relevant_search_response(self, relevant_search_response, collection_name: str, threshold: float,
                                        topK=1000):
        """
        从搜索结果中过滤出得分高于 threshold 的记录，
        并通过查询 ID 获取详细记录（这里假设搜索结果中每项为字典，包含 "score" 与 "id" 字段）。
        """
        ids = []
        for search_results in relevant_search_response:
            for result in search_results:
                if result.get("distance", 0) >= threshold:
                    ids.append(result.get("id"))

        if len(ids) == 0:
            return None

        query_resp = self.milvus_vector_db_util.query_by_ids(collection_name, ids, limit=topK)
        if query_resp and len(query_resp) > 0:
            return query_resp
        return None

    def search_query_with_topK_and_threshold(self, collection_name: str, query: str, threshold: float,
                                             topK: int = 1000, doid: str = None):
        """
        对用户输入 query 生成 embedding，
        并在 collection 中以 topK 的范围内搜索，将得分低于 threshold 的过滤掉。
        """
        query_embedding = self.llm_util.get_embedding(query)
        # 这里调用 MilvusVectorDBUtil 中按向量搜索的方法
        relevant_search_response = self.milvus_vector_db_util.search_collection_by_vector(
            collection_name=collection_name,
            query_vector=query_embedding,
            top_k=topK
        )
        relevance_response = self.filter_relevant_search_response(relevant_search_response, collection_name, threshold,
                                                                  topK)
        relevant_result = []

        if relevance_response:
            relevance_response = str(relevance_response)
            doid_values = re.findall(r"'doid':\s*'([^']+)'", str(relevance_response))
            dpml_values = re.findall(r"'dpml':\s*'([^']+)'", str(relevance_response))

            for doid_value, dpml_value in zip(doid_values, dpml_values):
                if doid and doid_value != doid:
                    continue

                relevant_result.append({
                    "doid": doid_value,
                    "dpml": dpml_values
                })

        return relevant_result
