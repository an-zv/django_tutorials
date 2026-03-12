from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase
import datetime
from django.urls import reverse
from django.utils import timezone

from polls.models import Question

class QuestionTestCase(TestCase):

    """It proved the exact limit of 24 hours for the was_published_recently() method"""
    def test_was_published_recently_edge(self):
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question.objects.create(question_text="Test Question", pub_date=time)
        self.assertIs(question.was_published_recently(), False)

    """It proved that the text of the question is correctly stored"""
    def test_question_text_length(self):
        question = Question.objects.create(question_text="Test Question", pub_date=timezone.now())
        self.assertEqual(len(question.question_text), len("Test Question"))

class QuestionSimpleTestCase(SimpleTestCase):

    """It proved that the upper() method of a string works correctly"""
    def test_text_uppercase(self):
        question_text = "hello world"
        self.assertEqual(question_text.upper(), "HELLO WORLD")

    """It proved that the reverse() function correctly generates the URL for the index view"""
    def test_url(self):
        url = reverse("polls:index")
        self.assertEqual(url, "/polls/")

    """It proved the same as the previous test but using args"""
    def test_url_with_args(self):
        url = reverse("polls:detail", args=[1])
        self.assertEqual(url, "/polls/1/")


class QuestionTransactionTestCase(TransactionTestCase):

    """It proved that the creation, storage and deletion of questions work correctly"""
    def test_create_question(self):
        Question.objects.create(question_text="Question1", pub_date=timezone.now())
        Question.objects.create(question_text="Question2", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 2)
        Question.objects.all().delete()
        self.assertEqual(Question.objects.count(), 0)

"""It proved that the page of polls loads correctly"""
class QuestionLiveServerTestCase(LiveServerTestCase):
    def test_polls_page(self):
        url = self.live_server_url + "/polls/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)