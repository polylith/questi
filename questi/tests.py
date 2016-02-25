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
        self.assertEqual(self.question.get_rate(),1)


    def test_questi_authentication(self):
        test_user = User.objects.get(pk=1)
        self.client.post('/admin/', {'username': 'test', 'password1': 'passw0rd'})
        assert test_user.is_authenticated()

