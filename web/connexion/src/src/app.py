import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from datetime import timedelta
from hashlib import sha512
from base64 import b64encode
# import js2py
# from utils import encrypt, get_db_connection, get_key_hex
from db_utilities import get_db_connection
from encryption import encrypt_message, get_key_hex
# import secrets

# import sys
# import platform
# print(sys.version)
# print(platform.version)

def get_post(post_id):
	conn = get_db_connection()
	post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
	conn.close()
	if post is None:
		abort(404)
	return post

# print(f'__name__ == {__name__}')

app = Flask(__name__)
# app.config['SECRET_KEY'] = '7WZKFbMK4264CaLstxK0WRha7jdDjVaURbEbkJsxxPBt6uP2GiIga0RS3LpL6WSK'
# app.config['SECRET_KEY'] = b64encode(secrets.randbits(48*8).to_bytes(48,'little')).decode()
# app.config['SECRET_KEY'] = b'\xbc\x98\x14\x02\x8e\x1c\xfd\xa0.\xc7\xc2\xa3w \xeb2\xa5-\xdel\xbc\x1b\xd3\x00\xb8\n\xa57\xee\x99\xe4\x87'
# app.config['SECRET_KEY'] = b'\xaf\x16\xe1\xe7a,\xe2_Iy\x19\x98\x9bU\xfc\x0b;B\xf3\x10z<\xc5\xac\x81\xaeG\xe3\xdf]\xb9$,\xe7\xa8|Z\xa6^9\xd6>\xd4g\x95\xc5@6eO\x05Gs0\xd8\xd6\x80\x9az\xed\x9b\x12\xf9\xf8'
app.config['SECRET_KEY'] = os.urandom(64)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# session.permanent = True

def new_message(message, sender, receiver):
	# key = get_key_hex(sender, receiver)
	conn = get_db_connection()
	cur = conn.cursor()
	# mt = encrypt_message(message, sender, receiver)
	# print(mt)
	mt = message
	cur.execute("INSERT INTO messages (sender, receiver, messagetime, messagetext) VALUES (?, ?, ?, ?)",
		(
			sender,
			receiver,
			'CURRENT_TIMESTAMP',
			# encrypt(message, key)
			mt
		)
	)
	users = [sender, receiver]
	users.sort()
	if len(cur.execute("SELECT user1 FROM chats WHERE (user1=? AND user2=?)", (users[0], users[1])).fetchall()) == 0:
		cur.execute("INSERT INTO chats (user1, user2, lastmodify) VALUES (?,?,?)", (users[0], users[1], 'CURRENT_TIMESTAMP'))
	else:
		cur.execute("""
			UPDATE chats
			SET lastmodify = CURRENT_TIMESTAMP
			WHERE (user1=? AND user2=?) 
		""", (users[0], users[1]))
	conn.commit()
	conn.close()

def new_encrypted_message(message, sender, receiver):
	new_message(encrypt_message(message, sender, receiver), sender, receiver)


@app.route('/signin', methods=('GET','POST'))
def signin():
	if session.get('userid') != None:
		return render_template('message.html', message='Already logged in!')
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if not username:
			flash('Username is required!')
		elif not password:
			flash('Password is required!')
		else:
			conn = get_db_connection()
			cur = conn.cursor()
			cur.execute('SELECT userid FROM users WHERE username=?', (username,))
			uids = cur.fetchall()
			conn.close()
			if len(uids) != 0:
				flash('Username not available')
			else:
				conn = get_db_connection()
				cur = conn.cursor()
				cur.execute("INSERT INTO users (username, passwordhash, seed) VALUES (?,?,?)", (
					username,
					sha512(password.encode('utf-8')).hexdigest(),
					os.urandom(32).hex()
				))
				conn.commit()
				cur.execute('SELECT userid FROM users WHERE username=?', (username,))
				uids = cur.fetchall()
				admin = cur.execute('SELECT userid FROM users WHERE username=?', ('admin',)).fetchone()['userid']
				bot = cur.execute('SELECT userid FROM users WHERE username=?', ('bot',)).fetchone()['userid']
				conn.close()
				if len(uids) != 1:
					return render_template('message.html', message='Something went wrong')
				uid = uids[0]['userid']
				session['userid'] = uid
				new_encrypted_message("Welcome to Connexion. I'm the admin, it can take a long time to answer you (don't write here if you need help, these messages will not be read).", admin, uid)
				new_encrypted_message("Welcome to Connexion. I'm a bot, try some of the buttons below!", bot, uid)
				return redirect(url_for('homepage'))
			return redirect(url_for('signin'))
	return render_template('signin.html')

@app.route('/login', methods=('GET','POST'))
def login():
	if session.get('userid') != None:
		return render_template('message.html', message='Already logged in!')
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if not username:
			flash('Username is required!')
		elif not password:
			flash('Password is required!')
		else:
			conn = get_db_connection()
			cur = conn.cursor()
			cur.execute('SELECT userid FROM users WHERE username=? AND passwordhash=?',
				(username, sha512(password.encode('utf-8')).hexdigest())
			)
			uids = cur.fetchall()
			conn.close()
			if len(uids) != 1:
				flash('Wrong username or password')
			else:
				session['userid'] = uids[0]['userid']
				return redirect(url_for('homepage'))
			return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/homepage')
def homepage():
	userid = session.get('userid')
	if userid == None:
		return redirect(url_for('login'))
	conn = get_db_connection()
	res = conn.execute('SELECT user1,user2 FROM chats WHERE (user1=? OR user2=?)',(userid,userid)).fetchall()
	s = set()
	# print(res)
	for r in res:
		# print(r)
		for c in ['user1','user2']:
			if r[c] != userid and r[c] not in s:
				s.add(r[c])
	chats = []
	for u in s:
		res = conn.execute('SELECT username FROM users WHERE userid=?',(u,)).fetchall()
		if(len(res)>0):
			chats.append([u, res[0]['username']])
	conn.close()
	return render_template('homepage.html', chats=chats)

@app.route('/')
def index():
	if(session.get('userid') == None):
		return redirect(url_for('login'))
	else:
		return redirect(url_for('homepage'))

@app.route('/getkey/<int:user1_id>/<int:user2_id>', methods=('GET',))
def getkey(user1_id,user2_id):
	if session.get('userid') == user1_id:
		k = get_key_hex(user1_id, user2_id)
		if k == None:
			abort(404)
		return k
	else:
		return abort(401)

bot_msg = {
	"What's the best CTF category?": 'Cryptography, of course',
	'Siamo primi?': 'Check the scoreboard!',
	"What's the flag?": 'Sorry, I can answer this question only to admins'
}

@app.route('/chat/<int:user1_id>/<int:user2_id>', methods=('GET','POST'))
def chat(user1_id, user2_id):
	if 'userid' not in session.keys():
		return redirect(url_for('logout'))
	allowed_users = [1, 2, session.get('userid',1)]
	if user2_id not in allowed_users or user1_id not in allowed_users:
		# print(user2_id, session.get('userid',-1))
		abort(401)
	if request.method == 'POST':
		if user1_id != session['userid']:
			abort(401)
		messagetext = request.form['message']
		# print(messagetext)
		if not messagetext:
			flash('Message is required!')
		else:
			if user2_id == 2:
				new_encrypted_message(messagetext, user1_id, user2_id)
				# print(messagetext.encode())
				new_encrypted_message(bot_msg.get(messagetext,"Sorry, I don't know the answer"), user2_id, user1_id)
			else:
				new_message(messagetext, user1_id, user2_id)
			return redirect(url_for('chat', user1_id=user1_id, user2_id=user2_id))
	conn = get_db_connection()
	cur = conn.cursor()
	corr = cur.execute("SELECT username FROM users WHERE userid=?", (user1_id,)).fetchall()
	if len(corr) != 1:
		abort(404)
	corr = cur.execute("SELECT username FROM users WHERE userid=?", (user2_id,)).fetchall()
	if len(corr) != 1:
		abort(404)
	corr = corr[0]['username']
	chat = cur.execute(
		"""
			SELECT *
			FROM messages
			WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
			ORDER BY messagetime
		""",
		(user1_id,user2_id, user2_id,user1_id)
	).fetchall()
	conn.close()
	return render_template('chat.html', chat=chat, users=[user1_id,user2_id], correspondent=corr, bot_msg=list(bot_msg.keys()))

@app.route('/logout')
def logout():
	session['userid'] = None
	return redirect(url_for('index'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/encryption.py')
def encryption_print():
	code = open('encryption.py','r').read()
	return f'<html><pre>\n{code}</pre></html>'

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
