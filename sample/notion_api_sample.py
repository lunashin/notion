#!/usr/local/bin/python3

import requests
import json
import time
import sys



##############################################
# Class
##############################################

class notion_api_sample:
    token = ""
    dbid = ""

    def __init__(self, token, dbid):
        self.token = token
        self.dbid = dbid

    def read_table(self):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/databases/" + self.dbid + '/query'
        print('url : ' + url)
        # body
        body = '{}'
        # send
        res = requests.post(url, headers=headers, data=body)
        print(res.status_code)
        print(res.text)
        j = json.loads(res.text)
        # print(j)
        print()
        # print(j['results'][1]['properties']['memo']['rich_text']['plain_text'])
        print(len(j['results']))
        for i in range(len(j['results'])):
            if i == 0:
                continue
            print(j['results'][i]['properties']['memo']['rich_text'][0]['plain_text'])
            print(j['results'][i]['properties']['Column']['select']['name'])
            print(j['results'][i]['properties']['Name']['title'][0]['plain_text'])
            print(j['results'][i]['properties']['num']['number'])
            print(j['results'][i]['properties']['date']['date']['start'])
            print(j['results'][i]['properties']['date']['date']['end'])
            print()

        # print('json_dict:{}'.format(type(json_dict)))

    def get_table_rows_id(self):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/databases/" + self.dbid + '/query'
        print('url : ' + url)
        # body
        body = '{}'
        # send
        res = requests.post(url, headers=headers, data=body)
        print("status code : " + str(res.status_code))
        if res.status_code != 200:
            print("aborted.")

        # print(res.text)
        j = json.loads(res.text)
        list_id = []
        for item in j['results']:
            list_id.append(item['id'])

        return list_id


    def update_table_field(self, row_id):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/pages/" + row_id
        # body
        body = '{"properties": {"Name": {"title": [{"text": {"content": "test_@@@"}}]}}}'
        # send
        res = requests.patch(url, headers=headers, data=body)
        print(res.status_code)
        print(res.text)
        json_obj = json.loads(res.text)
        print(json_obj)
        # print('json_dict:{}'.format(type(json_dict)))


    def delete_row(self, row_id):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/pages/" + row_id
        # body
        body = '{ "archived": true }'
        # send
        res = requests.patch(url, headers=headers, data=body)
        print(res.status_code)
        print(res.text)
        json_obj = json.loads(res.text)
        print(json_obj)
        # print('json_dict:{}'.format(type(json_dict)))


    def delete_all_row(self):
        # idリストを取得
        list = self.get_table_rows_id()
        # 削除
        for id in list:
            self.delete_row(id)
            time.sleep(0.3)


    def add_record(self):
        # headers
        #  "Authorization: Bearer xxx" \
        #  "Content-Type: application/json" \
        #  "Notion-Version: 2021-05-13" \
        headers = { "Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Notion-Version": "2021-08-16" }
        # url
        url = "https://api.notion.com/v1/pages/"
        # body
        # body = '{"properties": {"Name": {"title": [{"text": {"content": "test_@@@"}}]}}}'
        # body = '{"parent":{"database_id":"dbid"},"properties":{"Name":{"title":[{"text":{"content":"ジョジョ"}}]}}}'
        # body = '{"parent":{"database_id":"dbid"},"properties":{"Name":{"title":[{"text":{"content":"aaa"}}]},"memo":{"rich_text":[{"text":{"content":"コンテンツ"}}]}}}'
        body = '{"parent":{"database_id":"dbid"},"properties":{"Name":{"title":[{"text":{"content":"aaa"}}]},"memo":{"rich_text":[{"text":{"content":"コンテンツ"}}]},"date":{"date":{"start":"2020-12-08","end":null}}}}'
        body = body.replace("dbid", self.dbid)
        body = body.encode('utf-8')
        # send
        res = requests.post(url, headers=headers, data=body)
        print(res.status_code)
        print(res.text)
        json_obj = json.loads(res.text)
        print(json_obj)
        # print('json_dict:{}'.format(type(json_dict)))
