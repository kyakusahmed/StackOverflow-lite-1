import unittest

from flask import current_app
from flask_testing import TestCase

from app import app
from app.routes import routes
from app.models import Answer, Question
from config import Config


class APITestCase(TestCase):
    def create_app(self):
        app.config['DEBUG'] = True
        return app

    def setUp(self):
        self.app = app.test_client()
        self.answersList = createAnsList()
        self.questionsList = createQnsList()
        
    def tearDown(self):
        pass

    def post_question(self):
        pass





ans_List = [

    {
        'answerId': 1,
        'Qn_Id': 1,
        'body': ""},
    {'answerId': 2,
        'Qn_Id': 2,
        'body': ""},
    {'answerId': 3,
        'Qn_Id': 3,
        'body': ""},
    {'answerId': 4,
        'Qn_Id': 4,
        'body': ""}
]


def createQnsList():
    '''Generates a List of five questions with different topics
    and links answers to them'''

    QnsList = []
    body = ""

    topics = [0, '', '', '', '', '']

    for i in range(1, 6):
        Qn = Question(i, topics[i], body)

        for answer in ans_List:
            if answer['Qn_Id'] == Qn.id:
                Qn.answers.append(answer)

        QnsList.append(Qn.__repr__())
    return QnsList
    
questionsList = createQnsList()


def createAnsList():
    '''Generates list of five answers'''
    AnsList = []
    body = ""

    l = [question['questionId'] for question in questionsList]
    qnIds = [id for id in l]
    qnIds[:0] = [0]

    for i in range(1, 6):
        Ans = Answer(i, body, qnIds[i])
        AnsList.append(Ans.__repr__())
    return AnsList

answersList = createAnsList()

