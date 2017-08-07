
import sqlite3

from flask import g


schema="""
CREATE TABLE questions (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL
                );

CREATE TABLE stats (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                value INTEGER NOT NULL
                );

CREATE TABLE question_stats (
    id INTEGER PRIMARY KEY,
    stat_id INTEGER,
    question_id INTEGER,
    yes INTEGER,
    no INTEGER,

    FOREIGN KEY (stat_id) REFERENCES stats(id)
    FOREIGN KEY (question_id) REFERENCES questions(id)
    );


-- CREATE INDEX question_id_idx ON questions(id);

"""

DATABASE = 'db.sqlite3'

nonflask_con = None

def get_con():
    """ returns a database connection """
    global nonflask_con
    try:
        con = getattr(g, '_database', None)
    except RuntimeError:
        if nonflask_con:
            return nonflask_con
        else:
            print "using non-flask db connection"
            nonflask_con = sqlite3.connect(DATABASE)
            return nonflask_con
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con


def setup():
    con = get_con()
    for query in schema.split(';'):
        con.execute(query)


def execute(query, *args):
    con = get_con()
    cur = con.cursor()
    cur.execute(query, args)
    con.commit()
    return cur


def tuple_list_to_dict_list(tuple_list, keys):
    
    dict_list = []
    for row in tuple_list:
        dict_list.append(dict(zip(keys, row)))
    
    return dict_list


def answer_question(question_id, answer):

    if answer not in ["yes", "no"]:
        # FIXME - use specific Exception
        raise Exception("answer should be yes or no")
    
    for stat_mod in get_question_stats(question_id):
        print "modifying stat for q %s: %s" % (question_id, stat_mod[answer])
        edit_stat(stat_mod['stat_id'], stat_mod[answer])


def new_question(question, stats):
    """ stats are a list of (stat_id, yes, no) """

    cur = execute("INSERT INTO questions (content) VALUES (?)", question)

    for stat_id, yes, no in stats:
        new_question_stat(cur.lastrowid, stat_id, yes, no)

    return cur.lastrowid
        

def get_questions(start_id=0, count=1):
    cur = execute("SELECT * from questions where id >= ? LIMIT ?", start_id, count)
    questions = []
    for question_id, question in cur:
        questions.append({'id': question_id, 'question': question})
    return questions
    

def new_question_stat(question_id, stat_id, yes, no):
    execute('INSERT INTO question_stats (question_id, stat_id, yes, no) VALUES (?, ?, ?, ?)',  question_id, stat_id, yes, no)


def edit_question_stat(question_id, stat_id, yes, no):
    cur = execute('UPDATE question_stats SET yes = ?, no = ? WHERE question_id = ? and stat_id = ?', yes, no, question_id, stat_id)
    if cur.rowcount == 0:
        new_question_stat(question_id, stat_id, yes, no)


def get_question_stats(question_id):
    cur = execute("SELECT stat_id, name, yes, no FROM question_stats JOIN stats ON stats.id = stat_id WHERE question_id = ?", question_id)

    q_stats = tuple_list_to_dict_list(cur, ['stat_id', 'name', 'yes', 'no'])
    
    return q_stats


def new_stat(stat_name, val):
    cur = execute("INSERT INTO stats (name, value) VALUES (?, ?);", stat_name, val)
    return cur.lastrowid


def edit_stat(stat_id, change):
    execute('UPDATE stats SET value = value + ? WHERE id = ?', change, stat_id)


def get_stats():
    cur = execute("SELECT id, name, value FROM stats")

    stats = tuple_list_to_dict_list(cur, ['stat_id', 'name', 'value'])
    return stats
    

"""
new_questions
    - inserts question. returns id

edit question
    - edit the question
    - edit stats.
        in: list of: stat_name, yes, no

get questions

delete question

"""




