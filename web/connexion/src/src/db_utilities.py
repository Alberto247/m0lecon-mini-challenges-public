import sqlite3

def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

def get_user_seed(userid):
	conn = get_db_connection()
	cur = conn.cursor()
	k1 = cur.execute("SELECT seed FROM users WHERE userid=?",(userid,)).fetchall()
	conn.close()
	if(len(k1) != 1):
		return None
	return bytes.fromhex(k1[0]['seed'])
