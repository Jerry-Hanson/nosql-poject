from pymongo import MongoClient
class Mongo(object):
    def __init__(self,host='localhost',port=27017):
        self.client = MongoClient(host,port)
    def delete(self, database, collection, filter):
        # filter: 删除的条件
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.delete_many(filter)
        print(result.acknowledged)
        return result.acknowledged
    def __del__(self):
        self.client.close()
if __name__ == '__main__':
    mongo = Mongo()
    # 删除的条件
    filter={
        "username":'zhangsan'
    }
    mongo.delete('user','receiver',filter)