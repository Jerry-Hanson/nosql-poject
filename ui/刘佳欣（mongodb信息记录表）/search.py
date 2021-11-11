# 1. 导入MongoClient
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# 首先，需要一个类，把对数据库的增删改查操作封装为一个接口
# 该类的名名字随便期
class Mongo(object):
    def __init__(self,host='localhost',port=27017):
        self.client = MongoClient(host,port)
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
        print(type(results))
        print(dir(results))
        print(results)
        # 将查询结果return
        return results
    def __del__(self):
        self.client.close()
if __name__ == '__main__':
    mongo = Mongo()
    # 定义查询条件，查询条件必须是个字典
# 像下面的写法，是and的关系
    filter={
        "username":"zhangsan"# 注意：查询条件里，如果值是int等类型时，不能加“”，否则就会查不到数据，同理，删除/更新也是一样的
    }
    mongo.search('user','receiver',filter)