from django import forms
from .models import Comment


class BoardSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word') # form을 구성하는 모든 요소를 넣어주는 기능
#
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)