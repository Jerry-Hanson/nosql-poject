from pymongo import MongoClient
import datetime
class Mongo(object):
    def __init__(self,host='localhost',port=27017):
        self.client = MongoClient(host,port)
    def update(self,database,collection,filter,document_to):
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        # filiter: 更新的条件
        # update：第二个参数：即是否要更新的数据。即用update去更新那些符合filter条件的数据
        # 更新的操作:要更新的数据，首先是个字典，字典里面的格式为：{"$set":要更新的内容}
        result = _collection.update_many(filter,{"$set":document_to},upsert=True)
if __name__ == '__main__':
    mongo = Mongo()
    # filter:条件
    filter = {
        "username": "lisi"
    }
    #  要更新成的数据
    document_to = {
        "username": "lisi",
        "msg": "yo yo~",
        "date": datetime.datetime.now()
    }
    mongo.update('user','receiver', filter, document_to)