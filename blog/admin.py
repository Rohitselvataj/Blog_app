from django.contrib import admin

# Register your models here.
# blog/admin.py
from .models import DummyPost
from django.contrib import admin
from django.http import HttpResponse
from .mongo import collection  

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'labels')  
    def get_queryset(self, request):
        return list(collection.find())
    
    def save_model(self, request, obj, form, change):
        post_data = {
            'title': obj.title,
            'content': obj.content,
            'labels': obj.labels,
        }
        collection.insert_one(post_data)

    def delete_model(self, request, obj):
        collection.delete_one({'title': obj.title})


admin.site.register(DummyPost, PostAdmin)
