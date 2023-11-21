from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
import uuid

from db import db


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(), nullable=True, unique=True)
    password = db.Column(db.String(), nullable=True)
    role = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    auth = db.relationship("AuthTokens", back_populates="user")

    def __init__(self, email, password, role, active):
        self.email = email
        self.password = password
        self.role = role
        self.active = active

    def get_new_user():
        return Users("", "", "user", True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "email", "role", "active"]


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
