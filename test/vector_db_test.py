import logging

from vectordb.vector_business import VectorSearchBusinessLogic
from vectordb.vector_dao import VectorDatabase

if __name__ == '__main__':
    # 示例执行
    uri = "vectordb/data"
    try:
        vector_db = VectorDatabase(uri)
        business_logic = VectorSearchBusinessLogic(vector_db)

        # 创建样本表
        try:
            business_logic.create_sample_table()
        except Exception as e:
            print(e)

        # 执行搜索
        query_vector = [100, 100]
        search_results = business_logic.perform_search(query_vector)
        print(search_results)

    except ValueError as e:
        logging.error(f"发生错误：{e}")
