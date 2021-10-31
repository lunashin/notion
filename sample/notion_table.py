#!/usr/bin/python3

from requests.exceptions import Timeout
import requests
import json
import datetime
import locale
import time
import sys
import os




##################################################
# Params
##################################################

# HTTP通信タイムアウト
http_timeout = 3.5

# API送信間隔
wait_notion_api = 0.4



##################################################
# Class
##################################################

# notionテーブルクラス
class notion_table:
    list = []
    token = ""
    database_id = ""

    def __init__(self, token, database_id):
        self.database_id = database_id
        self.token = token

    # オブジェクトを構築する
    def make(self):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-08-16" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/databases/" + self.database_id + '/query'
        print('url : ' + url)
        # body
        body = '{}'
        # send
        try:
            res = requests.post(url, headers=headers, data=body, timeout=http_timeout)
        except Timeout:
            print("timeout")
            sys.exit()

        print(res.status_code)
        # print(res.text)
        if res.status_code == 200:
            self.parse(res.text)

    # bodyをパース
    def parse(self, json_text):
        j = json.loads(json_text)
        for i in range(len(j['results'])):
            rec = notion_table_record()
            rec.parse(j['results'][i])
            self.list.append(rec)

    # 指定行を更新
    def update_single(self, record, propatie_name):
        prop_names = [propatie_name]
        self.update(record, prop_names)

    # 指定行を更新
    def update(self, record, propatie_names):
        print('update')
        body = ""
        # make payload
        for prop_name in propatie_names:
            content = getattr(record, prop_name)
            type = getattr(record, prop_name + '_type')
            if body != "":
                body += ','
            body += self.make_update_payload(type, prop_name, content)
        payload = '{ "properties": {' + body + '}}'

        # update
        self.update_(record.id, payload)

    def update_title(self, row_id, key, text):
        body = self.make_update_payload("title", key, text)
        self.update_(row_id, body)

    # 指定行IDを更新
    def update_(self, row_id, payload):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/pages/" + row_id
        # send
        try:
            res = requests.patch(url, headers=headers, data=payload, timeout=http_timeout)
        except Timeout:
            print("timeout")
            sys.exit()

        print(res.status_code)
        # print(res.text)
        time.sleep(wait_notion_api)

    # payload 作成
    def make_update_payload(self, type, propertie_name, text):
        body = ""
        if type == 'url':
            body = '"{0}":{{"url":"{1}"}}'.format(propertie_name, text)
        if type == 'rich_text':
            body = '"{0}":{{"rich_text":[{{"text":{{"content":"{1}"}}}}]}}'.format(propertie_name, text)
        if type == 'title':
            body = '{{"properties":{{"{0}":{{"title":[{{"text":{{"content":"{1}"}}}}]}}}}}}'.format(propertie_name, text)
        print(body)
        return body





# notionレコードクラス
class notion_table_record:
    id = ""                     # 列ID ex) 27c04b6e-bb4a-4429-b7a3-f5ed026e4b45
    create_time = None          # 作成日
    last_edited_time = None     # 最終更新日

    # 各属性値を属性名を変数名としてメンバ変数へ格納
    def parse(self, json_result_obj):
        self.id = json_result_obj['id']

        # ex) 2021-09-17T09:01:00.000Z
        self.create_time = datetime.datetime.fromisoformat(json_result_obj['created_time'].replace('Z', '+00:00'))
        self.last_edited_time = datetime.datetime.fromisoformat(json_result_obj['last_edited_time'].replace('Z', '+00:00'))

        prop = json_result_obj['properties']
        for k, v in prop.items():
            # print(k)
            type = v['type']
            if type == 'title':
                setattr(self, k + '_type', 'title')
                if len(v[type]) != 0:
                    setattr(self, k, v[type][0]['plain_text'])
                else:
                    setattr(self, k, "")
            if type == 'rich_text':
                setattr(self, k + '_type', 'rich_text')
                if len(v[type]) != 0:
                    setattr(self, k, v[type][0]['plain_text'])
                else:
                    setattr(self, k, "")
            if type == 'number':
                setattr(self, k + '_type', 'number')
                if v[type] != None:
                    setattr(self, k, v[type])
                else:
                    setattr(self, k, None)
            if type == 'select':
                setattr(self, k + '_type', 'select')
                if v[type] != None:
                    setattr(self, k, v[type]['name'])
                else:
                    setattr(self, k, "")
            if type == 'url':
                setattr(self, k + '_type', 'url')
                if v[type] != None:
                    setattr(self, k, v[type])
                else:
                    setattr(self, k, "")
            if type == 'date':
                setattr(self, k + '_type', 'date')
                if v[type] != None:
                    if v[type]['start'] != None:
                        d = datetime.datetime.strptime(v[type]['start'], '%Y-%m-%d')
                        setattr(self, k + "_start", d)
                    else:
                        setattr(self, k + "_start", None)

                    if v[type]['end'] != None:
                        d = datetime.datetime.strptime(v[type]['end'], '%Y-%m-%d')
                        setattr(self, k + "_end", d)
                    else:
                        setattr(self, k + "_end", None)
                else:
                    setattr(self, k + "_start", None)
                    setattr(self, k + "_end", None)
