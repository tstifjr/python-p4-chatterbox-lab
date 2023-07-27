from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message
##
app = Flask(__name__) #turns our file into a Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
#above #NECESSARY adn is configuration stuff for setting up flask, includes defining/setting location for a sql database we will use to store all our data

CORS(app) #weird shit/may be needed when communicating between server-side and client-side

migrate = Migrate(app, db) #NECESSARY #setups under the hood stuff to allow our python code to communicate with and modify our database 
#essentially it tells our code how to use Flask to run Alembic

db.init_app(app) #NECESSARY #hooks up our Flask app with the db object that allows us to use SQLAlchemy stuff in our app thorugh db.
api = Api(app) #how we can access the flask_restful functionality in our app // isn't needed if only using @app.route setup


##Uncomment one of the two solutions below
############ @app.route solutions for the lab ########################

@app.route('/messages', methods = ("GET", "POST")) #decorator includes path and kind of methods you are expecting from a client-request
def messages():
    if request.method == "GET": #use if/elif statements to choose which code to run based on the received request (e.g. GET, POST, DELETE, PATCH)
        mess_dict = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]

        return  make_response(mess_dict, 200)
    
    elif request.method == "POST":
        data = request.get_json() #takes the recieved request (which inlcudes different stuff (header, method, body, etc..) in a stringified format), grabs and fomrats the data from it (JSON format), and sets it to the variable(e.g. data) (think r.json())
        new_message = Message(body = data['body'], username = data['username']) #creates a new instance of a Message with the request data we recevied 

        db.session.add(new_message) #adds the new message to our session object
        db.session.commit() #this step actually commits changes to the db

        mes_dict = new_message.to_dict() #the .to_dict() is method we call upon a class instance to convert all of their attributes to format resembling JSON

        response = make_response(mes_dict, 201) #takes the our data, a status code, and headers(optional) and packages it in a response object (this is the r you get in Javascript after a fetch(e.g. .then(r=>r.json())))
        return response #returns the response we want to send back to the client-side(this happens b/c of Flask/@app.route)


@app.route('/messages/<int:id>', methods=("DELETE", "PATCH"))
def messages_by_id(id):
    if request.method == "DELETE":
        message = Message.query.filter(Message.id == id).first()

        db.session.delete(message)
        db.session.commit()

        response = make_response({"message": f"Message id {id} has been deleted"}, 200)
        return response
        
    elif request.method == "PATCH":
        data = request.get_json() 
        message = Message.query.filter(Message.id == id).first()
        for attr in data:
            setattr(message, attr, data[attr]) #dictionary[key] => value : dictionary ::{key1 : value1, key2 : value2, key3: value3}
        db.session.commit()

        return make_response(message.to_dict(), 200)


############## Flask-restful solutions for the Lab ###########################

# ######## This maps to messages() above ###########
# class Messages(Resource): #makes the class we created act as a Resource class, so it can be used in the api.add_resource below
#     def get(self): #is called to run when recieve GET request
#         mess_dict = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
#         return  make_response(jsonify(mess_dict), 200)
    
#     def post(self): #is called when we receive a POST reqeust
#         data = request.get_json() #{'body': 'Some message we wrote on the clent', 'username': 'Duane'}
#         new_message = Message(body = data['body'], username = data['username'])

#         db.session.add(new_message)
#         db.session.commit()
#         mes_dict = new_message.to_dict()
#         response = make_response(jsonify(mes_dict), 201)
#         return response

# api.add_resource(Messages, '/messages') #how we hook up our class and its methods to interact with requests sent to us on the path in ''

# ########### This maps to messages_by_id() above ###################
# class MessageById(Resource):
#     def patch (self, id):
#         data = request.get_json() 
#         message = Message.query.filter_by(id=id).first()
#         for attr in data:
#             setattr(message, attr, data[attr]) #dictionary[key] => value : dictionary ::{key1 : value1, key2 : value2, key3: value3}
#         db.session.commit()

#         return make_response(jsonify(message.to_dict()), 200)

#     def delete(self, id):
#         message = Message.query.filter_by(id=id).first()

#         db.session.delete(message)
#         db.session.commit()

#         response = make_response(jsonify({"message": f"Message id {id} has been deleted"}), 200)
#         return response
     
# api.add_resource(MessageById, '/messages/<int:id>') #including the <int:id> in our path, will pass the value to our MessageById class as an arguement


if __name__ == '__main__':
    app.run(port=4000)
