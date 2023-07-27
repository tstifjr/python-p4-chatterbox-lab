from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata) #creates an instance of the SQLAlchemy special class and assigns it to db
#db is therefore essentially a data object that stores a whole bunch of methods/functions/attributes/etc.. that we gain access to by using db._____

class Message(db.Model, SerializerMixin): #SerializerMixin is a class we import that is passed to our Models so that they can have access to the to_dict method
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now()) #server_default inputs a default value for this column in the db when a instance is created.  db.func.now() is a function within the db class that returns the current time
    updated_at = db.Column(db.DateTime, onupdate = db.func.now()) #onupdate inputs a value for this column in the db when an update to the record (instance of a Class or a change in the column of a row) happens.