from django.db import models
from bson.objectid import ObjectId
from .mongo import collection
from tinymce.widgets import TinyMCE
from django import forms
from tinymce.models import HTMLField 

class Post:
    def __init__(self, title, content, media=None, labels=None):
        self.title = title
        self.content = content
        self.media = media
        self.labels = labels

    def save(self):
        post_data = {
            'title': self.title,
            'content': self.content,
            'media': self.media,
            'labels': self.labels
        }
        result = collection.insert_one(post_data)
        return str(result.inserted_id)
        

    @staticmethod
    def get_all():
        return list(collection.find())

    @staticmethod
    def get_by_id(post_id):
        return collection.find_one({'_id': ObjectId(post_id)})

    @staticmethod
    def update(post_id, updated_data):
        collection.update_one({'_id': ObjectId(post_id)}, {'$set': updated_data})

    @staticmethod
    def delete(post_id):
        collection.delete_one({'_id': ObjectId(post_id)})

class DummyPost(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    media = models.CharField(max_length=200, blank=True, null=True)  
    labels = models.CharField(max_length=200, blank=True, null=True)  

    class Meta:
        managed = False