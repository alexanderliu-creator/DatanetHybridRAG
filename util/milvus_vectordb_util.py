from pymilvus import MilvusClient
from pymilvus.grpc_gen.common_pb2 import Strong

from const.vectordb_const import DEFAULT_MILVUS_SERVICE_URL, DPML_COLLECTION


class MilvusVectorDBUtil:
    def __init__(self, uri: str = DEFAULT_MILVUS_SERVICE_URL):
        self.client = MilvusClient(uri)

    def create_if_not_exists(self, collection_name: str, dimension: int):
        if not self.client.has_collection(collection_name=collection_name):
            self.client.create_collection(collection_name=collection_name, dimension=dimension,
                                          consistency_level=Strong)

        return self.client.get_collection_stats(collection_name=collection_name)

    def drop_and_create(self, collection_name: str, dimension: int):
        if self.client.has_collection(collection_name=collection_name):
            self.client.drop_collection(collection_name=collection_name)
        return self.client.create_collection(collection_name=collection_name, dimension=dimension,
                                             consistency_level=Strong)

    def query_by_ids(self, collection_name: str, ids: list, limit=1000) -> any:
        return self.client.query(
            collection_name=collection_name,
            ids=ids,
            limit=limit
        )

    def query_by_id(self, collection_name: str, id_val: any) -> any:
        return self.query_by_ids(collection_name, [id_val])

    def search_collection_by_vector(self, collection_name: str, query_vector: list, top_k=1000) -> any:
        # self.client.load_collection(collection_name=collection_name)
        if not self.client.has_collection(collection_name=collection_name):
            raise "No DPML in the vector database right now, insert before query..."
        return self.client.search(
            collection_name=collection_name,
            data=[query_vector],
            anns_field="embedding",
            limit=top_k
        )

    def search_collection_by_vector_search_params(self, collection_name: str, query_vector: list, search_params: dict,
                                                  top_k=1000) -> any:
        self.client.load_collection(collection_name=collection_name)
        return self.client.search(
            collection_name=collection_name,
            data=[query_vector],
            anns_field="embedding",
            limit=top_k,
            params=search_params
        )

    def search_collection_by_vector_filer(self, collection_name: str, query_vector: list, filter_str: str,
                                          top_k=1000) -> any:
        self.client.get(collection_name=DPML_COLLECTION, output_fields=["*"], ids=[])
        return self.client.search(
            collection_name=collection_name,
            data=[query_vector],
            anns_field="embedding",
            limit=top_k,
            timeout=60000,
        )

    def get_native_client(self):
        return self.client

    def close(self) -> None:
        self.client.close()
