#!/usr/bin/python2

import json
import logging

from flask import Flask, Response, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import db
import models

app = Flask(__name__)
app.secret_key = 'supersecret'
logging.basicConfig(level=logging.INFO)



# For the admin page

class QuestionView(ModelView):
    # edit child models inline
    inline_models = (models.QuestionStat, )


class StatView(ModelView):
    form_excluded_columns = ['stats']


admin = Admin(app, name='Manage Questions', template_mode='bootstrap3')
admin.add_view(QuestionView(models.Question, models.session, name='Questions'))
admin.add_view(StatView(models.Stat, models.session, name='Edit stats/tokens'))



@app.route('/')
def index():
    return render_template('ask.html')


@app.route('/questions')
def questions():

    questions = db.get_questions(0, 10)
    return json_response(questions)


@app.route('/questions/<int:question_id>')
def get_question(question_id):
    question = db.get_questions(question_id)
    if question:
        question = question[0]
    return json_response(question)


@app.route('/questions/<int:question_id>/<answer>')
def answer_question(question_id, answer):
	logging.info("answering %s: %s" % (question_id, answer))

	try:
		db.answer_question(question_id, answer)
	except:
		return ("Error", 400, [])
	return "OK"


@app.route('/stats')
def stats():
    stats = db.get_stats()
    return json_response(stats)


def json_response(obj):
    return Response(json.dumps(obj), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
