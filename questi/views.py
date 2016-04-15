from django import forms
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from questi.models import Question, Vote, Answer
from questi.forms import QuestionForm, AnswerForm


def index(request):
    questions = Question.objects.all()
    return render(request, "questi/question_list.html", context={"questions": questions})


def create_question(request):
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
        form = AnswerForm(None)
        context['answer_form'] = form
        context['user_vote'] = self.object.is_vote_by_user(self.request.user)
        try:
            context['success_text'] = self.request.session.get('success_text', None)
            del self.request.session['success_text']
        except KeyError:
            pass
        return context

    def post(self, request, **kwargs):
        self.object = Question.objects.get(pk=kwargs.get('slug'))

        form = AnswerForm(request.POST)
        context = self.get_context_data(**kwargs)
        if form.is_valid() and request.user.is_authenticated():
            new_answer = form.save(commit=False)
            new_answer.question = self.object
            new_answer.answerer = request.user
            new_answer.save()
            return self.render_to_response(context)
        else:
            context['answer_form'] = form
            return self.render_to_response(context)


class QuestionUpdateView(UpdateView):
    model = Question
    slug_field = 'pk'
    fields = ['text',
              'title']
    template_name_suffix = '_update'

    def get_success_url(self):
        user = self.request.user
        self.request.session["success_text"] = "Frage wurde erfolgreich editiert."
        return "/question/" + str(self.object.id)


def question_vote_up(request, question_id):
    if request.method == "POST" and request.user.is_authenticated():
        question = Question.objects.get(pk=question_id)
        vote = request.user.vote_question(question, 1)
        if vote != None:
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()


def question_vote_down(request, question_id):
    if request.method == "POST" and request.user.is_authenticated():
        question = Question.objects.get(pk=question_id)
        vote = request.user.vote_question(question, -1)
        if vote != None:
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()
