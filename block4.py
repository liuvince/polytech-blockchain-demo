"""
	blockchain with tokens and coinbase by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/public-private-keys/blockchain.html

	Usage: python block4.py
	Or:    mpirun -n 4 python block4.py
"""




from hash import sha256
from block1 import Block, difficulty, pattern
from block2 import Block_v2
from blockchain import Blockchain
from mpi4py import MPI
from signature import generate_keys, sign_message, verify_message, encrypt, key_to_string
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import sys
import numpy

class Tx(object):
	def __init__(self, amount, sender_public_key, recipient_public_key, sender_private_key):
		self.amount = amount
		self.sender = sender_public_key
		self.recipient = recipient_public_key
		self.sign, _ = sign_message(str(amount) + key_to_string(sender_public_key) + key_to_string(recipient_public_key), sender_private_key)

	@property
	def valid(self):
		plaintext = str(self.amount) + key_to_string(self.sender) + key_to_string(self.recipient)
		Hash = SHA256.new(plaintext.encode()).digest()
		return verify_message(self.sign, Hash, self.sender)

	def to_string(self):
		return str(self.amount) + key_to_string(self.sender) + key_to_string(self.recipient) + str(self.sign)
	
	@property
	def sender_str(self):
		return key_to_string(self.sender)
	@property
	def recipient_str(self):
		return key_to_string(self.recipient)

class Person(object):
	def __init__(self, name):
		self.name = name
		self.public_key, self.private_key = generate_keys()
	
	@property
	def pubkey(self):
		return key_to_string(self.public_key)
	@property
	def privkey(self):
		return key_to_string(self.private_key)
  
class Block_v4(Block_v2):

	def __init__(self, block = 0, nonce = 0, data = "", coinbase = None, tx = []):
		Block_v2.__init__(self, block, nonce, data)
		self.coinbase = coinbase
		self.tx = tx

		
	@property
	def hash(self):

		s = self.coinbase["amount"] + self.coinbase["recipient"] if self.coinbase else ""

		for t in self.tx:
			s += t.to_string()

		if self.previous:
			s += self.previous.hash
		else:
			s += "0" * 64

		return sha256(str(self.block) + str(self.nonce) + s )
 
	def text_hash(self, i):

		s = self.coinbase["amount"] + self.coinbase["recipient"] if self.coinbase else ""

		for t in self.tx:
			s += t.to_string()

		if self.previous:
			s += self.previous.hash
		else:
			s += "0" * 64

		return sha256(str(self.block) + str(i) + s)

	def show(self):
		# Your result
		print("\n=================")
		print("=== Block =======")
		print("=================\n")
		print("Block: #{}".format(self.block))
		print("Nonce: {}".format(self.nonce)) 
		if self.coinbase:
			print("Coinbase: ${} -> {}".format(self.coinbase["amount"], self.coinbase["recipient"]))
		print("\n")
		for t in self.tx:
			print("$ {} From: {} ---------------------------> {} (Valid : {})\n".format(t.amount, t.recipient_str, t.sender_str,t.valid) )
		if self.previous:
			print("Previous: {}\n".format(self.previous.hash))
		else:
			print("Previous: " + "0"*64)
		print("Hash: {}\n".format(self.hash))
		print("Valid: {}\n".format(self.valid))

## Unit test
if __name__ == "__main__":

	
	# Initialize MPI
	comm = MPI.COMM_WORLD
	size = comm.Get_size() # Returns the number of tasks in comm
	rank = comm.Get_rank()	# Returns the rank of the calling task

	P1 = Person("Vincent")	
	P2 = Person("Samir")

	bchain = Blockchain()

	Coinbase = {"amount": "100.00", "recipient": P1.pubkey}  
	T = []
	bchain.add( Block_v4(block = "1", nonce = "29082", coinbase = Coinbase, tx = T) )

	Coinbase = {"amount": "100.00", "recipient": P1.pubkey}  
	T = [Tx("100", P1.public_key, P2.public_key, P1.private_key)]
	bchain.add( Block_v4(block = "1", nonce = "16651", coinbase = Coinbase, tx = T) )

	if rank == 0:
		bchain.show()
		
	bchain.mine()

	if rank == 0:
		print("We mine, and get the NEW nonce for every blocks")
		bchain.show()
