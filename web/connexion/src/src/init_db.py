import os
from db_utilities import get_db_connection
from encryption import encrypt, get_key_hex
from hashlib import sha512
from base64 import b64encode
# import secrets

connection = get_db_connection() # sqlite3.connect('database.db')

# seed0 = os.urandom(32).hex()
# seed1 = os.urandom(32).hex()
seed0 = 'bdc9c23547b44d582a72225de93d97462ca7170d18ac5d2daa14f3d8fe54bc90'
seed1 = '0e8777c6e648419c1746204e1bca858408de17673f2144acce1533400d42ddfb'

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


cur.execute("INSERT INTO users (username, passwordhash, seed) VALUES (?, ?, ?)",
	(
		'admin',
		# 'bc547750b92797f955b36112cc9bdd5cddf7d0862151d03a167ada8995aa24a9ad24610b36a68bc02da24141ee51670aea13ed6469099a4453f335cb239db5da',
		'c83228ee952112be51ae5b70fe32bbc6af0abe8c56437c9cbad59b2c9cff1bd4828542507c4d1c27d737c48435aa49824f613016e09d1102756eabc8e9fee5c1',
		seed0
	)
)

cur.execute("INSERT INTO users (username, passwordhash, seed) VALUES (?, ?, ?)",
	(
		'bot',
		# sha512(b64encode(secrets.randbits(48*8).to_bytes(48,'little'))).hexdigest(),
		# '92a891f888e79d1c2e8b82663c0f37cc6d61466c508ec62b8132588afe354712b20bb75429aa20aa3ab7cfcc58836c734306b43efd368080a2250831bf7f363f',
		'b7c7ff1331892d993ae8cdaee99917d1e265a9fd3713fc47668c7b05f333c9cfb241452b276418c645b82c464dc6cdb92c8dd4921749f140658aa4f59efb87b9',
		seed1
	)
)

connection.commit()

cur.execute("SELECT userid FROM users WHERE username=?", ('admin',))
admin = cur.fetchall()[0][0]
cur.execute("SELECT userid FROM users WHERE username=?", ('bot',))
bot = cur.fetchall()[0][0]
users = [admin,bot]
users.sort()

# print(admin)
# print(bot)

cur.execute("INSERT INTO chats (user1, user2, lastmodify) VALUES (?,?,?)",
	(
		users[0],
		users[1],
		'CURRENT_TIMESTAMP'
	)
)

cur.execute("INSERT INTO messages (sender, receiver, messagetime, messagetext) VALUES (?, ?, ?, ?)",
	(
		admin,
		bot,
		'CURRENT_TIMESTAMP',
		# "U2FsdGVkX19T4cNuCaa3bG/NfeytkUZfkQerG/+q3Yw="
		encrypt("What's the flag?", get_key_hex(admin, bot))
	)
)

cur.execute("INSERT INTO messages (sender, receiver, messagetime, messagetext) VALUES (?, ?, ?, ?)",
	(
		bot,
		admin,
		'CURRENT_TIMESTAMP',
		# "U2FsdGVkX18tzaf7SwTWlMWr8NYq8seRYoeHBHkbzaw="
		encrypt('ptm{no7_th3_r1ght_way_t0_xor_7hing5}', get_key_hex(bot, admin))
	)
)

connection.commit()
connection.close()
