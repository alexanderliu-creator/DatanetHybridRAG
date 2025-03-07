from util.milvus_vectordb_util import MilvusVectorDBUtil
from util.ollama_llm_util import OllamaLLMUtil


def create_and_show_all():
    """
    模拟 CreateAndShowAll：
    对一组文本（dpmlList）计算 embedding，创建集合 "dpml_embedding_example"，插入记录，
    然后查询集合中所有记录并打印。
    """
    dpml_list = [
        "The sky is blue because of Rayleigh scattering",
        "Water is wet and essential for life",
        "The quick brown fox jumps over the lazy dog",
        "Artificial intelligence is transforming the technology landscape",
        "Quantum computing could revolutionize problem-solving methods",
        "Climate change poses significant risks to biodiversity",
        "Renewable energy sources are crucial for sustainable development",
        "Blockchain technology ensures secure and transparent transactions",
        "The principles of physics govern the behavior of the universe",
        "Advanced algorithms drive innovations in data science"
    ]
    llm_util = OllamaLLMUtil()
    milvus_util = MilvusVectorDBUtil()

    # 根据第一条文本的 embedding 长度确定集合维度
    embedding_first = llm_util.get_embedding(dpml_list[0])
    dimension = len(embedding_first)

    collection_name = "dpml_embedding_example"
    milvus_util.drop_and_create(collection_name, dimension)
    print(f"Collection '{collection_name}' created with dimension {dimension}")

    rows = []
    id_counter = 1
    for dpml in dpml_list:
        vector = llm_util.get_embedding(dpml)
        row = {
            "id": id_counter,
            "vector": vector,
            "dpml": dpml
        }
        rows.append(row)
        id_counter += 1

    insert_result = milvus_util.get_native_client().insert(collection_name, rows)
    print(f"{insert_result.get('insert_cnt', 'unknown')} rows inserted")

    # 查询集合行数
    client = milvus_util.get_native_client()
    query_result = client.query(collection_name=collection_name, filter="", output_fields=["count(*)"])
    if query_result:
        count_val = query_result[0].get("count(*)")
        print(f"{count_val} rows persisted")

    # 根据 ID 检索所有记录
    ids = list(range(1, id_counter))
    get_result = client.get(collection_name=collection_name, ids=ids, output_fields=["*"])
    print("\nRetrieved embedding rows:")
    # for res in get_result:
    #     print(res)

    milvus_util.close()


def create_and_embedding_search():
    """
    模拟 CreateAndEmbeddingSearch2：
    先调用 create_and_show_all() 构造数据，再对集合 "dpml_embedding_example" 执行向量搜索（查询文本 "AI"）。
    """
    create_and_show_all()  # 先创建数据
    llm_util = OllamaLLMUtil()
    milvus_util = MilvusVectorDBUtil()
    client = milvus_util.get_native_client()

    query_embedding = llm_util.get_embedding("AI")
    search_result = client.search(
        collection_name="dpml_embedding_example",
        data=[query_embedding],
        anns_field="vector",
        limit=5
    )
    print("Search results for query 'AI':")
    for res in search_result:
        print(res)

    client.close()


def query_by_ids():
    """
    模拟 queryByIds：先调用 create_and_show_all() 构造数据，
    然后根据 ID 列表 [1, 2, 3] 查询并打印结果。
    """
    create_and_show_all()
    milvus_util = MilvusVectorDBUtil()
    result = milvus_util.query_by_ids("dpml_embedding_example", [1, 2, 3])
    print("Query by IDs [1, 2, 3] result:")
    print(result)
    milvus_util.close()


def drop_collection():
    llm_util = OllamaLLMUtil()
    milvus_util = MilvusVectorDBUtil()

    milvus_util.get_native_client().drop_collection("DPMLCollection")


if __name__ == "__main__":
    # print("\n=== Create and Embedding Search ===")
    # create_and_embedding_search()
    # print("\n=== Query by IDs ===")
    # query_by_ids()
    print("drop_collection")
    drop_collection()
