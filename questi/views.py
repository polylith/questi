from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from questi.models import Question


def index(request):
    questions = Question.objects.all()
    return render(request, "questi/question_list.html", context={"questions": questions})


def post_question(request):
    class QuestionForm(forms.ModelForm):

        title = forms.CharField(min_length=10, max_length=200, widget= forms.TextInput(attrs={'size': 60}))
        text = forms.CharField(min_length=20,max_length=2000, widget= forms.Textarea(attrs={'cols': 60, 'rows': 10}))

        class Meta:
            model = Question
            fields = ['title', 'text']

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
        else:
            return render(request,'questi/question_create.html',{'form':form})
    form = QuestionForm(None)
    return render(request,'questi/question_create.html',{'form':form})



class QuestionListView(ListView):

    model = Question
    queryset = Question.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)

        return context

class QuestionDetailView(DetailView):

    model = Question
    slug_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        return context