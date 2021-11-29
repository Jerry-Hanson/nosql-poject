# 1. 导入MongoClient
from pymongo import MongoClient
import datetime
from pymongo.errors import DuplicateKeyError


# 首先，需要一个类，把对数据库的增删改查操作封装为一个接口
# 该类的名名字随便期
class MongodbDao(object):
    # 初始化，就是连接数据库
    # port:必须是个整数，不能加引号变成字符串
    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host, port)

    # 插入数据
    def insert(self, database, collection, document):
        try:
            _database = self.client.get_database(database)
            _collection = _database.get_collection(collection)
            #  如果document 是个字典，说明就是一个值，就可以用insert_one()
            # isinstance:是python里的函数，判断一个对象是个个字典，还是个列表
            if isinstance(document, dict):
                result = _collection.insert_one(document)
                # 如果插入成功就返回一个result.acknowledged
                return result.acknowledged
            elif isinstance(document, list):
                result = _collection.insert_many(document)
                return result.acknowledged
            else:
                return False
        except DuplicateKeyError:
            return False

    def delete(self, database, collection, filter):
        # filter: 删除的条件
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.delete_many(filter)
        print(result.acknowledged)
        return result.acknowledged

    def search(self, database, collection, filter):
        """
        :param database:   数据库
        :param collection: 表
        :param filter:     查询条件,查询条件必须是个字典
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        # 把查询结果转化成列表
        results = list(_collection.find(filter))
        # print(type(results))
        # print(dir(results))
        # print(results)
        # 将查询结果return
        return results

    def update(self, database, collection, filter, document_to):
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        # filiter: 更新的条件
        # update：第二个参数：即是否要更新的数据。即用update去更新那些符合filter条件的数据
        # 更新的操作:要更新的数据，首先是个字典，字典里面的格式为：{"$set":要更新的内容}
        result = _collection.update_many(filter, {"$set": document_to}, upsert=True)

    def __del__(self):
        self.client.close()


# if __name__ == '__main__':
#     mongo = MongodbDao()
#     data = [
#         # 如果指定了插入时的id值，就会用你指定的值，如果没有指定id值，插入后就会自动有个ObjectId("5bb9bc6aa236ce29f4898035")
#         {
#             # '_id':'1',
#             "username": 'zhangsan',
#             "msg": 'hello',
#             'date': datetime.datetime.now()
#         },
#         {
#             # '_id': '2',
#             "username": 'lisi',
#             "msg": '你好',
#             'date': datetime.datetime.now()
#         },
#         {
#             # '_id': '3',
#             "username": 'wangwu',
#             "msg": 'fine',
#             'date': datetime.datetime.now()
#         },
#     ]
#     # 插入数据
#     # 'user':要插入的库，如果不存在，mongoDB会自动帮你创建这个库
#     # 'receiver'：表，如果不存在，MongoDB会自动帮你创建表
#     # data: 要插入到 trade_center库下面的users表里的数据
#     mongo.insert('test', 'test', data)
