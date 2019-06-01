"""
	blockchain with tokens and coinbase by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/coinbase.html

	Usage: python block3.py
	Or:    mpirun -n 4 python block3.py
"""




from hash import sha256
from block1 import Block, difficulty, pattern
from block2 import Block_v2
from blockchain import Blockchain
from mpi4py import MPI
import sys
import numpy

class Block_v3(Block_v2):

	def __init__(self, block = 0, nonce = 0, data = "", coinbase = None, tx = []):
		Block_v2.__init__(self, block, nonce, data)
		self.coinbase = coinbase
		self.tx = tx

		
	@property
	def hash(self):

		s = self.coinbase["amount"] + self.coinbase["recipient"] if self.coinbase else ""

		for t in self.tx:
			s += t['amount'] + t['from'] + t['recipient']

		if self.previous:
			s += self.previous.hash
		else:
			s += "0" * 64

		return sha256(str(self.block) + str(self.nonce) +  s )
  
	def text_hash(self, i):

		s = self.coinbase["amount"] + self.coinbase["recipient"] if self.coinbase else ""

		for t in self.tx:
			s += t['amount'] + t['from'] + t['recipient']

		if self.previous:
			s += self.previous.hash
		else:
			s += "0" * 64

		return sha256(str(self.block) + str(i) +  s)

	def show(self):
		# Your result
		print("\n=================")
		print("=== Block =======")
		print("=================\n")
		print("Block: #{}".format(self.block))
		print("Nonce: {}".format(self.nonce)) 
		if self.coinbase:
			print("Coinbase: ${} -> {}".format(self.coinbase["amount"], self.coinbase["recipient"]))
		for t in self.tx:
			print("$ {} From: {} -> {}".format(t["amount"], t["from"], t["recipient"]))
		if self.previous:
			print("Previous: {}".format(self.previous.hash))
		else:
			print("Previous: " + "0"*64)
		print("Hash: {}".format(self.hash))
		print("Valid: {}\n".format(self.valid))

## Unit test
if __name__ == "__main__":

	
	# Initialize MPI
	comm = MPI.COMM_WORLD
	size = comm.Get_size() # Returns the number of tasks in comm
	rank = comm.Get_rank()	# Returns the rank of the calling task

	bchain = Blockchain()

	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = []
	bchain.add( Block_v3(block = "1", nonce = "16651", coinbase = Coinbase, tx = Tx) )


	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "10.00", "from": "Anders", "recipient": "Sophia"},
		{"amount": "20.00", "from": "Anders", "recipient": "Lucas"},
		{"amount": "15.00", "from": "Anders", "recipient": "Emily"},
		{"amount": "15.00", "from": "Anders", "recipient": "Madison"}  ]
	bchain.add( Block_v3(block = "2", nonce = "215458", coinbase = Coinbase, tx = Tx) )

	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "10.00", "from": "Emily", "recipient": "Jackson"},
		{"amount": "5.00", "from": "Madison", "recipient": "Jackson"},
		{"amount": "20.00", "from": "Lucas", "recipient": "Grace"}  ]
	bchain.add( Block_v3(block = "3", nonce = "146", coinbase = Coinbase, tx = Tx) )

	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "15.00", "from": "Jackson", "recipient": "Ryan"},
		{"amount": "5.00", "from": "Emily", "recipient": "Madison"},
		{"amount": "8.00", "from": "Sophia", "recipient": "Jackson"}  ]
	bchain.add( Block_v3(block = "4", nonce = "18292", coinbase = Coinbase, tx = Tx) )

	Coinbase = {"amount": "100.00", "recipient": "Sophia"}  
	Tx = [{"amount": "2.00", "from": "Jackson", "recipient": "Alexander"},
		{"amount": "6.00", "from": "Ryan", "recipient": "Carter"},
		{"amount": "4.00", "from": "Ryan", "recipient": "Riley"},
		{"amount": "9.95", "from": "Grace", "recipient": "Katherine"}  ]
	bchain.add( Block_v3(block = "5", nonce = "108899", coinbase = Coinbase, tx = Tx) )

	if rank == 0:
		bchain.show()
		print("We change anders to ander in the first data")

	i = 1
	Coinbase = {"amount": "100.00", "recipient": "Ander"} 
	bchain.get_block(i).coinbase = Coinbase

	#if rank == 0:
	#	bchain.show()
		
	bchain.mine()

	if rank == 0:
		print("We mine, and get the NEW nonce for every blocks")
		bchain.show()
