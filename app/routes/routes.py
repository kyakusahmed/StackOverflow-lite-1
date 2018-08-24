from flask import (Flask, Response, flash, json, jsonify, request, session,
                   url_for)

from app import app
from app.models import Answer, Question, answersList, questionsList


@app.route('/')
def show_api_works():
    return jsonify({'Welcome to my app': [{'message': "endpoints work"}]})


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    if questionsList:
        return jsonify({'questions': questionsList})
    return jsonify({'message': 'No Questions added yet'})

@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    if questionsList:
        for question in questionsList:
            if question['questionId'] == questionId:
                temp = {
                    'questionId': question['questionId'],
                    'topic': question['topic'],
                    'body': question['body']
                }
                return jsonify(temp)
        return Response(json.dumps(['Question not Found']), 
                        status=404, mimetype='application/json')
    return jsonify({f'Question {questionId}': 'Has not been added yet'})


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    if answersList:
        return jsonify({'answers': answersList})
    return jsonify({'message': 'No Answers added yet'})


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['GET'])
def get_answer(questionId, answerId):
    if questionsList:
        if answersList:
            for answer in answersList:
                if answer['answerId'] == answerId:
                    temp = {
                        'answerId': answer['answerId'],
                        'Qn_Id': answer['Qn_Id'],
                        'body': answer['body']
                    }
                    return jsonify(temp)
            return Response(json.dumps(['Answer not Found']), 
                            status=404, mimetype='application/json')
    return jsonify({f'Answer{answerId} for Question{questionId}': 'Has not been added yet'})


@app.route('/api/v1/questions', methods=['POST'])
def add_question():

    request_data = request.get_json()
    if (valid_question(request_data)):
        temp = {
            'topic': request_data['topic'],
            'body': request_data['body']
        }
        question = Question(temp['topic'], temp['body'])
        id = question.id
        temp['questionId'] = id
        questionsList.append(temp)
        
        return jsonify({'msg': f'Question {id} posted successfully'})
    else:
        bad_object = {
            "error": "Invalid question object",
            "hint": '''Request format should be,{'topic': 'python',
                'body': 'what is python in programming' }'''
        }
        response = Response(json.dumps([bad_object]), 
                            status=400, mimetype='application/json')
        return response

@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
def add_answer(questionId):
    request_data = request.get_json()
    if questionsList:
    
        if (valid_answer(request_data)):
            print(request_data)
            temp = {
                'Qn_Id': request_data['Qn_Id'],
                'body': request_data['body']
            }
            answer = Answer(temp['body'], temp['Qn_Id'])
            id = answer.answerId
            temp['answerId'] = id
            answersList.append(temp)
            return jsonify({'msg': f'Answer {id} posted successfully'})
    
        else:
                bad_object = {
                    "error": "Invalid answer object",
                    "hint": '''Request format should be { 
                    'body': 'this is the body',
                        'Qn_Id': 2}'''
                }
                response = Response(json.dumps([bad_object]), 
                                    status=400, mimetype='application/json')
                return response
    return jsonify({f'Attempt to answer Question {questionId}': 
                    f'Question {questionId} does not exist.'})


@app.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
def update_question(questionId):
    request_data = request.get_json()
    if questionsList:
        updated_question = dict()
        ids = [question['questionId'] for question in questionsList]
        
        if questionId in ids:
            if "topic" in request_data:
                updated_question["topic"] = request_data["topic"]
            if "body" in request_data:
                updated_question["body"] = request_data["topic"]
        
            for question in questionsList:
                if question["questionId"] == questionId:
                    question.update(updated_question)

            response = Response('', status=204)
            response.headers['Location'] = "/questions" + str(questionId)
            return response
    response = Response(json.dumps(['Question not found']), status=404)
    return response


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
def delete_question(questionId):
    if questionsList:
        ids = [question['questionId'] for question in questionsList]
        if questionId in ids:
            for question in questionsList:
                if questionId == question['questionId']:
                    questionsList.remove(question)
            response = Response('', status=200, mimetype='application/json')
            return response
    response = Response(json.dumps(['Question not found']), 
                        status=404, mimetype='application/json')
    return response
        

def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        if questionsList:
            for question in questionsList:
                if question['body'] != questionObject['body']:
                    return True
        return True
    else:
        return False

def valid_answer(answerObject):
    if 'Qn_Id' in answerObject and 'body' in answerObject:
        if answersList:
            for answer in answersList:
                if answer['body'] != answerObject['body']:
                    return True
        return True
    else:
        return False
