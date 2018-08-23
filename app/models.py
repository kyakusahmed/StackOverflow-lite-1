class Question:
    def __init__(self, questionId=0, topic='', body=''):
        self.id = questionId
        self.topic = topic
        self.body = body
        self.answers = []

    def __repr__(self):
        return {
            'questionId': self.id,
            'topic': self.topic,
            'body': self.body
        }


class Answer:
    def __init__(self, answerId=0, body='', Qn_Id=0):
        self.answerId = answerId
        self.body = body
        self.Qn_Id = Qn_Id

    def __repr__(self):
        return {
            'answerId': self.answerId,
            'Qn_Id': self.Qn_Id,
            'body': self.body
        }
        
questionsList = []
answersList = []
