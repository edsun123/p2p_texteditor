from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from CBC import *
import json
from cryptography.fernet import Fernet

load_dotenv()

# Generate Keys
key = bytes(os.getenv('KEY').encode("utf-8"))
encryption_type = Fernet(key)

#generating new keys
myfile="file1"
user1=User("user1")
user1.generate_userkeys()
file1=File(user1, myfile)

file1.generate_filekey()
file1.cipher_gen()
user1.generate_userkeys()


app = Flask(__name__)

from flask_webpackext.project import WebpackTemplateProject
from flask_webpackext import FlaskWebpackExt

project = WebpackTemplateProject(
    __name__,
    project_folder='static',
    config_path="config.json",
)

app.config.update(dict(
    WEBPACKEXT_PROJECT=project,
))

# Initialize extension
FlaskWebpackExt(app)

number_of_users = 2

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def keyCheck():
    print("entering frontend and passing the keys")
    key1 = request.form['key1']  # getting usernames

    if key1 == "password":
        return render_template('quill.html')


@app.route('/editor')
def editor():
    return render_template('quill.html')


# #may leave alone
# @app.route('/process', methods=['POST'])
# def get_post_json():
#     print("posting json onto database")
#     # Connect with Mongodb Atlas.
#     client = MongoClient(os.getenv('MONGO_STRING'))
#     db = client.p2p_docs
#
#     data = request.get_json()
#     print(data)
#
#     ## in case if we don't use flask, we might need to move all operations to javascript
#     user1 = User("user1")
#     user1.generate_userkeys()
#
#     file1 = File(user1, myfile)
#     file1.generate_filekey()
#     file1.cipher_gen()
#     enc_data = file1.encrypt_data(data)
#
#     # Insert into database
#     # db.documents.insert_one(data)
#     db.documents.insert_one(enc_data)
#
#     return jsonify(status="success", data=data)


# @app.route('/getData')
# def get_data():
#     print("retrieving data from database")
#     # Connect with Mongodb Atlas.
#     client = MongoClient(os.getenv('MONGO_STRING'))
#     db = client.p2p_docs
#     collection = db['documents']
#
#     ek = encrypt_key(file1, user1)
#     decrypt_data(ek, user1, file1, enc_data)
#
#     cursor = collection.find({})
#     #    for document in cursor:
#     #        return str(document["ops"])
#
#
#     for document in cursor:
#
#         print("decrypting")
#         print("generating encryption key")
#         ek = encrypt_key(file1, user1)
#         dec_content = decrypt_data(ek, user1, file1, document['data'])
#         print ("this is decrypted data: "+str(dec_data, 'utf-8'))
# #        dec_content = decrypt_data(ek, user1, file1, str(document["ops"]))
#         return dec_content

@app.route('/test', methods=['POST'])
def test():
    global key
    global encryption_type
    global file1
    global user1
    data = request.get_json()
    print(data)

    # Encrypt
    encrypted_message = encryption_type.encrypt(json.dumps(data).encode())
    print(encrypted_message)
    
#    enc_data = file1.encrypt_data(json.dumps(data).encode())

    # Write to file
    f = open("database.txt", "wb")
    f.write(encrypted_message)
    f.close()

    return "success", 201


@app.route('/testGet', methods=['GET'])
def testGet():
    global key
    global encryption_type
    global file1
    global user1
    
    # Read from file and decrypt
    with open('database.txt', "rb") as f:
        encrypted_message = f.readline()
        print(encrypted_message)
        global key
        global encryption_type
        global file1
        global user1
        
#        ek = encrypt_key(file1, user1)
#        dec_data = decrypt_data(ek, user1, file1, enc_data)


        decrypted_message = encryption_type.decrypt(encrypted_message)
        print(decrypted_message)

    return {'data': decrypted_message.decode('utf-8')}

if __name__ == '__main__':
    # print("creating file 1 and user1")
    # myfile="file1"
    # user1=User("user1")
    # user1.generate_userkeys()
    # file1=File(user1, myfile)
    
    # print("creating cipher, userkeys, and filekeys ")
    # file1.generate_filekey()
    # file1.cipher_gen()
    # user1.generate_userkeys()
    
    app.run()
