from django.conf.urls import url
from questi.views import QuestionListView, QuestionDetailView, QuestionUpdateView, AnswerUpdateView
from questi import views

urlpatterns = [
    url(r'^question/create/$', views.create_question, ),
    url(r'^questions/$', QuestionListView.as_view(), name="question_list"),
    url(r'^question/(?P<slug>[^/]+)/$', QuestionDetailView.as_view(), name='question_detail'),
    url(r'^question/(?P<question_id>[0-9]+)/vote_up/$', views.question_vote_up, name="question_vote_up"),
    url(r'^question/(?P<question_id>[0-9]+)/vote_down/$', views.question_vote_down, name="question_vote_down"),
    url(r'^question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/vote_up/$', views.answer_vote_up, name="answer_vote_up"),
    url(r'^question/(?P<question_id>[0-9]+)/answer/(?P<answer_id>[0-9]+)/vote_down/$', views.answer_vote_down, name="answer_vote_down"),
    url(r'^question/(?P<slug>[^/]+)/edit/$', QuestionUpdateView.as_view(), name='question_update'),
    url(r'^question/(?P<question_id>[0-9]+)/answer/(?P<slug>[^/]+)/edit/$', AnswerUpdateView.as_view(), name='answer_update')
]
