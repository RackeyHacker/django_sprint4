from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].widget = forms.DateTimeInput(
            attrs={'type': 'date'},
            format='%Y-%m-%dT%H:%M'
        )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
