import logging

from vectordb.vectordb_dao import VectorDatabase

### HTML -> Embedding
# DPML Summarization -> DPML DOI
if __name__ == '__main__':
    # 示例执行
    uri = "vectordb/data"
    try:
        vector_db = VectorDatabase(uri)
        table_name = "test_table"

        # 创建样本表
        try:
            data = [
                {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
                {"vector": [5.9, 26.5], "item": "bar", "price": 20.0}
            ]
            vector_db.create_table(table_name, data)
        except Exception as e:
            print(e)

        # 执行搜索
        query_vector = [100, 100]
        search_results = vector_db.search(table_name, query_vector)
        print(search_results)

    except ValueError as e:
        logging.error(f"发生错误：{e}")
