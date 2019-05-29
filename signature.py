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
	Building blocks of the Blockchain
	"""
	random_generator = Random.new().read
	private_key = RSA.generate(1024, random_generator)
	public_key = private_key.publickey()

plaintext = 'data'
cipher_rsa = PKCS1_OAEP.new(public_key)
cipher_text = cipher_rsa.encrypt(plaintext.encode())


cipher_rsa2 = PKCS1_OAEP.new(private_key)
rec = cipher_rsa2.decrypt(cipher_text)

print(rec)



hash = SHA256.new(plaintext.encode()).digest()

signature = private_key.sign(hash, '')
print(public_key.verify(hash, signature))

