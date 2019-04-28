import oyaml
from yaml import SafeLoader
import pprint
import jinja2

TEMPLATE = """
import flask
import flask_sqlalchemy
import flask_restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)
{% for row in tables %}
{% for k, v in row.items() %}
class {{ k }}(db.Model):
    {% for k1, v1 in v.items() -%}
    {% if ((v1["dtype"] == "Unicode" ) and ("primary_key" in v1.keys())) -%}
    {{k1}} = db.Column(db.{{v1["dtype"]}}({{v1["length"]}}), primary_key=True)
    {% elif ("length" in v1.keys()) and (not "primary_key" in v1.keys())  -%}
    {{k1}} = db.Column(db.{{v1["dtype"]}}({{v1["length"]}}))
    {% else -%}
    {{k1}} = db.Column(db.{{v1["dtype"]}}())
    {% endif -%}
    {%- endfor %}{%- endfor %}{%- endfor %}


db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
{% for row in tables -%}
{% for k, v in row.items() %}
manager.create_api({{k}}, methods=['GET', 'POST', 'DELETE'])
{% endfor %}
{%- endfor %}
if __name__ == '__main__':# main()
    app.run(port=5353)
"""


def load_dict(dir):
    f = open(dir, "r").read()
    auto_api_dict = oyaml.load(f, Loader=SafeLoader)
    return auto_api_dict

LEGAL_DATATYPES = ["Boolean", "Unicode", "BigInt", "Integer", "Date", "DateTime", "Float"]

def validate_yaml(auto_api_dict):
    ''' Validate the yaml file so that only legal datatypes are allowed and only length is attributed to unicode.'''
    for k1 in auto_api_dict.keys():
        for k2 in auto_api_dict[k1].keys():
            # print(k2)
            for k3 in auto_api_dict[k1][k2].keys():
                if k3 == "dtype":
                    dtype = auto_api_dict[k1][k2][k3]
                    assert dtype in LEGAL_DATATYPES, "Column data type is not a legal datatype"

                elif k3 == "length":
                    corresponding_dtype = auto_api_dict[k1][k2]["dtype"]
                    assert (
                    (sorted(auto_api_dict[k1][k2].keys()) == ["dtype", "length"]
                    or
                    sorted(auto_api_dict[k1][k2].keys()) == ["dtype", "length", "primary_key"]) and
                    corresponding_dtype == "Unicode"), "Only unicode data type has length"

def assert_primary_keys_valid(auto_api_dict):
    ''' Asserts that there is one primary key per table '''
    table_columns = []
    for k,v in auto_api_dict.items():

        for k1,v1 in v.items():
            if "primary_key" in v1:
                table_columns.append(v1)

    assert len(table_columns) == len(auto_api_dict.keys()), "You must provide one primary_key per table"

def render_temp(auto_api_dict):
    validate_yaml(auto_api_dict)
    assert_primary_keys_valid(auto_api_dict)
    tables = [ { k:auto_api_dict[k] } for k in auto_api_dict.keys() ]
    t = jinja2.Template(TEMPLATE)
    render = t.render(tables = tables)
    return render
