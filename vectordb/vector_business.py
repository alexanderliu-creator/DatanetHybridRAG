import logging

from vectordb.vector_dao import VectorDatabase


class VectorSearchBusinessLogic:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db

    def perform_search(self, query_vector: list, top_k: int = 2):
        """
        执行搜索操作，并检查查询向量是否合法。
        """
        if not isinstance(query_vector, list) or len(query_vector) == 0:
            logging.error("查询向量无效，必须为非空列表")
            raise ValueError("查询向量无效，必须为非空列表")

        result = self.vector_db.search("my_table", query_vector, top_k)
        return result

    def create_sample_table(self):
        """
        创建样本表，检查数据格式。
        """
        data = [
            {"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
            {"vector": [5.9, 26.5], "item": "bar", "price": 20.0}
        ]
        self.vector_db.create_table("my_table", data)
