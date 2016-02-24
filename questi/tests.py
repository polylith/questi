from django.test import TestCase
from questi.models import Question
# Create your tests here.
class ForumTest(TestCase):
    def setUp(self):
        Question.objects.create(title="Test Question")

    def test_questi_list(self):
        question = Question.objects.get(pk=1)
        self.assertIsNotNone(question)