from pymongo import MongoClient

class MyMongodb:

    client = None

    def __init__(self, name):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.name = name
        __all__=['db']
        
    #选择或者创建数据库
    def select_collection(self, db_name):
        return self.client[self.name][db_name]

    #插入数据
    def insert_contact(self,db_name, data):
        collection = self.select_collection(db_name)
        return collection.insert_one(data)
    
    def insert_comment(self,db_name, data):
        collection = self.select_collection(db_name)
        return collection.insert_one(data)

    def insert_data(self, db_name, data):
            collection = self.select_collection(db_name)
            for i in collection.find():
                if data['name'] == i['name']:
                    break
                else:
                    return collection.insert_one(data)
            print("element exist insert false")

    #插入更多數據
    def insert_more(self, db_name, data):
        collection = self.select_collection(db_name)
        inserted_count = 0
        existing_count = 0

        for document in data:
            # 使用 find_one 来检查是否存在具有相同名称的文档
            existing_document = collection.find_one({'name': document['name']})
            if existing_document:
                existing_count += 1
            else:
                # 如果不存在，则插入新文档
                collection.insert_one(document)
                inserted_count += 1

        print(f"{existing_count} elements already exist, {inserted_count} elements inserted.")
        return collection

    #獲取數據（名字）
    def get_skills(self,db_name):
        collection = self.select_collection(db_name)
        data=list (collection.find({}, {'_id': 0}))
        return [skill['name'] for skill in data]    

    #獲取數據（成就）
    def get_projects(self,db_name):
        collection = self.select_collection(db_name)
        data= list(collection.find({}, {'_id': 0, 'name': 1, 'description':1}))
        return data

    #获取联系方式
    def get_contact(self,db_name):
        collection = self.select_collection(db_name)
        data= collection.find_one({}, {'_id': 0})
        return data

    def get_comments(self,db_name):
        collection = self.select_collection(db_name)
        data= list(collection.find({},{'_id':1,'name':1, 'rating':1, 'text':1}))
        return data

    def count_documents(self,db_name,name):
        collection = self.select_collection(db_name)
        data= list(collection.find())
        count = 0
        for i in data:
            if name in i.values():
                count+=1
        return count
    def get_comments_owner(self,db_name,comments_id):
        collection = self.select_collection(db_name)
        data = list(collection.find({},{'_id':1,'name':1}))
        
        for i in data: 
            if str(i['_id']) == str(comments_id):
                return i['name']

    # def get_email(self,db_name):
    #     collection = self.select_collection(db_name)
    #     data= list(collection.find({}, {'_id': 0, 'email': 1, 'phone':0}))
    #     return data

    # def get_phone(self,db_name):
    #     collection = self.select_collection(db_name)
    #     data= list(collection.find({}, {'_id': 0, 'email': 0, 'phone':1}))
    #     return data 
    


    # def get_collection_data(self,db_name,field, filter_query=None,limit=None):
    #     collection = self.select_collection(db_name)
    #     filter_query = filter_query or {}
    #     cursor = collection.find(filter_query,{field:1,'_id':0})
    #     return [doc[field] for doc in cursor]



    #查找数据
    def find_data(self, db_name, query):
        collection = self.select_collection(db_name)
        results = collection.find(query)
        return results

    #删除数据
    def delete_data(self, db_name, query):
        collection = self.select_collection(db_name)
        return collection.delete_many(query)

    #更新数据
    def update_data(self, db_name, query, new_data):
        collection = self.select_collection(db_name)
        return collection.update_many(query,{"$set":new_data})


# if __name__ == "__main__":
#         db = MyMongodb('resume')

#         result = db.get_data("skills")
#         print(result)

        