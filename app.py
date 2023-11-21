from flask import Flask
from flask_bcrypt import generate_password_hash

from db import *
from util.blueprints import register_blueprints
from models.users import Users

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://127.0.0.1:5432/apc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)


def create_admin():

    admin = db.session.query(Users).filter(Users.email == "admin@test.com").first()

    if not admin:
        email = "admin@test.com"
        password = "1234"
        role = "admin"
        active = True

        password = generate_password_hash(password).decode("utf8")

        new_admin = Users(email, password, role, active)
        db.session.add(new_admin)
        db.session.commit()


def create_user():

    user = db.session.query(Users).filter(Users.email == "user@test.com").first()

    if not user:
        email = "user@test.com"
        password = "1234"
        role = "user"
        active = True

        password = generate_password_hash(password).decode("utf8")

        new_user = Users(email, password, role, active)
        db.session.add(new_user)
        db.session.commit()


def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")

        print("Creating users...")
        create_admin()
        create_user()
        print("Users created successfully")


register_blueprints(app)

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port="8086", debug=True)
