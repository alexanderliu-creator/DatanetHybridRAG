import logging

from vectordb.embedding_dao import EmbeddingProcessor
from vectordb.vectordb_dao import VectorDatabase

if __name__ == '__main__':
    # 示例执行
    uri = "vectordb/data"  # 修改为你自己的向量数据库路径
    table_name = "bert_db_plus"

    # 初始化EmbeddingProcessor并生成嵌入
    try:
        embedding_processor = EmbeddingProcessor(model_name='bert-base-uncased')
        # 示例文本
        sentences = [
            "Hello, this is a test sentence.",
            "Embedding with BERT is cool!",
            "Datanet is a really newbee system"
        ]

        # 获取文本的嵌入并构建数据
        embeddings = [embedding_processor.encode_text(sentence) for sentence in sentences]
        data = [
            {"vector": embedding, "content": sentence}  # 为每个项附加向量和价格
            for idx, (embedding, sentence) in enumerate(zip(embeddings, sentences))
        ]

        # 连接到数据库并创建表
        vector_db = VectorDatabase(uri)
        try:
            vector_db.create_table(table_name, data)
            logging.info(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

        # 执行搜索
        query_vector = embedding_processor.encode_text("Datanet")
        print(query_vector)
        search_results = vector_db.search(table_name, query_vector)
        print("Search results:", search_results)

    except ValueError as e:
        logging.error(f"发生错误：{e}")
