import uuid

import bcrypt


class Question:
    def __init__(self, topic, body):
        self.id = uuid.uuid4().int
        self.topic = topic.strip()
        self.body = body.strip()

    def __repr__(self):
        return {
            'topic': self.topic,
            'body': self.body,
            'questionId': self.id
        }


class Answer:
    def __init__(self, body, Qn_Id, pref=False):
        self.answerId = uuid.uuid4().int
        self.body = body.strip()
        self.Qn_Id = Qn_Id
        self.prefered = pref

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body,
            'prefered': self.prefered
        }

    def prefer_answer(self, answer):
        answer.prefered = True


class User:
    def __init__(self, username, email, password):
        self.salt = bcrypt.gensalt()
        self.id = uuid.uuid4().int
        self.username = username.strip()
        self.email = email.strip()
        self.password_hash = bcrypt.hashpw(password.encode('utf8'), self.salt)
    
    def __repr__(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password_hash,
            'user_id': self.id
        }



