from flask import Flask
from map import test_has_uppercase, test_is_lowercase


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.jinja_env.tests['has_uppercase'] = test_has_uppercase
app.jinja_env.tests['is_lowercase'] = test_is_lowercase

import routes
