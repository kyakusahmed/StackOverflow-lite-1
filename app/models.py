import uuid

import bcrypt
from werkzeug.security import generate_password_hash


class Question:
    def __init__(self, topic, body):
        self.id = uuid.uuid4().int
        self.topic = str(topic).strip()
        self.body = str(body).strip()

    def __repr__(self):
        return {
            'topic': self.topic,
            'body': self.body,
            'questionId': self.id
        }


class Answer:
    def __init__(self, body, Qn_Id, pref=False):
        self.answerId = uuid.uuid4().int
        self.body = str(body).strip()
        self.Qn_Id = Qn_Id
        self.prefered = pref

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body,
            'prefered': self.prefered
        }

    def prefer_answer(self):
        self.prefered = True


class User:
    def __init__(self, username, email, password):
        self.salt = bcrypt.gensalt()
        self.id = uuid.uuid4().int
        self.username = str(username).strip()
        self.email = str(email).strip()
        self.password_hash = generate_password_hash(password)
    
    def __repr__(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password_hash,
            'user_id': self.id
        }
