from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from questi.models import Question, Vote


def index(request):
    questions = Question.objects.all()
    return render(request, "questi/question_list.html", context={"questions": questions})


def create_question(request):
    class QuestionForm(forms.ModelForm):

        title = forms.CharField(min_length=10, max_length=200, widget=forms.TextInput(attrs={'size': 60}))
        text = forms.CharField(min_length=20, max_length=2000, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

        class Meta:
            model = Question
            fields = ['title', 'text']

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.questioner = request.user
            new_question.save()
            return redirect('question_list')
        else:
            return render(request, 'questi/question_create.html', {'form': form})
    form = QuestionForm(None)
    return render(request, 'questi/question_create.html', {'form': form})


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


def question_vote_up(request, question_id):
    if request.method == "POST" and request.user.is_authenticated():
        question = Question.objects.get(pk=question_id)
        try:
            user_vote = question.vote_set.get(voter=request.user)
            user_vote.vote_up()
            user_vote.save()
            return HttpResponse("aktualisiert")

        except Vote.DoesNotExist:
            new_user_vote = Vote(voted_question=question, rate=1)
            new_user_vote.save()
            return HttpResponse("neuer Vote")
    else:
        pass


def question_vote_down(request, question_id):
    if request.method == "POST" and request.user.is_authenticated():
        question = Question.objects.get(pk=question_id)
        try:
            user_vote = question.vote_set.get(voter=request.user)
            user_vote.vote_down()
            user_vote.save()
            return HttpResponse("aktualisiert")

        except Vote.DoesNotExist:
            new_user_vote = Vote(voted_question=question, rate=-1)
            new_user_vote.save()
            return HttpResponse("neuer Vote")
    else:
        pass