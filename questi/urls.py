from django.conf.urls import url
from questi.views import QuestionListView, QuestionDetailView
from questi import views

urlpatterns = [
    url(r'^create/$',views.create_question,),
    url(r'^index/$', QuestionListView.as_view(), name="question_list"),
    url(r'^question/(?P<slug>[^/]+)/$', QuestionDetailView.as_view(), name='question_detail'),
    url(r'^question/(?P<question_id>[0-9]+)/vote_up/$', views.question_vote_up,),
    url(r'^question/(?P<question_id>[0-9]+)/vote_down/$', views.question_vote_down,),
]