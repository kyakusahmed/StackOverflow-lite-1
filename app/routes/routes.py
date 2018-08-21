from flask import (Flask, Response, flash, json, jsonify, request, session, url_for)

from app import app
from app.models import Answer, Question, answersList, questionsList


@app.route('/api/v1/questions', methods=['GET'])
def get_questions():
    return jsonify({'questions': questionsList})

