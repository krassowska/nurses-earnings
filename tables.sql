DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

CREATE TYPE education_type AS ENUM (
    'liceum medyczne',
    'szkola policealna',
    'licencjat',
    'magister',
    'doktorat',
    'studia pomostowe',
    'studia podyplomowe',
    'kurs kwalifikacyjny',
    'kurs specjalistyczny',
    'specjalizacja',
    'inne'
);

CREATE TABLE IF NOT EXISTS nursing_course (
    id serial PRIMARY KEY,
    course_level education_type NOT NULL,
    course_name text NOT NULL,
    UNIQUE (course_level, course_name)
);

CREATE TABLE IF NOT EXISTS person (
    id serial PRIMARY KEY,
    username text NOT NULL UNIQUE,
    hashed_password text NOT NULL,
    date_added timestamptz NOT NULL,
    date_modified timestamptz NOT NULL,
    year_of_birth INTEGER NOT NULL,
    sex text NOT NULL,
    years_of_experience NUMERIC
);

CREATE TABLE IF NOT EXISTS employment (
    id serial PRIMARY KEY,
    date_from DATE,
    date_to DATE,
    place text,
    position text,
    type_of_contract text,
    wage NUMERIC,
    wage_per_x text,
    person_id INTEGER REFERENCES person (id),
    date_entered timestamptz NOT NULL,
    date_modified timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS education (
    id serial PRIMARY KEY,
    year_course_finished INTEGER,
    nursing_course_id INTEGER REFERENCES nursing_course (id),
    person_id INTEGER REFERENCES person (id),
    date_entered timestamptz NOT NULL,
    date_modified timestamptz NOT NULL
);