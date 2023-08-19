from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from bson import ObjectId
import json
from . import Url
import validators
import datetime
import random
import requests 
import boto3
from .models import get_public_ip
from kazoo.client import KazooClient
import time
zk = KazooClient(hosts='localhost:2181')
zk.start()
def increment_counter(zk, counter_path):
    # Check if the counter node exists, create it if not
    if not zk.exists(counter_path):
        zk.create(counter_path, value=b'0')

    else:
        # Get the current value of the counter
        counter_value, _ = zk.get(counter_path)
        
        # Increment the counter value
        new_value = int(counter_value) + 1
        
        # Update the counter value in ZooKeeper
        zk.set(counter_path, str(new_value).encode())
        
      


# Path for the counter node
counter_path = '/mycounter'

# Call the increment_counter function
increment_counter(zk, counter_path)
views = Blueprint('views', __name__)

def encode(num):
    """Encode a positive number into Base X and return the string.

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    alphabet = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    if num == 0:
        return alphabet[0]
    arr = []
    arr_append = arr.append  # Extract bound-method for faster access.
    _divmod = divmod  # Access to locals is faster.
    base = len(alphabet)
    while num:
        num, rem = _divmod(num, base)
        arr_append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

@views.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        userid = ObjectId(current_user._id)
        title = request.form.get('url_title')
        if (long_url[0:8] != 'https://'):
            long_url = 'https://' + long_url
        validation = validators.url(long_url)
        check = Url.find_one({'long_url': long_url, 'user_id':userid})
        if check: 
            flash('You cannot have duplicate URLs', category = 'error')
        elif not validation: 
            flash('URL is not valid', category = 'error')
        else: 
            current_date = str(datetime.date.today())
            #generate short url
            counter_value, _ = zk.get(counter_path)

            zookept = int(counter_value) 
            zookept = encode(int(counter_value))
            # Call the increment_counter function
            increment_counter(zk, counter_path)
            short_url = '3.128.79.246/' + str(zookept)
            #set _id equal to short url for speed
            new_note = {
                        'short_url':str(short_url),
                        'long_url' : long_url, 
                        'user_id': userid, 
                        'title': title,
                        'times_used': 0, 
                        'created': current_date}
            Url.insert_one(new_note)
            flash('Note Added!', category='success')

    return render_template("home.html", user= current_user)

@views.route('/delete-note', methods = ['POST']) 
def delete_note():
    
    note = json.loads(request.data)
    noteId = ObjectId(note['noteId'])
    note = Url.find_one({'_id': noteId})
    if note['user_id'] == ObjectId(current_user._id): 
        Url.delete_one({'_id':noteId})
    return jsonify({})
