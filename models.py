from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin




db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, unique=True)
    lastname = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    address = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())


    def __repr__(self):
        return f'<Customer Item {self.firstname}>'
    @validates("firstname", "lastname")
    def validate_names(self,key,name):
        if not name:
            raise ValueError('Name Field is required')
        return name
    
    @validates("email")
    def validate_email(self,key,value):
        if '@' not in value:
            raise ValueError('Please enter a valid email')
        return value
