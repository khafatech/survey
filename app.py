#!/usr/bin/python2

from flask import Flask
import db

app = Flask(__name__)



@app.route('/')
def index():
    questions = db.get_questions(0, 10)
    return str(questions)

@app.route('/questions/<int:question_id>')
def get_question(question_id):
    question = db.get_questions(question_id)
    return str(question)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
