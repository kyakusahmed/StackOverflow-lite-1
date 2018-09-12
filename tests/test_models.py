from flask import json
from flask_testing import TestCase
from tests import app

from app.connect import DatabaseConnection
from app.models import (Answer, Question, User, valid_answer, valid_login_data,
                        valid_question, valid_signup_data, valid_username)

from .base import APITestCase, answersList, questionsList


class TestModels(APITestCase):

    def setUp(self):

        self.conn = DatabaseConnection()
        self.conn.create_Questions_table()
        self.conn.create_Answers_table()
        self.conn.create_Users_table()
        
        self.user1 = User('Peter', 'ptr@gmail.com','1234')
        self.user2 = User('Jane', 'jenn@gmail.com','1234')
        self.question1 = Question('computers', 'what is python ?')
        self.question1.author = self.user1.username
        self.question2 = Question('api', 'what is Flask ?')
        self.question2.author = self.user2.username
        self.answer1 = Answer('it is a programming language', 
                              self.question1.id)
        self.answer1.author = self.user1.username
        self.answer2 = Answer('it a microframework for building python apps', 
                              self.question2.id)
        self.answer2.author = self.user2.username

        def  insert_new_records(queries):
            for query in queries:
                self.conn.insert_new_record(query[0], query[1])
        
        self.queries = (('questions', self.question1.__repr__()), ('questions', self.question2.__repr__()),
                        ('answers', self.answer1.__repr__()), ('answers', self.answer2.__repr__()),
                        ('users', self.user1.__repr__()), ('users', self.user2.__repr__()))

        insert_new_records(self.queries)
        
        self.ansList = self.conn.query_all('answers')
        self.qnsList = self.conn.query_all('questions')
        self.usersList = self.conn.query_all('users')



    def tearDown(self):
        self.conn.drop_table('users')
        self.conn.drop_table('questions')
        self.conn.drop_table('answers')


    def test_answers_questions_have_uniqueIds(self):
        self.assertTrue(self.question1.id != self.question2.id)
        self.assertTrue(self.answer1.answerId != self.answer2.answerId)
        self.assertTrue(self.user1.id != self.user2.id)

    def test_question_answer_relationship(self):
        self.assertTrue(self.question1.id == self.answer1.Qn_Id)
        self.assertTrue(self.answer2.Qn_Id == self.question2.id)
        self.assertTrue(self.question1.author == self.user1.username)
        self.assertTrue(self.answer2.author == self.user2.username)


    def test_repr_turnsObject_into_dict(self):
        res1 = self.answer1.__repr__()
        res2 = self.question1.__repr__()
        res3 = self.user1.__repr__()
        self.assertTrue(type(res1) == dict)
        self.assertTrue(type(res2) == dict)
        self.assertTrue(type(res3) == dict)

    def test_recors_inserted_properly(self):
        if self.qnsList:
            for question in self.qnsList:
                self.assertEqual(5, len(question))
        self.assertEqual(2, len(self.qnsList))

        if self.ansList:
            for answer in self.ansList:
                self.assertEqual(6, len(answer))
        self.assertEqual(2, len(self.ansList))

        if self.usersList:
            for user in self.usersList:
                self.assertEqual(5, len(user))
        self.assertEqual(2, len(self.usersList))
    
    def test_user_can_query_db(self):
        question = Question('computer science', 'What is a program?')
        question.author = self.user1.username
        body = '''a program is a set of instructions 
                  given to a computer to perform certain tasks'''
        answer = Answer(body, question.id)
        answer.author = self.user2.username

        self.conn.insert_new_record('questions', question.__repr__())
        self.conn.insert_new_record('answers', answer.__repr__())
        ansL = [ans for ans in self.conn.query_all('answers') if int(ans[1])==question.id]

        qnsL = [qn for qn in self.conn.query_all('questions') if int(qn[4])==question.id]

        self.assertEqual(body, ansL[0][2])
        self.assertEqual(self.user2.username, ansL[0][4])
        self.assertEqual('computer science', qnsL[0][1])
        self.assertEqual('What is a program?', qnsL[0][2])
    
    def test_valid_question(self):
        data = {
            'topic': 'computers and tech',
            'body': 'What is the relevance of computers in technology!'
        }
        res = valid_question(data)
        self.assertEqual((True, ), res)
        data['topic'] = 'api'
        res = valid_question(data)
        value = (False, "Question topic already exists!")
        self.assertEqual(value, res)
        topic = data['topic']
        body = data['body']
        condition1 = topic == '  ' or topic == '' or topic == 1234
        condition2 = body == '  ' or body == '' or body == 1234
        if condition1 or condition2:
            res = valid_question(data)
            value = (False, {"hint_1":"Question topic or body should not be empty!",
                            "hint_2":"body and topic fileds should not consist entirely of integer-type data"})
            self.assertEqual(value, res)
        elif condition1 and condition2 :
            res = valid_question(data)
            value = (False, {"hint_1":"Question topic or body should not be empty!",
                            "hint_2":"body and topic fileds should not consist entirely of integer-type data"})
            self.assertEqual(value, res)
        else:
            data = {}
            res = valid_question(data)
            self.assertEqual((False, ), res)
    
    def test_valid_username(self):
        res = valid_username('Peter')
        self.assertTrue(res == False)
        res = valid_username('Kangol')
        self.assertTrue(res == True)

    def test_valid_answer(self):
        data ={
            'body': 'It is a scripting language',
        }
        res = valid_answer(data)
        self.assertTrue(res == (True, ))
        value = (False, {'hint_1': "Answer body should not be empty!",
                            'hint_2': """body and Qn_Id fileds should not contain
                            numbers only and string-type data respectively"""})
        if len(data['body']) == 0 or type(data['body']) == int:
            res = valid_answer(data)
            self.assertTrue(value == res)
        elif len(data['body']) == 0 and type(data['body']) == int:
            res = valid_answer(data)
            self.assertTrue(value == res)
        else:
            if data == {}:
                res = valid_answer(data)
                self.assertTrue((False, ) == res)

    def test_valid_signup_data(self):
        data = {
            'username': 'Kangol',
            'email': 'kangol@gmail.com',
            'password': '123e',
            'repeat_password': '123e'
        }
        res = valid_signup_data(data)
        self.assertTrue(res == True)
        del data['username']
        res = valid_signup_data(data)
        self.assertTrue(res == False)
        del data['email']
        res = valid_signup_data(data)
        self.assertTrue(res == False)
        del data['password']
        res = valid_signup_data(data)
        self.assertTrue(res == False)
        del data['repeat_password']
        res = valid_signup_data(data)
        self.assertTrue(res == False)
    
    def test_valid_login_data(self):
        data = {
            'username': 'Tom Peter',
            'password': 1234
        }
        res = valid_login_data(data)
        self.assertTrue(res == True)
        del data['username']
        res = valid_login_data(data)
        self.assertTrue(res == False)
        del data['password']
        res = valid_login_data(data)
        res = valid_login_data(data)
        self.assertTrue(res == False)