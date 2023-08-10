from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *


class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ['title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 3:
            raise ValidationError({
                "title": "Title must be at least 3 letters!"
            })
        text = cleaned_data.get("text")
        if text == title:
            raise ValidationError({
                "text": "The text must not match the title!"
            })
        return cleaned_data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            self.fields['comment_text'].label = "Write your comment here:"

