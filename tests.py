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
input1 = """
inventory:
  product_id:
    dtype: Unicode
    length: 36
    primary_key: true
  stock:
    dtype: Integer

products:
  product_id:
    dtype: Unicode
    primary_key: true
  product_name:
    dtype: Unicode
  product_price_usd:
    dtype: Float

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
output1 = """

import flask
import flask_sqlalchemy
import flask_restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)


class inventory(db.Model):
    product_id = db.Column(db.Unicode(36), primary_key=True)
    stock = db.Column(db.Integer())


class products(db.Model):
    product_id = db.Column(db.Unicode(), primary_key=True)
    product_name = db.Column(db.Unicode())
    product_price_usd = db.Column(db.Float())



db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(inventory, methods=['GET', 'POST', 'DELETE'])

manager.create_api(products, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':# main()
    app.run(port=5353)
"""
auto_api_dict = oyaml.load(input, Loader=SafeLoader)
auto_api_dict1 = oyaml.load(input1, Loader=SafeLoader)

assert render_temp(auto_api_dict), output
assert render_temp(auto_api_dict1), output1
