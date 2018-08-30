from datetime import datetime, timedelta

import bcrypt
from flask import Flask, Response, json, jsonify, request, url_for
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from werkzeug.security import check_password_hash
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
    user = [user for user in users if check_password_hash(user[3], password) and user[1] == username]
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(
        identity=username,
        fresh=timedelta(minutes=60)
    )
    msg = {'access_token': f'{access_token}'}

    return jsonify({f'access token created for user {username}': msg}), 200


@app.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({'message': 'JSON missing in request!'}), 400

    username = str(request.args.get('username', None)).split()
    email = request.args.get('email', None)
    password = request.args.get('password', None)
    repeat_password = request.args.get('repeat_password', None)

    if not username:
        return jsonify({
            'message': 'Required parameter: username missing!'
        }), 400
    else:
        if not repeat_password:
            msg = 'Required parameter: repeat_password missing!'
            return jsonify({'message': f'{msg}'}), 400
    
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


        if username:
            if len(username) > 1:
                username_ = username[0] + " " + username[1]
                username = username_
                if not valid_username(username):
                    return jsonify({'message': f'username {username} already taken!'}), 401
            elif len(username) == 1:
                username = username[0]
                if not valid_username(username):
                    return jsonify({'message': f'username {username} already taken!'}), 401
            if not email:
                return jsonify({'message': 'Required parameter: email missing!'}), 400
            elif not password:
                return jsonify({'message': 'Required parameter: password missing!'}), 400
            else:
                if not repeat_password:
                    msg = 'Required parameter: repeat_password missing!'
                    return jsonify({'message': f'{msg}'}), 400

            if repeat_password == password:
                user = User(username, email, password)
                conn.insert_new_record('users', user.__repr__())
                return jsonify({
                    'success': f"{username}'s account created succesfully"
                }), 200
            else:
                if repeat_password != password:
                    return jsonify({
                        'message': 'Password does not match repeat_password'
                    }), 401


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
            if int(question[3]) == questionId:
                temp = {
                    'questionId': question[3],
                    'topic': question[1],
                    'body': question[2]
                }
                return jsonify(temp), 200
        return Response(json.dumps(['Question not Found']),
                        status=404, mimetype='application/json')
    return jsonify({f'Question {questionId}': 'Has not been added yet'}), 200


@app.route('/api/v1/questions/<int:questionId>/answers', methods=['GET'])
def get_answers(questionId):
    answersList = conn.query_all('answers')
    if answersList:
        for answer in answersList:
            if int(answer[1]) == questionId:
                return jsonify({'answers': answersList}), 200
    return jsonify({'message': f'No Answers added yet for question {questionId}'}), 404


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>',
           methods=['GET'])
def get_answer(questionId, answerId):
    questionsList = conn.query_all('questions')
    answersList = conn.query_all('answers')
    if questionsList:
        if answersList:
            for answer in answersList:
                if int(answer[3]) == answerId:
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
        print(request_data)

        duplicate_check = valid_question(request_data)
        print(duplicate_check)
        
        if duplicate_check[0]:
            temp = {
                'topic': request_data['topic'],
                'body': request_data['body']
            }

            question = Question(temp['topic'], temp['body'])
            id = question.id
            temp['questionId'] = id
            conn.insert_new_record('questions', question.__repr__())

            return jsonify({
                'msg': f'Question {id} posted successfully',
                'Posted by': f'{current_user}'
            }), 201

        else:
            if not duplicate_check[0] and len(duplicate_check) > 1:
                reason = duplicate_check[1]
                return jsonify({"error": f"{reason}"})
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
            answer_check = valid_answer(request_data)
            ids = [int(qn[3]) for qn in questionsList]
            if answer_check[0] and request_data['Qn_Id'] in ids:
                temp = {
                    'Qn_Id': request_data['Qn_Id'],
                    'body': request_data['body']
                }
                answer = Answer(temp['body'], temp['Qn_Id'])
                id = answer.answerId
                temp['answerId'] = id
                conn.insert_new_record('answers', answer.__repr__())

                return jsonify({
                    'msg': f'Answer {id} posted successfully'
                }), 201
            # return jsonify({'msg': 'body and Qn_Id fields should not be empty'})
            else:

                if not answer_check[0] and len(answer_check) > 1:
                    reason = answer_check[1]
                    return jsonify({"error": f"{reason}"})
                else:
                    bad_object = {
                        "error": "Invalid answer object",
                        "hint": '''Request format should be {
                            'body': 'this is the body',
                                'Qn_Id': 2}''',
                        "hint2": f"Qn_Id should correspond with {questionId}"
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


@app.route('/api/v1/questions/<int:questionId>/answers/<int:answerId>', methods=['PUT'])
@jwt_required
def select_answer_as_preferred(questionId, answerId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')

        if questionsList:
            answer_check = valid_answer(request_data)
            ids = [int(qn[3]) for qn in questionsList]
            if answer_check[0] and request_data['Qn_Id'] in ids:
        
                conn.update_answer(str(answerId))

                return jsonify({
                    'msg': f"Answer {answerId} marked as preferred"
                }), 201
            # return jsonify({'msg': 'body and Qn_Id fields should not be empty'})
            else:

                if not answer_check[0] and len(answer_check) > 1:
                    reason = answer_check[1]
                    return jsonify({"error": f"{reason}"})
                else:
                    bad_object = {
                        "error": "Invalid answer object",
                        "hint": '''Request format should be {
                            'body': 'this is the body',
                                'Qn_Id': 2}''',
                        "hint2": f"Qn_Id should correspond with {questionId}"
                    }
                    response = Response(json.dumps([bad_object]),
                                            status=400, mimetype='application/json')
                    return response
        return jsonify({f'Attempt to select answer to Question {questionId} as prefered':
                        f'Question {questionId} does not exist.'}), 404

    return jsonify({
        'message': 'To post an answer, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    }), 401


@app.route('/api/v1/questions/<int:questionId>', methods=['PATCH'])
@jwt_required
def update_question(questionId):
    current_user = get_jwt_identity()
    if current_user:
        request_data = request.get_json()
        questionsList = conn.query_all('questions')
        if questionsList:
            updated_question = dict()
            ids = [int(question[3]) for question in questionsList]
            print(ids)
            if questionId in ids:
                if "topic" in request_data:
                    updated_question["topic"] = request_data["topic"]
                if "body" in request_data:
                    updated_question["body"] = request_data["body"]
                if len(updated_question['topic'])!=0 and len(updated_question['body'])!=0:
                    for question in questionsList:
                        if int(question[3]) == questionId:
                            print(type(question[1]))
                            conn.update_question(updated_question['topic'], updated_question['body'], str(questionId))
                            return jsonify({'msg': f'Question {questionId} updated successfully.'}), 200
                return jsonify({
                    'msg': 'body and topic fields should not be empty'})
                
        response = Response(json.dumps(['Question not found']), status=404)
        return response

    return jsonify({
        'message': 'To update a question, you need to be logged in',
        'info': 'Signup or login, to get access_token'
    })


@app.route('/api/v1/questions/<int:questionId>', methods=['DELETE'])
@jwt_required
def delete_question(questionId):
    current_user = get_jwt_identity()
    if current_user:
        questionsList = conn.query_all('questions')
        if questionsList:
            ids = [int(question[3]) for question in questionsList]
            if questionId in ids:
                print('yeah')
                for question in questionsList:
                    if questionId == int(question[3]):
                        questionsList.remove(question)
                        conn.delete_entry('questions', str(questionId))
                        message = {'success': f"Question {questionId} deleted successfully!"}
                        response = Response(
                            json.dumps(message), status=202, mimetype='application/json')
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
    if 'topic' in questionObject.keys() and 'body' in questionObject.keys():
        questionsList = conn.query_all('questions')
        input_topic = questionObject['topic']
        input_body = questionObject['body']
        empty_field = len(str(input_topic).strip()) and len(str(input_body).strip()) == 0
        check_type = type(input_topic) == int or type(input_body) == int
        print(check_type)
        if empty_field or check_type:
                    value = (False, {"hint_1":"Question topic or body should not be empty!",
                                    "hint_2":"body and topic fileds should not consist entirely of integer-type data"}
                        )
                    return value
        if questionsList:
            topics = [question[1] for question in questionsList if question[1] == input_topic]

            if len(topics) != 0:
                value = (False, "Question topic already exists!")
                return value             
            else:
                if len(topics) == 0:
                    return (True, )
    else:
        if 'topic' or 'body' not in questionObject.keys():
            return (False, )
 

def valid_answer(answerObject):
    if 'Qn_Id' in answerObject.keys() and 'body' in answerObject.keys():
        input_QnId = answerObject['Qn_Id']
        input_body = answerObject['body']
        empty_field = len(str(input_QnId)) and len(input_body.strip()) == 0
        check_type = type(input_QnId) == str or type(input_body) == int
        if empty_field or check_type:
            return (False, {'hint': "Answer body should not be empty!",
                            'hint2': "body and topic fileds should not contain numbers only and string-type data respectively"}
                )
        return (True, )
    else:
        return (False, )

@app.errorhandler(500)
def internal_sserver_error(e):
    msg = "Sorry,we are experiencing some technical difficulties"
    msg2 = "Please report this to cedriclusiba@gmail.com and check back with us soon"
    return jsonify({'error': msg, "hint": msg2}), 500

@app.errorhandler(404)
def url_unknown(e):
    return jsonify({"error": "Sorry, resource you are looking for does not exist"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': "Sorry, this action is not supported for this url"}), 405

@app.errorhandler(403)
def forbidden_resource(e):
    return jsonify({'error': "Sorry, resource you are trying to access is forbidden"}), 403

@app.errorhandler(410)
def deleted_resource(e):
    return jsonify({'error': "Sorry, this resource was deleted"}), 410