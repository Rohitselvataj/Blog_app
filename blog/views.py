from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from pymongo import MongoClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime




client = MongoClient('mongodb://localhost:27017/')
db = client['blogger']
collection = db['blogg']
media_collection = db['media']

def dashboard(request):
    posts = Post.get_all()
    current_year = datetime.now().year
    return render(request, 'blog/dashboard.html', {'posts': posts, 'current_year': current_year})

def add_post(request):
    form = PostForm()
    current_year = datetime.now().year
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            labels = form.cleaned_data['labels']
            media_files = request.FILES.getlist('media')

            # Create a new Post instance and save it
            post_data = {
                'title': title,
                'content': content,
                'media': media,
                'labels': labels,
                # Add any other fields you want to save
            }
            post_id = collection.insert_one(post_data).inserted_id  # Save the post and get its ID

            # Handle media files (images/videos)
            media_ids = []  # List to store media IDs for reference
            for media in media_files:
                # Read the file and save it to MongoDB
                media_data = {
                    'filename': media.name,
                    'content_type': media.content_type,
                    'data': media.read()  # Read the file data
                }
                media_id = media_collection.insert_one(media_data).inserted_id  # Save to media collection
                media_ids.append(media_id)  # Store the media ID

            # Link the media IDs to the post
            collection.update_one({'_id': post_id}, {'$set': {'media_ids': media_ids}})

            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = PostForm()  # Redirect to the dashboard after saving
    return render(request, 'blog/add_post.html', {'form': form, 'current_year': current_year})



def my_posts(request):
    posts = Post.get_all() 
    current_year = datetime.now().year 
    return render(request, 'blog/my_posts.html', {'posts': posts, 'current_year': current_year})

def edit_post(request, post_id):
    post_data = Post.get_by_id(post_id)  # Assuming you have a method to get a post by ID
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            updated_data = {
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
                'labels': form.cleaned_data['labels'],
                # Handle images/videos if needed
            }
            Post.update(post_id, updated_data)  # Assuming you have a method to update a post
            return redirect('dashboard')
    else:
        # Pre-fill the form with existing post data
        initial_data = {
            'title': post_data['title'],
            'content': post_data['content'],
            'labels': post_data.get('labels', None),
            # Add any other fields you want to pre-fill
        }
        form = PostForm(initial=initial_data)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post_data})

def delete_post(request, post_id):
    # Assuming you have a method to delete a post
    collection.delete_one({'_id': post_id})  # Delete the post from MongoDB
    return redirect('my_posts')

@csrf_exempt  # Use with caution; consider using CSRF tokens for security
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Handle the image upload logic here
        return JsonResponse({'location': '/path/to/image'})  # Return the image URL
    return JsonResponse({'error': 'Image upload failed'}, status=400)