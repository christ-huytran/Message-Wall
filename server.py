from flask import Flask, render_template, redirect, url_for, session, request
# from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = '=\xb3\xb0iAb\x93\xec\x9f\x0f\xde\xf3\x06R\xd8\xa0*\x1fh\xd7%Q\x88\xaf'
# mysql = MySQLConnector('mydb')

@app.route('/')
def index():
	return render_template('index.html')

app.run(debug=True)