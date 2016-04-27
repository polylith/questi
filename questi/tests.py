from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from questi.models import Question, Vote, Answer


# Create your tests here.
class ForumTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.de', 'passw0rd')
        self.user2 = User.objects.create_user('test2', 'test@test.de', 'passw0rd2')
        self.question = Question.objects.create(title="Test Question", user=self.user)

    def test_questi_list(self):
        question = Question.objects.get(pk=1)
        self.assertIsNotNone(question)

    def test_questi_vote_up(self):
        test_user = User.objects.get(pk=1)
        self.client.login(username='test', password='passw0rd')
        self.assertEqual(self.question.vote_set.count(), 0)
        self.assertEqual(self.question.get_rate(), 0)
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

    def test_questi_question_double_up_vote(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_up/')
        self.assertEqual(self.question.vote_set.count(), 1)
        self.client.post('/question/1/vote_up/')
        self.assertEqual(self.question.vote_set.count(), 0)

    def test_questi_question_double_down_vote(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_down/')
        self.assertEqual(self.question.vote_set.count(), 1)
        self.client.post('/question/1/vote_down/')
        self.assertEqual(self.question.vote_set.count(), 0)

    def test_questi_up_vote_down_vote_question(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_up/')
        self.assertEqual(self.question.vote_set.count(), 1)
        self.client.post('/question/1/vote_down/')
        self.assertEqual(self.question.get_rate(), -1)

    def test_questi_down_vote_up_vote_question(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_down/')
        self.assertEqual(self.question.vote_set.count(), 1)
        self.client.post('/question/1/vote_up/')
        self.assertEqual(self.question.get_rate(), 1)

    def test_questi_delete_question(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/vote_down/')
        self.assertEqual(Vote.objects.count(), 1)
        self.question.delete()
        self.assertEqual(Vote.objects.count(), 0)

    def test_questi_post_to_question_detail_view(self):
        self.client.login(username='test', password='passw0rd')
        self.client.get('/question/1/')
        self.client.post('/question/1/')

    def test_questi_add_answer_to_question(self):
        self.client.login(username='test2', password='passw0rd2')
        self.client.post('/question/1/', {'text': 'Thats a good question.'})
        test_answer = Answer(text='Thats a good question.')
        self.assertEqual(Question.objects.get(pk=1).answer_set.first().text, test_answer.text)

    def test_questi_edit_question_from_other_user(self):
        self.client.login(username='test', password='passw0rd')
        self.client.post('/question/1/edit/', {'text': 'New Text for Question 1 looks awesome.',
                                               'title': 'Changed Title of Question'})
        self.assertEqual(Question.objects.get(pk=1).title, 'New Text for Question 1 looks awesome.')

    def test_questi_edit_question_from_other_user(self):
        self.client.login(username='test2', password='passw0rd2')
        question_befor_edit = Question.objects.get(pk=1)
        self.client.post('/question/1/edit/', {'text': 'New Text for Question 1 looks awesome.',
                                               'title': 'Changed Title of Question'})
        self.assertNotEqual(Question.objects.get(pk=1).title, 'New Text for Question 1 looks awesome.')
