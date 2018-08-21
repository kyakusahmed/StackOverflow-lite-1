from flask import (Flask, Response, flash, json, jsonify, request, session, url_for)

from app import app
from app.models import Answer, Question, answersList, questionsList


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions': questionsList})

@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    for question in questionsList:
        if question['questionId'] == questionId:
            temp = {
                'questionId': question['questionId'],
                'topic': question['topic'],
                'body': question['body']
            }
            return jsonify(temp)
    return Response(json.dumps(['Question not Found']), status=404, mimetype='application/json')
