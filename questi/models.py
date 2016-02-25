from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=2000)
    title = models.CharField(max_length=200)
    questioner = models.ForeignKey(User,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)


    def get_rate(self):
        ges_rate = 0
        for vote in self.vote_set.all():
            ges_rate += vote.rate
            return ges_rate
        return ges_rate
    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.CharField(max_length=2000)
    question = models.ForeignKey(Question)
    answerer = models.ForeignKey(User,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

class Comment(models.Model):
    text = models.CharField(max_length=2000)
    commentator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commented_question = models.ForeignKey(Question)
    commented_answer = models.ForeignKey(Answer)


class Vote(models.Model):
    voter = models.ForeignKey(User,null=True)
    rate = models.IntegerField(choices=(
        (1, "Upvote"),
        (-1, "Downvote"),
    ))
    voted_question = models.ForeignKey(Question,null=True)
    voted_answer = models.ForeignKey(Answer,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def vote_up(self):
        if self.rate == 1:
            pass
        else:
            self.rate = 1

    def vote_down(self):
        if self.rate == -1:
            pass
        else:
            self.rate == -1


