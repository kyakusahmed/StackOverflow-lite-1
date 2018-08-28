from datetime import datetime, timedelta

import bcrypt
from flask import Flask, Response, json, jsonify, request, url_for
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from app import app
from app.models import Answer, Question, User
from connect import conn


@app.route('/')
def show_api_works():
    return jsonify({'Welcome to my app': [{'message': "endpoints work"}]})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify({'message': 'JSON missing in request!'}), 400

    username = request.args.get('username', None)
    password = request.args.get('password', None)

    if not username:
        return jsonify({
            'message': 'Required parameter: username missing!'
        }), 400
    elif not password:
        return jsonify({
            'message': 'Required parameter: password missing!'
        }), 400

    users = conn.query_all('users')
    user = [user for user in users if user[1]
            == username and user[3]
            == bcrypt.hashpw(password.encode('utf8'), user[3])]
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(
        identity=username,
        fresh=timedelta(minutes=30)
    )
    msg = {'access_token': f'{access_token}'}

    return jsonify({f'access token created for user {username}': msg}), 200


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({'message': 'JSON missing in request!'}), 400

    username = request.args.get('username', None).split()
    email = request.args.get('email', None)
    password = request.args.get('password', None)
    repeat_password = request.args.get('repeat_password', None)

    if not username:
        return jsonify({
            'message': 'Required parameter: username missing!'
        }), 400
    elif not email:
        return jsonify({'message': 'Required parameter: email missing!'}), 400
    elif not password:
        return jsonify({'message': 'Required parameter: email missing!'}), 400
    else:
        if not repeat_password:
            msg = 'Required parameter: repeat_password missing!'
            return jsonify({'message': f'{msg}'}), 400
    users = conn.query_all('users')
    print(users)
    if len(username) > 1:
        username_ = username[0] + " " + username[1]
        print(username_)
    username = username[0]
    if valid_username(username):

        if repeat_password == password:
            user = User(username, email, password)
            conn.insert_new_record('users', user.__repr__())
            return jsonify({
                'success': f"{username}'s account created succesfully"
            }), 200

        return jsonify({
            'message': 'Password does not match repeat_password'
        }), 401
    return jsonify({'message': f'username {username} already taken!'}), 401


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    questionsList = conn.query_all('questions')
    if questionsList:
        return jsonify({'questions': questionsList}), 200
    return jsonify({'message': 'No Questions added yet'}), 404


@app.route('/api/v1/questions/<int:questionId>', methods=['GET'])
def get_question(questionId):
    questionsList = conn.query_all('questions')
    if questionsList:
        for question in questionsList:
            if question[3] == questionId:
                temp = {
                    'questionId': question[3],
                    'topic': question[1],
                    'body': question[2]
                }
                return jsonify(temp), 200
        return Response(json.dumps(['Question not Found']),
                        status=404, mimetype='application/json')
    return jsonify({f'Question {questionId}': 'Has not been added yet'}), 404


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    answersList = conn.query_all('answers')
    if answersList:
        return jsonify({'answers': answersList}), 200
    return jsonify({'message': 'No Answers added yet'}), 404


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>',
           methods=['GET'])
def get_answer(questionId, answerId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    if questionsList:
        if answersList:
            for answer in answersList:
                if answer[3] == answerId:
                    temp = {
                        'answerId': answer[3],
                        'Qn_Id': answer[1],
                        'body': answer[2]
                    }
                    return jsonify(temp), 200
            return Response(json.dumps(['Answer not Found']),
                            status=404, mimetype='application/json')
    return jsonify({
        f'Answer{answerId} for Question{questionId}': 'Has not been added yet'
    }), 404


@app.route('/api/v1/questions', methods=['POST'])
@jwt_required
def add_question():

    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        if (valid_question(request_data)):
            temp = {
                'topic': request_data['topic'],
                'body': request_data['body']
            }
            if len(temp['topic'])!= 0 and len(temp['body'])!=0:
                question = Question(temp['topic'], temp['body'])
                id = question.id
                temp['questionId'] = id
                conn.insert_new_record('questions', temp)

                return jsonify({
                    'msg': f'Question {id} posted successfully',
                    'Posted by': f'{current_user}'
                }), 201
            return jsonify({'msg': 'topic and body fields should not be empty'})

        else:
            bad_object = {
                "error": "Invalid question object",
                "hint": '''Request format should be,{'topic': 'python',
                    'body': 'what is python in programming' }'''
            }
            response = Response(json.dumps([bad_object]),
                                status=400, mimetype='application/json')
            return response
    return jsonify({
        'message': 'To post a question, you need to be logged in',
        'info': 'Signup or login, to get acces_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['POST'])
@jwt_required
def add_answer(questionId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList:

            if (valid_answer(request_data)):

                temp = {
                    'Qn_Id': request_data['Qn_Id'],
                    'body': request_data['body']
                }
                if len(temp['Qn_Id'])!=0 and len(temp['body'])!=0:
                    answer = Answer(temp['body'], temp['Qn_Id'])
                    id = answer.answerId
                    temp['answerId'] = id
                    conn.insert_new_record('answers', temp)

                    return jsonify({
                        'msg': f'Answer {id} posted successfully'
                    }), 201
                return jsonify({'msg': 'body and Qn_Id fields should not be empty'})
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
                        f'Question {questionId} does not exist.'}), 404

    return jsonify({
        'message': 'To post an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
@jwt_required
def update_question(questionId, topic, body, question_id):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList:
            updated_question = dict()
            ids = [question[3] for question in questionsList]

            if questionId in ids:
                if "topic" in request_data:
                    updated_question["topic"] = request_data["topic"]
                if "body" in request_data:
                    updated_question["body"] = request_data["topic"]
                if len(updated_question['topic'])!=0 and len(updated_question['body'])!=0:
                    for question in questionsList:
                        if question["questionId"] == questionId:
                            conn.update_entry(
                                'questions',
                                topic,
                                updated_question['topic'],
                                question_id,
                                questionId
                            )
                            conn.update_entry(
                                'questions',
                                body,
                                updated_question['body'],
                                question_id,
                                questionId
                            )
                    return jsonify({'msg': f'Question {questionId} updated successfully.'}), 204
                return jsonify({'msg': 'body and topic fields should not be empty'})
                
        response = Response(json.dumps(['Question not found']), status=404)
        return response

    return jsonify({
        'message': 'To update a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    })


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId, question_id):
    current_user = get_jwt_identity()
    if current_user:
        questionsList = conn.query_all('questions')
        if questionsList:
            ids = [question[3] for question in questionsList]
            if questionId in ids:
                for question in questionsList:
                    if questionId == question[3]:
                        questionsList.remove(question)
                        conn.delete_entry('questions', question_id, questionId)
                response = Response(
                    '', status=200, mimetype='application/json')
                return response
        response = Response(json.dumps(['Question not found']),
                            status=404, mimetype='application/json')
        return response
    return jsonify({
        'message': 'To delete a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


def valid_username(username):
    users = conn.query_all('users')
    if len(users) != 0:
        for user in users:
            existing_user = [user[1]
                             for user in users if user[1] == username]
            if not existing_user:
                return True
    elif len(users) == 0:
        return True
    return False


def valid_question(questionObject):
    if 'topic' in questionObject and 'body' in questionObject:
        questionsList = conn.query_all('questions')
        for question in questionsList:
            if question['topic'] != questionObject['topic']:
                    return True
    else:
        return False


def valid_answer(answerObject):
    if 'Qn_Id' in answerObject and 'body' in answerObject:
        return True
    else:
        return False
