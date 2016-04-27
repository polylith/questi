from django import template

register = template.Library()


@register.simple_tag
def answer_is_vote_up(user, answer):
    if answer.is_vote_by_user(user) == 1:
        return "active"
    else:
        return ""

@register.simple_tag
def answer_is_vote_down(user, answer):
    if answer.is_vote_by_user(user) == -1:
        return "active"
    else:
        return "###´" \
               "" \
