from django import forms
from .models import News, Post, Comment

class PostImageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image"]


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "date", "teaser", "content", "image"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "date", "category", "intro", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "author_email", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 5}),
        }


class CommentModerationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["status", "owner_reply"]
        widgets = {
            "owner_reply": forms.Textarea(attrs={"rows": 4}),
        }