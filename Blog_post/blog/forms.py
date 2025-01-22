from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

class CommentForm(forms.Form):
    post_id = forms.CharField(widget=forms.HiddenInput())
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
