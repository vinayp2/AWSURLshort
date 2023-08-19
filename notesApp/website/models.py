from . import db, Users, Url
from flask import jsonify, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
import requests
import boto3
import os
from dotenv import load_dotenv
import socket

def get_public_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_ip = s.getsockname()[0]
    s.close()
    return public_ip

#need to make user and url generator





#User mixin provides things like is_autenticated and get_id 
class User(UserMixin):
    #id is internally stored as a ObjectId

    def get_id(self): 
        return str(self.user_data['_id'])
    def __init__(self,user_data): 
        self.user_data = user_data
        email = user_data['email']
        temp = db.Users.find_one({"email":email}, {"_id":1})
        self._id = temp["_id"]
    #returns the notes the user has created 
    def notes(self): 
        ret = []
        for i in Url.find({'user_id': self._id}):
            note = Notes(i)
            ret.append(note)
        return ret
class Notes(): 
    def __init__(self, note_data): 
        self._id = note_data['_id']
        self.title = note_data['title']
        self.user_id = note_data['user_id']
        self.times_used = note_data['times_used']
        self.created = note_data['created']
        self.long_url = note_data['long_url']
        self.short = (note_data['short_url'])
     
def find_email(email): 
    user = db.Users.find_one({'email':email}, {"_id":1, "email":1, "firstName":1, "password":1})
    return user 
def find_long(short_url): 
    user = db.Url.find_one({'short_url':"http://127.0.0.1:5000/awsdkel"})
    if user:
        found_long = user['long_url']
        return found_long
    return None

