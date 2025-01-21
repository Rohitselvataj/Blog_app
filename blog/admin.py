from django.contrib import admin

# Register your models here.
# blog/admin.py
from .models import DummyPost
from django.contrib import admin
from django.http import HttpResponse
from .mongo import collection  # Import your MongoDB collection

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'labels')  # Customize as needed

    def get_queryset(self, request):
        # Return all posts from MongoDB
        return list(collection.find())

    def save_model(self, request, obj, form, change):
        # Handle saving a post
        post_data = {
            'title': obj.title,
            'content': obj.content,
            'labels': obj.labels,
            # Add other fields as necessary
        }
        collection.insert_one(post_data)

    def delete_model(self, request, obj):
        # Handle deleting a post
        collection.delete_one({'title': obj.title})

# Register the custom admin
admin.site.register(DummyPost, PostAdmin)
