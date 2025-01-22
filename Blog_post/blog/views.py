from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from pymongo import MongoClient

from .forms import CommentForm, PostForm


client = MongoClient('mongodb+srv://rohit:Rohit2004@cluster0.oxj1e.mongodb.net/')
db = client['Blogdb']
posts_collection = db['posts']
comments_collection = db['comments']

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def dashboard(request):
    posts = list(posts_collection.find())
    return render(request, 'dashboard.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            posts_collection.insert_one({
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
                'author': request.user.username
            })
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def view_post(request, post_id):
    post = posts_collection.find_one({'_id': post_id})
    comments = list(comments_collection.find({'post_id': post_id}))
    form = CommentForm(initial={'post_id': post_id})
    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'form': form})

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments_collection.insert_one({
                'post_id': form.cleaned_data['post_id'],
                'comment': form.cleaned_data['comment'],
                'author': request.user.username
            })
            return redirect('view_post', post_id=form.cleaned_data['post_id'])
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

