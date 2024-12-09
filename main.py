from db_module import MyMongodb


def main():   
    db = MyMongodb("resume")
    
    # db.insert_more("skills",[
    #     {'name':'python'},
    #     {'name':'C'},
    #     {'name':'D'}
    # ])
    db.update_data("projects", 
        # {'name': 'web','description': 'A'},
        # {'name':'Portfolio website','description':'A personal'},
        # {'name':'E-commerce Platform','description':'An online'}
        {'name':'Robot Programming','description':'I used to program my own robots to behave as expected at Matilda Wahing Middle School.'},
        {'name':'In junior high school','description':'I used to program my own robots to behave as expected at Matilda Wahing Middle School.',"gallery": ["/static/img/img1.jpg", "/static/img/img2.jpg", "/static/img/img3.jpg"]}
        )
    # db.insert_data("comments",{'project_name':'one','name':'A','rating':3,'text':'just so so'})
    # db.insert_data("email",'@auck.com')
    # db.delete_data("projects",
    #     {'name': 'web','description': 'A'}
    #     {'name':'Portfolio website','description':'A personal'}
    # )
    # db.insert_contact("contact", 
    # {
    #     'email':'mikuohatsune0712@gmail.com',
    #     'phone':'13647482621',
    # },
    # {
    #     'email':'mikuohatsune0712@gmail.com',
    #     'phone1':'02108500920',
    #     'phone2':'13647482621',
    # }
    # )
#    for i in db.find_data("myconn", {"_id": '6736d5713c766ba10baf0fd4'}):
#        print(i)

if __name__ == "__main__":
    main()

