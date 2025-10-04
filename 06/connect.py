from peewee import Model, MySQLDatabase, IntegerField, CharField, AutoField

db = MySQLDatabase(
    'motivation',
    user='root',
    password='root',
    host='localhost',
    port=3306
)

class BaseModel(Model):
    class Meta:
        database = db

class SurveyResult(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    mood = CharField()
    score = IntegerField()

class MotivationQuote(BaseModel):
    id = AutoField()
    text = CharField()
    mood_tag = CharField()
    author = CharField(null=True)


db.connect()
db.create_tables([SurveyResult, MotivationQuote], safe=True)
db.close()

