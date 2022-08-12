import os
import hashlib
from bson.json_util import dumps
import datetime
from flask_cors import cross_origin
from db import *
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



load_dotenv()

app = Flask(__name__)


jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=8)


@app.route('/', methods=["GET"])
def index():
	return "<p>Simple REST API</p>"


@app.route('/register/', methods=["POST"])
@cross_origin()
def register():

	new_user = request.get_json()
	new_user["password"] = hashlib.sha256(new_user['password'].encode("utf-8")).hexdigest()

	database_collection = db.users
	doc = database_collection.find_one({"email": new_user["email"]})
	if not doc:
		database_collection.insert_one(new_user)  #SAVED TO DATABASE
		return jsonify({'msg': 'User created successfully'}), 201
	else:
		return jsonify({'msg': 'Username already exists'}), 409


@app.route('/login/', methods=["POST"])
@cross_origin()
def login():

    login_info = request.get_json()
    database_collection = db.users
    database_users = database_collection.find_one({'email': login_info['email']})
    if database_users:
        encrpted_password = hashlib.sha256(login_info['password'].encode("utf-8")).hexdigest()
        if encrpted_password == database_users['password']:
            access_token = create_access_token(identity=str(database_users['_id']))
            return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'The username or password is incorrect'}), 401



	


@app.route('/template/<id>', methods=["GET"])
@jwt_required()
def template_id(id):

	get_jwt_identity()

	database_collection = db.users
	data = dumps(database_collection.find_one({"_id":ObjectId(id)}))
	if data:
		return jsonify({'msg': 'Template fetch successful', 'data':data}), 200
	else:
		return jsonify({'msg': 'Template does not exist in current collection'}), 500
		



	

if __name__ == '__main__':
	app.run(threaded=True, port=5000)
