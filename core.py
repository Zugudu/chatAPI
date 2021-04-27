from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from time import time
import pymongo
import os
# ======================
# Created by great @Zugudu
# ======================


# ======================
# Init values
# ======================
load_dotenv()

db = pymongo.MongoClient(os.environ['DB_URL'])['chat']
print('Database initilize')

app = Flask(__name__)


# ======================
# Define system functions
# ======================
def getCurrentTime():
	return int(time() * 1000)

def getUser(request):
	return db['user'].find_one({'name': 'Test'})['_id']

def getAll(coll):
	return db[coll].find()


def insertOne(coll, doc):
	return db[coll].insert_one(doc).inserted_id


# ===========
# Hight level functions
# Get functions
# ===========
def getAllMessage():
	ret = []
	for el in getAll('message'):
		ret.append({
			"_id": str(el['_id']),
			"user_id": str(el['user_id']),
			"msg": el.get('msg', ''),
			"data": el.get('data', 0)
		})
	return ret


def getAllUser():
	ret = []
	for el in getAll('user'):
		ret.append({
			"_id": str(el['_id']),
			"name": el['name']
		})
	return ret


# ===========
# Add functions
# ===========
def newMessage(user_id, msg):
	message = {
		"user_id": user_id,
		"msg": msg,
		"data": getCurrentTime()
	}
	return insertOne('message', message)


# ======================
# Define Routes
# ======================
@app.route('/m', methods=['GET', 'POST'])
def message():
	if request.method == 'GET':
		return jsonify(getAllMessage())
	elif request.method == 'POST':
		msgText = request.get_json().get('mes')
		if msgText:
			newMessage(str(getUser(request)), msgText)
			return ('OK', 200)
		else:
			abort(400)
	else:
		abort(404)


@app.route('/u')
def user():
	if request.method == 'GET':
		return jsonify(getAllUser())
	else:
		abort(404)