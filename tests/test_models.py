from flask import json
from tests import app

from app.models import Answer, Question

from .base import APITestCase, answersList, questionsList


class TestModels(APITestCase):

    def setUp(self):
        self.question1 = Question('computers', 'what is python ?')
        self.answer1 = Answer('it is a programming language', 1)
        answersList.append(self.answer1.__repr__())

    def test_answerList_created_properly(self):
        self.assertEqual(6, len(answersList))
        for answer in answersList:
            self.assertIn('answerId', answer)
            self.assertIn('body', answer)
            self.assertIn('Qn_Id', answer)

    def test_questionsList_created_properly(self):
        self.assertEqual(5, len(questionsList))
        for question in questionsList:
            self.assertIn('questionId', question)
            self.assertIn('topic', question)
            self.assertIn('body', question)
        

    def test_repr_turnsObject_into_dict(self):
        res1 = self.answer1.__repr__()
        res2 = self.question1.__repr__()
        self.assertTrue(type(res1))
        self.assertTrue(type(res2))
