from pymongo import MongoClient
 
client = MongoClient('localhost', 27017) # MongoDB服务地址和端口
db = client['my_database'] # 要打开的数据库名
# 在这里可以对db进行操作
db.my_collections.insert_one({'name':"example"})
print("collections:",db.list_collection_names())
