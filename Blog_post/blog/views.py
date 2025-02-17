from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
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
            return redirect('dashboard')
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
    for post in posts:
        post['str_id'] = str(post['_id'])
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
    post = posts_collection.find_one({'_id': ObjectId(post_id)})
    comments = list(comments_collection.find({'post_id': post_id}))
    comment_form = CommentForm(initial={'post_id': post_id})
    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

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

def delete_post(request, post_id):
    if request.user.is_authenticated:
        post = posts_collection.find_one({'_id': ObjectId(post_id)})
        if post and post['author'] == request.user.username:
            posts_collection.delete_one({'_id': ObjectId(post_id)})
        else:
            return render(request, 'dashboard.html', {
                'posts': list(posts_collection.find()),
                'error': 'You are not authorized to delete this post.'
            })
    return redirect('dashboard')
