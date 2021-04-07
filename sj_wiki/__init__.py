from flask import Flask

app = Flask(__name__, template_folder='templates')
DATABASE = 'test.db'

from sj_wiki import routes
