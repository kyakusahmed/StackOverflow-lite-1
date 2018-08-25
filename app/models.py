import uuid


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
    def __init__(self, body, Qn_Id):
        self.answerId = uuid.uuid4().int
        self.body = body.strip()
        self.Qn_Id = Qn_Id

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body
        }
        
questionsList = []
answersList = []
