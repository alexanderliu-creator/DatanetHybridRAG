import json

from flask import Flask, request, jsonify
import traceback

from const.vectordb_const import DPML_COLLECTION
from service.vectordb_service import VectorDBService

app = Flask(__name__)

vectordb_service = VectorDBService()


@app.route('/search', methods=['POST'])
def handle_search():
    try:
        req = request.get_json()
        # 从 JSON 中提取 header.parameters.attributes 数据
        attributes = req.get("header", {}).get("parameters", {}).get("attributes", {})
        doid = attributes.get("doid", None)
        query = attributes.get("query", "")
        threshold = attributes.get("threshold", 0)
        topK = attributes.get("topK", 0)

        # 根据是否存在 doid 调用不同的查询方法
        query_results = vectordb_service.search_query_with_topK_and_threshold(
            collection_name=DPML_COLLECTION,
            query=query,
            threshold=threshold,
            topK=topK,
            doid=doid
        )

        if query_results is None:
            response = {
                "responseCode": "UnKnownError",
                "attributes": {"queryResp": "No available query results"}
            }
        else:
            response = {
                "responseCode": "Success",
                "body": {}
            }

            response['body']["queryNum"] = len(query_results)
            response['body']["queryResp"] = json.dumps(query_results)
        return jsonify(response)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "responseCode": "UnKnownError",
            "error": traceback.format_exc()
        }), 500


@app.route('/publish', methods=['POST'])
def handle_publish():
    try:
        req = request.get_json()
        # 假设 DPML 数据在 body.data 中，为一个字符串
        dpml_content = req.get("body", {}).get("dpml", "")
        dpml_doid = req.get("body", {}).get("doid", "")
        print("Input DPML:\n" + dpml_content + "\nInput DOID:\n" + dpml_doid)

        if dpml_content and dpml_doid:
            insert_resp = vectordb_service.embed_and_save(
                collection_name=DPML_COLLECTION,
                doid=dpml_doid,
                dpml=dpml_content
            )
        else:
            raise Exception("Invalid input data.")

        response = {
            "responseCode": "Success",
            "body": {}
        }
        if insert_resp:
            response["body"]["insertCount"] = insert_resp.get("insert_count")
            response["body"]["insertedIDs"] = str(insert_resp.get("ids"))

        return jsonify(response)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "responseCode": "UnKnownError",
            "error": traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
