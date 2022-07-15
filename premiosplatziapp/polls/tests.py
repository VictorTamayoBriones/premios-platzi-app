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


def createQuestion(question_text, days):
    """
    create a Question with the given "Question text"
    and published te given number of days offet to now (negative for question published in the past
    positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTest(TestCase):

    def test_no_question(self):
        """if no question exist , an aporpiate message is displayed"""

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_future_question(self):
        """
            No public questions del futuri
        """
        createQuestion("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
    

    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page
        """

        question = createQuestion("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        pas_question = createQuestion(question_text="past question", days=-30)
        future_question = createQuestion(question_text="future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuersetEqual(
            response.context["latest_question_list"],
            [pas_question]
        )


    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        """
        past_question1 = createQuestion(question_text="past question 1", days=-30)
        past_question2 = createQuestion(question_text="past question 2", days=-60)

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )