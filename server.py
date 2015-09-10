from flask import Flask, render_template, redirect, url_for, session, request, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '=\xb3\xb0iAb\x93\xec\x9f\x0f\xde\xf3\x06R\xd8\xa0*\x1fh\xd7%Q\x88\xaf'
mysql = MySQLConnector('the_wall_flask')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/users', methods=['POST'])
def create():
	error = False
	email = request.form['email']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	password = request.form['password']

	if len(first_name) < 1:
		error = True
		flash('First name cannot be blank')
	if len(last_name) < 1:
		error = True
		flash('Last name cannot be blank')
	if len(email) < 1:
		error = True
		flash('Email cannot be blank')
	if len(password) < 1:
		error = True
		flash('Password cannot be blank')
	if not EMAIL_REGEX.match(email):
		error = True
		flash('Email is invalid')

	if error:
		return redirect(url_for('index'))
	# run validations and if they are successful we can create the password hash with bcrypt
	pw_hash = bcrypt.generate_password_hash(password)
	
	# now we insert the new user into the database
	insert_query = "INSERT INTO users (email, first_name, last_name, password, created_at) VALUES ('{}', '{}', '{}', '{}', NOW())".format(email, first_name, last_name, pw_hash)
	mysql.run_mysql_query(insert_query)
	return redirect(url_for('index'))

app.run(debug=True)