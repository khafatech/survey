#!/usr/bin/python2

import json

from flask import Flask, Response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import db
import models

app = Flask(__name__)
app.secret_key = 'supersecret'


class QuestionView(ModelView):
    # edit child models inline
    inline_models = (models.QuestionStat, )


class StatView(ModelView):
    form_excluded_columns = ['stats']


admin = Admin(app, name='Manage Questions', template_mode='bootstrap3')
admin.add_view(QuestionView(models.Question, models.session, name='Questions'))
admin.add_view(StatView(models.Stat, models.session, name='Edit stats/tokens'))


def json_response(obj):
    return Response(json.dumps(obj), mimetype='application/json')

@app.route('/')
def index():
    questions = db.get_questions(0, 10)
    return json_response(questions)


@app.route('/questions/<int:question_id>')
def get_question(question_id):
    question = db.get_questions(question_id)
    return str(question)


@app.route('/stats')
def stats():
    stats = db.get_stats()
    return str(stats)



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
