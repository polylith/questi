from django import forms

from questi.models import Answer, Question


class QuestionForm(forms.ModelForm):
    title = forms.CharField(min_length=10, max_length=200, widget=forms.TextInput(attrs={'size': 60}))
    text = forms.CharField(min_length=20, max_length=2000, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    text = forms.CharField(min_length=20, max_length=2000, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

    class Meta:
        model = Answer
        fields = ['text']
