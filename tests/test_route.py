from flask import json, url_for
from tests import app

from .base import APITestCase, questionsList


class TestRoutes(APITestCase):

    def test_root_route(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    # def test_user_can_login(self):
    #     res = self.client.post(url_for('login'))
    #     self.assertEqual(res.status_code, 400)

    def test_user_can_get_questions(self):
        with self.client:
            res = self.client.get('/api/v1/questions')
            self.assertEqual(res.status_code, 404)

    def test_user_can_get_question(self):
        res = self.client.get('/api/v1/questions/2')
        self.assertEqual(res.status_code, 404)

    def test_user_can_get_answers(self):
        res = self.client.get('/api/v1/questions/2/answers')
        self.assertEqual(res.status_code, 404)

    def test_user_can_get_answer(self):
        res = self.client.get('/api/v1/questions/2/answers/3')
        self.assertEqual(res.status_code, 404)

    def test_user_can_post_question(self):
        question = {
            "questionId": 34,
            "topic": "computer science",
            "body": "what is software?"
        }
        res = self.client.post('/api/v1/questions', json=question)
        self.assertEqual(res.status_code, 401)

    def test_user_post_answer(self):
        answer = {
            "answerId": 34,
            "body": "what is software?",
            "Qn_Id": 2
        }
        res = self.client.post('/api/v1/questions/4/answers', json=answer)
        self.assertEqual(res.status_code, 401)

    def test_user_can_update_question(self):

        new_question = {
            "topic": "computer science",
            "body": "what is software?"
        }
        res = self.client.patch('/api/v1/questions/4', json=new_question)
        self.assertEqual(res.status_code, 401)

    def test_user_can_delete_question(self):
        res = self.client.delete('/api/v1/questions/5')
        self.assertEqual(res.status_code, 401)
