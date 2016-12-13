from django.db import models
from mongoengine import *
# Create your models here.
# connect('ganji', host='localhost', port=27017)


class ItemInfo(Document):
    pub_date = StringField()
    look = StringField()
    area = ListField(StringField())
    title = StringField()
    url = StringField()
    cates = ListField(StringField())
    price = FloatField()
    time = IntField()
    meta = {
        'collection': 'item_info2_1'
    }
pipeline = [
    {'$sort': {'pub_date': -1}},
    {'$limit': 1}
]
last_pub_date = []
for i in ItemInfo._get_collection().aggregate(pipeline):
    last_pub_date.append(i['pub_date'])
# print(last_pub_date)
