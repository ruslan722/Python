from peewee import MySQLDatabase, Model, AutoField, CharField, IntegerField


db = MySQLDatabase(
    'fastapi',  
    user='root',
    password='root',
    host='localhost',
    port=3306
)


class BaseModel(Model):
    class Meta:
        database = db


class Course(BaseModel):
    id = AutoField()
    title = CharField()
    instructor = CharField()
    duration = IntegerField() 
    level = CharField() 


db.connect()
db.create_tables([Course], safe=True)

db.close()

