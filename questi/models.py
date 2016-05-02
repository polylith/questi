# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=2000)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def get_time_as_string(self):
        create_time = self.created_at.strftime('%d.%m.%Y %H:%M %S Uhr')
        update_time = self.updated_at.strftime('%d %m %Y %H:%M %S Uhr')
        if create_time == update_time:
            return "{0} {1} von {2}".format(_("created at"), self.created_at.strftime('%d.%m.%Y %H:%M Uhr'),
                                            self.user)
        else:
            return "{0} {1} von {2}".format(_("last changed at"), self.updated_at.strftime('%d.%m.%Y %H:%M Uhr'),
                                            self.user)

    def get_rate(self):
        ges_rate = 0
        for vote in self.vote_set.all():
            ges_rate += vote.rate
            return ges_rate
        return ges_rate

    def is_vote_by_user(self, user):
        try:
            vote = user.vote_set.get(voted_question=self.id)
            return vote.rate
        except Vote.DoesNotExist:
            return 0

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    text = models.CharField(max_length=2000)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_rate(self):
        ges_rate = 0
        for vote in self.vote_set.all():
            ges_rate += vote.rate
            return ges_rate
        return ges_rate

    def is_vote_by_user(self, user):
        try:
            vote = user.vote_set.get(voted_answer=self.id)
            return vote.rate
        except Vote.DoesNotExist:
            return 0

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=2000)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    commented_question = models.ForeignKey(Question)
    commented_answer = models.ForeignKey(Answer)


class Vote(models.Model):
    user = models.ForeignKey(User, null=True)
    rate = models.IntegerField(choices=(
        (1, "Upvote"),
        (-1, "Downvote"),
    ))
    voted_question = models.ForeignKey(Question, null=True)
    voted_answer = models.ForeignKey(Answer, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_rate(self, rate):
        if rate > 1:
            self.rate = 1
        elif rate < -1:
            self.rate = -1
        elif rate == 0:
            pass
        else:
            self.rate = rate


# new auth.user functions
def vote_question(user, question, rate):
    try:
        user_vote = user.vote_set.get(voted_question=question)
        if user_vote.rate == rate:
            user_vote.delete()
            return None
        else:
            user_vote.set_rate(rate)
            user_vote.save()
            return user_vote
    except Vote.DoesNotExist:
        new_user_vote = Vote(voted_question=question, user=user)
        new_user_vote.set_rate(rate)
        new_user_vote.save()
        return new_user_vote


def vote_answer(user, answer, rate):
    try:
        user_vote = user.vote_set.get(voted_answer=answer)
    except Vote.DoesNotExist:
        new_user_vote = Vote(voted_answer=answer, user=user)
        new_user_vote.set_rate(rate)
        new_user_vote.save()
        return new_user_vote

    if user_vote.rate == rate:
        user_vote.delete()
        return None
    else:
        user_vote.set_rate(rate)
        user_vote.save()
        return user_vote


User.add_to_class('vote_question', vote_question)
User.add_to_class('vote_answer', vote_answer)
