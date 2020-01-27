from app import app
from db import db

db.init_app(app)

# create the database if it does not exists (no need for create_tables.py anymore)
# still need to run app.py from /code folder
@app.before_first_request
def create_tables():
    db.create_all()
