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

CREATE INDEX question_id_idx ON questions(id);

