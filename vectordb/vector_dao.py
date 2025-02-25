import lancedb
import logging


class VectorDatabase:
    def __init__(self, uri: str):
        self.uri = uri
        self.db = self.connect(uri)

    def connect(self, uri: str):
        """
        连接到数据库并进行检查。
        """
        try:
            db = lancedb.connect(uri)
            return db
        except Exception as e:
            logging.error(f"连接到数据库失败: {e}")
            raise ValueError(f"无法连接到数据库：{uri}")

    def open_table(self, table_name: str):
        """
        打开指定名称的表，并检查是否存在该表。
        """
        if table_name not in self.db.table_names():
            logging.warning(f"表 {table_name} 不存在！")
            raise ValueError(f"表 {table_name} 不存在")
        return self.db.open_table(table_name)

    def create_table(self, table_name: str, data: list):
        """
        创建新表并进行数据格式检查。
        """
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            logging.error("数据格式无效，应为字典列表")
            raise ValueError("数据格式无效，应为字典列表")

        for item in data:
            if "vector" not in item or "item" not in item or "price" not in item:
                logging.error("数据项缺少必需字段")
                raise ValueError("数据项缺少必需字段")

        # 创建表
        return self.db.create_table(table_name, data)

    def search(self, table_name: str, query_vector: list, top_k: int = 2):
        """
        执行语义搜索，并检查向量的有效性。
        """
        if not isinstance(query_vector, list) or len(query_vector) == 0:
            logging.error("查询向量无效，必须为非空列表")
            raise ValueError("查询向量无效，必须为非空列表")

        table = self.open_table(table_name)
        return table.search(query_vector).limit(top_k).to_pandas()
