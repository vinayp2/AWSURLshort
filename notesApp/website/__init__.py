#this file makes the website folder a python folder.
#init runs automatically when called



import bson 
import os
from os import path 
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify, redirect, flash
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from flask_login import LoginManager
from bson import ObjectId
# access your MongoDB Atlas cluster
load_dotenv()
connection_string = os.environ.get("CONNECTION_STRING")


#mongo_client:MongoClient = MongoClient(connection_string)

# add in your database and collection from Atlas
#db: Database = mongo_client.get_database("Bookshelf")
# connection_string = os.environ.get("CONNECTION_STRING")

# mongo:MongoClient = MongoClient(connection_string)

# db: Database = mongo.get_database("urlshort")
# collection: Collection = db.get_collection("Book")
# book = {"name": "John Lennon"}
# collection.insert_one(book)





load_dotenv()
connection_string = os.environ.get("CONNECTION_STRING")

mongo:MongoClient = MongoClient(connection_string)
db: Database = mongo.get_database("urlprogram")
Users: Collection = db.get_collection("Users")
Url: Collection = db.get_collection("URL")

def create_app():
    
    app = Flask(__name__) # how you initialize flask
    app.config['SECRET_KEY'] = ';7lka1js3dfj;a1klsd4f;'#secret key don't share
    app.config["MONGO_URI"] = connection_string
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    
    
    #set db and config app



    from .views import views
    from .auth import auth
    #from .redirect import redirect

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    #app.register_blueprint(redirect, url_prefix = '/')
    #from .models import #put stuff to import
    from .models import User
    # @auth.route('/<short_url>')
# def redirect_url(short_url):
#     short_url = request.url_root + short_url
#     print(short_url)
#     item = find_long(str(short_url))
#     if item: 
#         return redirect(item) 
#     else: 
#         return "URL not found", 404
    @app.route('/<path:path>')
    def catch_all(path):
        short_url = '3.128.79.246/' + path
        print(short_url) 
        item = Url.find_one({'short_url':short_url})
        if item: 
            long_url = item['long_url']
            
            Url.find_one_and_update(
                {'short_url':short_url},
                {'$inc':{'times_used':1}}
                 )
            return redirect(long_url)
        return f'Route not found. There may be a typo in --> {request.url_root}{path}', 404
    @login_manager.user_loader
    #this function loads user using the id field needed
    def load_user(id):
        #return using object user id
        user_data = db.Users.find_one({'_id':ObjectId(id)})
        return User(user_data)
        #load user and compares 


    return app
#made flask app, secret key and returned it from init
#import website package into main.py

