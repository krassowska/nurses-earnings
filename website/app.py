from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from map import test_has_uppercase, test_is_lowercase
from sqlalchemy.ext.automap import automap_base
from unidecode import unidecode


app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
Base = automap_base(declarative_base=db.Model)
engine = db.engine

Base.prepare(engine, reflect=True)

NursingCourse = Base.classes.nursing_course
Person = Base.classes.person
Employment = Base.classes.employment
Education = Base.classes.education

app.jinja_env.tests['has_uppercase'] = test_has_uppercase
app.jinja_env.tests['is_lowercase'] = test_is_lowercase
app.jinja_env.globals['unidecode'] = unidecode


import routes
