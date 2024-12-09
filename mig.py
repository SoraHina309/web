from pymongo import MongoClient

# 连接 MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["resume"]
collection = db["projects"]

# 聚合查询重复数据
pipeline = [
    {
        "$group": {
            "_id": {"name": "$name", "discription": "$discription"},
            "count": {"$sum": 1},
            "ids": {"$push": "$_id"}
        }
    },
    {"$match": {"count": {"$gt": 1}}}
]

duplicates = list(collection.aggregate(pipeline))

# 打印重复数据
for duplicate in duplicates:
    print("Duplicate group:", duplicate["_id"])
    print("Duplicate IDs:", duplicate["ids"])

for duplicate in duplicates:
    ids_to_delete = duplicate["ids"][1:]  # 保留第一条记录
    collection.delete_many({"_id": {"$in": ids_to_delete}})
    print(f"Deleted {len(ids_to_delete)} duplicate documents.")