from flask import Flask, jsonify, request, make_response
from models import db, Customer
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db.init_app(app)



api = Api(app)



class Index(Resource):

    @staticmethod
    def get():
        response_dict = {
            "index": "Welcome to the Project RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

api.add_resource(Index, '/')

class LogIn(Resource):

    @staticmethod
    def post():
        user = Customer.query.filter_by(lastname=request.get_json()['username']).first()
        
        response = make_response(
            jsonify(user.to_dict()),
            201,
        )
        return response

api.add_resource(LogIn, '/login')



class Customers(Resource):

    @staticmethod
    def get():
        response_dict_list = [n.to_dict() for n in Customer.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

    @staticmethod
    def post():
        
        data = request.get_json()
        new_record = Customer(
            firstname=data["firstname"],
            lastname=data['lastname'],
            email=data['email'],
            password=data['password'],
            address=data['address'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )
        return response


api.add_resource(Customers, '/customers')

class CustomerByID(Resource):

    @staticmethod
    def get(id):
        response_dict = Customer.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )
        return response

    @staticmethod
    def patch(id):
        record = Customer.query.filter_by(id=id).first()
        for attr in request.get_json():
            setattr(record, attr, request.get_json()[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            jsonify(response_dict),
            200
        )
        return response

    @staticmethod
    def delete(id):
        record = Customer.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )
        return response

api.add_resource(CustomerByID, '/customers/<int:id>')




if __name__ == "__main__":
    app.run(debug=True)
