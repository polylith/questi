from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from questi.models import Question, Vote


# Create your tests here.
class ForumTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(title="Test Question")
        self.user = User.objects.create_user('test', 'test@test.de', 'passw0rd')

    def test_questi_list(self):
        question = Question.objects.get(pk=1)
        self.assertIsNotNone(question)

    def test_questi_vote_up(self):
        test_user = User.objects.get(pk=1)
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_up/')
        self.assertEqual(self.question.get_rate(), 1)

    def test_questi_authentication(self):
        test_user = User.objects.get(pk=1)
        self.client.post('/admin/', {'username': 'test', 'password1': 'passw0rd'})
        assert test_user.is_authenticated()

    def test_questi_post_question(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/create/',
                         {'title': 'Question1: Lorem ipsum dolor sit amet, consetetur sadipscing elitr',
                          'text': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'})
        new_question = Question.objects.get(pk="2")
        self.assertEqual(new_question.title, 'Question1: Lorem ipsum dolor sit amet, consetetur sadipscing elitr')
        self.assertEqual(new_question.text,
                         'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.')
        self.assertEqual(Question.objects.count(), 2)
