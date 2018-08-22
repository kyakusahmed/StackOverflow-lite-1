
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

