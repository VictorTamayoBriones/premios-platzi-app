import datetime
from django.urls import reverse

from django.utils import timezone
from django.test import TestCase

from polls.models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿cual course director is the best?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    
class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        """if no question exist , an aporpiate message is displayed"""

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])