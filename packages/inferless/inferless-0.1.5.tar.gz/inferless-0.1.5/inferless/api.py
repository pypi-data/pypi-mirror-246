import os
from typing import Optional
import json
import threading


def call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None, callback=None):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data
    :param callback: Callback function to be called after the response is received
    :return: Response from the API call
    """
    try:
        import requests
        if workspace_api_key is None:
            workspace_api_key = os.environ.get("INFERLESS_API_KEY")
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {workspace_api_key}"}
        if data is None:
            data = {}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to call {url} with status code {response.status_code} and response {response.text}")
        if callback is not None:
            callback(None, response.json())
        return response.json()
    except Exception as e:
        if callback is not None:
            callback(e, None)
        else:
            raise e


def parallel_call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None, callback=None):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data
    :param callback: Callback function to be called after the response is received
    :return: Response from the API call
    """
    thread = threading.Thread(target=call, args=(url, workspace_api_key, data, callback))
    thread.start()
    return thread


URL = "https://m-18087e9d1fcb47be9cb184bcd0376f16-m.default.model-v1-dev.inferless.com/v2/models/gpt2_18087e9d1fcb47be9cb184bcd0376f16/versions/1/infer"
KEY = "fb16856b2258f8f99650b617ef6d0bcfdfb11c482e03faa469e0bf31bb08cc04edfb5822583d13bf8024337f1ae620c211cd11da092be1295bcea230afb2a6f2"
DATA = {
    "inputs": [{
        "data": ["Once upon a time"],
        "name": "prompt",
        "shape": [1],
        "datatype": "BYTES"
    }]
}


def callback_fun(e, response):
    # write response to file
    with open("response.json", "w") as f:
        f.write(json.dumps(response))

from datetime import datetime
t1 = datetime.now()
# response = call(url, key, data)
parallel_call(URL, KEY, DATA, callback_fun)
# print(response)
t2 = datetime.now()
print(f"time taken: {t2 - t1}")