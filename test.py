str = """{"user": "jerry", "info": "msg"}"""
from bson import json_util

print(json_util.loads(str))