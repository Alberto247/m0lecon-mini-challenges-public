import js2py
from base64 import b64encode
from db_utilities import get_user_seed

aes_js = open('static/js/aes.js', 'r').read() # this is the standard CryptoJS implementation, you don't need to know what's inside to solve the challenge

def xor(a, b):
	r = b''
	for c,d in zip(a,b):
		r += bytes([c^d])
	return r

def get_key_hex(user1_id, user2_id):
	k1 = get_user_seed(user1_id)
	k2 = get_user_seed(user2_id)
	if k1==None or k2==None:
		return None
	k = xor(k1,k2)
	return f'k{k.hex()}'

def encrypt(message, key):
	m64 = b64encode(message.encode('utf-8')).decode('ascii')
	return js2py.eval_js(f'{aes_js}CryptoJS.AES.encrypt("{m64}", "{key}").toString();')

def encrypt_message(message, sender, receiver):
	key = get_key_hex(sender, receiver)
	return encrypt(message, key)

