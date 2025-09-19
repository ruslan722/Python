from peewee import Model, AutoField, CharField, IntegerField, MySQLDatabase, DateTimeField

db = MySQLDatabase('sfetofor', user='root',
                   password='root', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class TrafficLight(BaseModel):
    id = AutoField()
    location = CharField()
    status = CharField()
    last_updated = DateTimeField()
    duration = IntegerField()

db.connect()
db.create_tables([TrafficLight])
db.close()
