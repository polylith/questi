from django.contrib import admin
from questi import models


# Register your models here.

class VoteInline(admin.TabularInline):
    model = models.Vote


class QuestionAdmin(admin.ModelAdmin):
    inlines = [VoteInline, ]
    extra = 0

admin.site.register(models.Question, QuestionAdmin)
