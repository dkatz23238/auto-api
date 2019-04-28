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
