from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

# @app.route('/messages', methods = ("GET", "POST"))
# def messages():
#     return ''
class Messages(Resource):
    def get(self): #is called to run when recieve GET request
        mess_dict = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        return  make_response(jsonify(mess_dict), 200)
    
    def post(self):
        data = request.get_json() #{'body': 'Some message we wrote on the clent', 'username': 'Duane'}
        new_message = Message(body = data['body'], username = data['username'])

        db.session.add(new_message)
        db.session.commit()

        response = make_response(jsonify(new_message.to_dict()), 201)
        return response

api.add_resource(Messages, '/messages')

class MessageById(Resource):
    def patch (self, id):
        data = request.get_json() 
        message = Message.query.filter_by(id=id).first()
        for attr in data:
            setattr(message, attr, data[attr]) #dictionary[key] => value : dictionary ::{key1 : value1, key2 : value2, key3: value3}
        db.session.commit()

        return make_response(jsonify(message.to_dict()), 200)

    def delete(self, id):
        message = Message.query.filter_by(id=id).first()

        db.session.delete(message)
        db.session.commit()

        response = make_response({"message": f"Message id {id} has been deleted"}, 200)
        return response
     
api.add_resource(MessageById, '/messages/<int:id>')

# # @app.route('/messages/<int:id>', methods=("DELETE", "PATCH"))
# # def messages_by_id(id):
# #     return ''

if __name__ == '__main__':
    app.run(port=4000)
