import requests
import json
from mysql import connector
from datetime import datetime, timedelta

from .environment import ACCESS_TOKEN,CONSUMER_KEY

request_headers = {"Content-Type": "application/json; charset=UTF-8", "X-Accept": "application/json"}
base_path = "https://getpocket.com/v3/"


def get_items():
    get_index_path = base_path + "get"
    get_index_request_data = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(
        get_index_path,
        data=json.dumps(get_index_request_data),
        headers=request_headers
    )
    list_in_response = response.json()["list"]

    # 注:item_id から何から全て文字列
    items = [
        {
            "item_id": item["item_id"],
            "given_url": item["given_url"],
            "time_updated": item["time_updated"],
            "favorite": item["favorite"]
        }
        for item in list_in_response.values()
    ]
    return items


# 今から七日以上前の記事のリストを取得
def get_delete_items(items):
    now = datetime.now()
    seven_days_ago_timestamp = (now - timedelta(days=31)).strftime("%s")
    passed_seven_days_items = [
        item for item in items
        if item["time_updated"] < seven_days_ago_timestamp
    ]
    return passed_seven_days_items


# pocket の delete 用の endpoint にリクエストを投げる
def delete_user_item(delete_list):
    delete_url = "https://getpocket.com/v3/send"
    for delete_item in delete_list:
        action = [{
            "action": "delete",
            "item_id": int(delete_item["item_id"])
        }]
        delete_data = {
            "consumer_key": CONSUMER_KEY,
            "access_token": ACCESS_TOKEN,
            "actions": action
        }
        requests.post(
            delete_url,
            data=json.dumps(delete_data),
            headers=request_headers
        )
    return None


# DB に入っている全ユーザーのaccess_tokenのリストを取得する
def get_user_access_token():
    conn = connector.connect(user="foo", host="bar", database="foobar")
    cur = conn.cursor()
    cur.execute("select access_token from users;")

    user_access_token_list = [
        row[0] for row in cur.fetchall()
    ]

    cur.close()
    conn.close()

    return user_access_token_list
