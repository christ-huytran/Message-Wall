from flask import Flask, render_template, redirect, url_for, session, request, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
import time
from time import mktime
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '=\xb3\xb0iAb\x93\xec\x9f\x0f\xde\xf3\x06R\xd8\xa0*\x1fh\xd7%Q\x88\xaf'
mysql = MySQLConnector('the_wall_flask')

@app.route('/')
def index():
	return render_template('signup.html')

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

@app.route('/signin', methods=['POST','GET'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	email = request.form['email']
	password = request.form['password']
	user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(email)
	user = mysql.fetch(user_query)

	if user:
		if bcrypt.check_password_hash(user[0]['password'], password):
			session['id'] = user[0]['id']
			session['first_name'] = user[0]['first_name']
			return redirect(url_for('show'))
	flash('Invalid email or password')
	return redirect(url_for('signin'))

@app.route('/signout')
def signout():
	session.pop('id')
	session.pop('first_name')
	return redirect(url_for('index'))

@app.route('/messages', methods=['GET', 'POST'])
def show():
	if request.method == 'GET':
		# get_msgs_query = "SELECT messages.id, messages.message, CONCAT(users.first_name, ' ', users.last_name) AS author, messages.created_at FROM messages JOIN users ON users.id = messages.user_id ORDER BY messages.created_at DESC"
		get_msgs_query = "SELECT messages.id, messages.message, CONCAT(users.first_name, ' ', users.last_name) AS message_author, messages.created_at AS message_created_at, GROUP_CONCAT(comments.comment SEPARATOR '-----') AS comments, GROUP_CONCAT(CONCAT(users2.first_name, ' ', users2.last_name)) AS comment_author, GROUP_CONCAT(comments.created_at) AS comment_created_at FROM messages JOIN users ON users.id = messages.user_id LEFT JOIN comments ON messages.id = comments.message_id LEFT JOIN users AS users2 ON users2.id = comments.user_id GROUP BY messages.id ORDER BY messages.created_at DESC"

		messages = mysql.fetch(get_msgs_query)
		print messages
		for msg in messages:
			if msg['comments']:
				msg['comments'] = msg['comments'].split('-----')
				msg['comment_author'] = msg['comment_author'].split(',')
				msg['comment_created_at'] = msg['comment_created_at'].split(',')
				for index, value in enumerate(msg['comment_created_at']):
					msg['comment_created_at'][index] = datetime.fromtimestamp(mktime(time.strptime(value, '%Y-%m-%d %H:%M:%S')))

		return render_template('messages.html', messages=messages)
	message = request.form['message']
	escape_message = message.replace("'", "\\'")
	if len(message) < 1:
		flash('Message cannot be blank')
	else:
		insert_msg_query = "INSERT INTO messages (message, user_id, created_at) VALUES ('{}','{}',NOW())".format(escape_message, session['id'])
		mysql.run_mysql_query(insert_msg_query)
	return redirect(url_for('show'))

@app.route('/comments', methods=['POST'])
def create_comment():
	comment = request.form['comment']
	escape_comment = comment.replace("'", "\\'")
	message_id = request.form['message_id']
	insert_comment_query = "INSERT INTO comments (comment, message_id, user_id, created_at) VALUES ('{}','{}','{}', NOW())".format(escape_comment, message_id, session['id'])
	mysql.run_mysql_query(insert_comment_query)
	return redirect(url_for('show'))

app.run(debug=True)