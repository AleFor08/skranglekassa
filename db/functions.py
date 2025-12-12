from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
import mysql.connector, bcrypt
import json

try:
	import ai_logic as ai
	print("Is ai yes")
	noai = False
except:
	print("Ai not working")
	noai = True




# loggedIn = False


def connect():
	db = mysql.connector.connect(
	host = "127.0.0.1",		#
	user = "root",			# Change credentials
	password = "root",		#
	database = "skranglekassa",
	port = 3306
	)

	c = db.cursor()
	return db, c


def encrypt(password):
	hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
	print("password hashed", hashed)
	return hashed


def retrieve():
	data = request.get_json(force=True)
	print("Retrieved")
	return data

# Eskil code

# Load product database from JSON file
with open("db/database.json", "r") as f:
	database = json.load(f) # Load product to database variable

# End of Eskil code