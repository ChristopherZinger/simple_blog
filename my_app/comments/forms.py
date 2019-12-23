from captcha.fields import ReCaptchaField
from django import forms
from . models import Comment

class CommentForm(forms.ModelForm):
    #captcha = ReCaptchaField()
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your Comment.',
        'class':'comment-text-input'}))
    class Meta:
        model = Comment
        fields = ['text',]
