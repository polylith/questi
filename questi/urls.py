from django.conf.urls import url
from questi.views import QuestionListView, QuestionDetailView
from questi import views

urlpatterns = [
    url(r'^create/',views.post_question,),
    url(r'^index', QuestionListView.as_view(), name="question_list"),
    url(r'^question/(?P<slug>[^/]+)', QuestionDetailView.as_view(), name='question_detail'),
]