from autoapi import *
import oyaml

input = """
# types: boolean, unicode, integer, date, datetime, float
people:
  first_name:
    dtype: Unicode
    primary_key: true
  last_name:
    dtype: Unicode
  age:
    dtype: Integer

teams:
  team_name:
    dtype: Unicode
  team_id:
    dtype: Unicode
    length: 36
    primary_key: true

"""

output= """

import flask
import flask_sqlalchemy
import flask_restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)


class people(db.Model):
    first_name = db.Column(db.Unicode(), primary_key=True)
    last_name = db.Column(db.Unicode())
    age = db.Column(db.Integer())


class teams(db.Model):
    team_name = db.Column(db.Unicode())
    team_id = db.Column(db.Unicode(36), primary_key=True)



db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(people, methods=['GET', 'POST', 'DELETE'])

manager.create_api(teams, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':# main()
    app.run(port=5353)
"""

auto_api_dict = oyaml.load(input, Loader=SafeLoader)

assert render_temp(auto_api_dict), output
