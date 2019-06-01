"""	
	Public/Private key signatures by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/hash.html
	Usage: python .py [your_input]
"""

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256




def generate_keys():
	"""
	Returns private & public keys
	generated with the RSA algorithm
	"""
	random_generator = Random.new().read
	private_key = RSA.generate(1024, random_generator)
	public_key = private_key.publickey()
	return public_key, private_key



def sign_message(plaintext, private_key):
	"""
	Returns the signature of a message using the private key
	"""
	Hash = SHA256.new(plaintext.encode()).digest()
	return private_key.sign(Hash, ''), Hash
	


def verify_message(signature, Hash, public_key):
	"""
	Verify that the message has been signed by the right private key
	"""
	return public_key.verify(Hash, signature)


def encrypt(public_key, plaintext):
	"""
	Encrypt a message using the RSA standard
	"""
	cipher_rsa = PKCS1_OAEP.new(public_key)
	cipher_text = cipher_rsa.encrypt(plaintext.encode())
	return cipher_text


def decrypt(private_key, cipher_text):
	"""
	Decrypt a message encrypted with the RSA standard
	"""
	cipher_rsa = PKCS1_OAEP.new(private_key)
	plaintext = cipher_rsa.decrypt(cipher_text)
	return plaintext

def key_to_string(key):
	s = key.exportKey("PEM")
	s = s.split("\n")
	s = s[1:-1]
	s = "".join(s)
	return s

a, b = generate_keys()
print(a.exportKey("PEM"))
print(key_to_string(a))
