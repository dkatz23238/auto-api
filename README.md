# auto-api

0. Populate auto-api.yml file
1. ```python -m pip install -r requirements.txt``` or ```python setup.py```
2. python makeapi >> app.py

# auto-api.yml file
``` yaml
# one primary_key per table
# types: Boolean, Unicode, Integer, Date, DateTime, or Float
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


```
This will generate the following python code:

```python
import flask
import flask.ext.sqlalchemy
import flask.ext.restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)


class people(db.Model):
    first_name = db.Column(db.Unicode(), primary_key=True)
    last_name = db.Column(db.Unicode())
    age = db.Column(db.Integer())


class teams(db.Model):
    team_name = db.Column(db.Unicode())
    team_id = db.Column(db.Unicode(36), primary_key=True)



db.create_all()
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)


manager.create_api(people, methods=['GET', 'POST', 'DELETE'])



manager.create_api(teams, methods=['GET', 'POST', 'DELETE'])


if __name__ == '__main__':# main()
    app.run(port=5353)

```
