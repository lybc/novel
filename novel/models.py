from peewee import *
import datetime

db = MySQLDatabase(host='localhost', user='homestead', passwd='secret', database='novel')

class BaseModel(Model):
    class Meta:
        database = db

class Chapter(BaseModel):
    id = PrimaryKeyField()
    title = CharField()
    content = CharField()
    seq = IntegerField()
    novel_id = IntegerField()
    source_url = CharField()

class Novel(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    source_url = CharField()
