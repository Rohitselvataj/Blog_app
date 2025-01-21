# blog/forms.py

from django import forms
from .models import Post


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    labels = forms.CharField(max_length=200, required=False)
    media = forms.FileField(required=False)
    class Meta:
        model = Post
        fields = '__all__'