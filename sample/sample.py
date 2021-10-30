#!/usr/local/bin/python3

import notion_api_sample as notion
import sys



token=""
dbid = ""

notion = notion.notion_api_sample(token, dbid)

notion.add_record()
# notion.delete_all_row()
# notion.read_table(dbid)
# notion.update_table_field("b335c723-4697-42a6-9c45-4ab333c3c24b")
# notion.delete_row("b335c723-4697-42a6-9c45-4ab333c3c24b")
