
from django import forms
from . models import Post#, Images
from django.forms import TextInput,Select

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'topic']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            'subtitle': TextInput(attrs={'placeholder': 'Subtitle'}),
            }

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'description', 'topic']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            'subtitle': TextInput(attrs={'placeholder': 'Subtitle'}),
            'description': TextInput(attrs={'placeholder': 'Post description'}),
            }

# class ImgForm(forms.ModelForm):
#     class Meta:
#         model = Images
#         fields = ['image',]
