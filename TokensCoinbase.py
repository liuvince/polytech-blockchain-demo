"""
	blockchain with tokens and coinbase by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
		Inspired by: https://anders.com/blockchain/coinbase.html

		Usage: python TokensCoinbase.py
		Or:    mpirun -n 4 python TokensCoinbase.py
"""




from hash import sha256
from block import Block, difficulty, pattern
from blockchain import Blockchain
from mpi4py import MPI
import sys
import numpy

class Block_v2(Block):
	def __init__(self, block = 0, coinbase = None, tx = None, nonce = 0, previous = None):
		Block.__init__(self, block, nonce, "", previous)
		self.coinbase = coinbase
		self.tx = tx

	def update(self):
		if self.init:
			if self.previous:
				if self.previous == "0" * 64:
					self.hash = sha256(str(self.block) + str(self.nonce) +  self.data  + self.previous)
				else:
					self.hash = sha256(str(self.block) + str(self.nonce) +  self.data  + self.previous.hash)
			else:
				self.hash = sha256(str(self.block) + str(self.nonce) +  self.data)


			self.valid = (self.hash[0:difficulty] == pattern)

	@property
	def coinbase(self):
		return self.__coinbase

	@coinbase.setter
	def coinbase(self, coinbase):
		if coinbase:
			self.__coinbase = coinbase
			d = coinbase["amount"] + coinbase["recipient"]
			try:
				for t in self.tx:
					d += t["amount"] + t["from"] + t["recipient"]
			except:
				pass
			self.data = d
			self.update()
			point = self.next
			while point:
				point.update()
				point = point.next

	@property
	def tx(self):
		return self.__tx

	@tx.setter
	def tx(self, tx):
		self.__tx = tx
		try:
			d = self.coinbase["amount"] + self.coinbase["recipient"]
		except:
			d = ""
		if tx:
			for t in tx:
				d += t["amount"] + t["from"] + t["recipient"]
		self.data = d
		self.update()
		point = self.next
		while point:
			point.update()
			point = point.next


	def show(self):
		# Your result
		print("\n=================")
		print("=== Block =======")
		print("=================\n")
		print("Block: #{}".format(self.block))
		print("Nonce: {}".format(self.nonce)) 
		if self.coinbase:
			print("Coinbase: ${} -> {}".format(self.coinbase["amount"], self.coinbase["recipient"]))
		if self.tx:
			for t in self.tx:
				print("$ {} From: {} -> {}".format(t["amount"], t["from"], t["recipient"]))
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
	Tx = None
	bchain.add( Block_v2(block = "1", coinbase = Coinbase, tx = Tx, nonce = "16651") )


	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "10.00", "from": "Anders", "recipient": "Sophia"},
		{"amount": "20.00", "from": "Anders", "recipient": "Lucas"},
		{"amount": "15.00", "from": "Anders", "recipient": "Emily"},
		{"amount": "15.00", "from": "Anders", "recipient": "Madison"}  ]
	bchain.add( Block_v2(block = "2", coinbase = Coinbase, tx = Tx, nonce = "215458") )

	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "10.00", "from": "Emily", "recipient": "Jackson"},
		{"amount": "5.00", "from": "Madison", "recipient": "Jackson"},
		{"amount": "20.00", "from": "Lucas", "recipient": "Grace"}  ]
	bchain.add( Block_v2(block = "3", coinbase = Coinbase, tx = Tx, nonce = "146") )

	Coinbase = {"amount": "100.00", "recipient": "Anders"}  
	Tx = [{"amount": "15.00", "from": "Jackson", "recipient": "Ryan"},
		{"amount": "5.00", "from": "Emily", "recipient": "Madison"},
		{"amount": "8.00", "from": "Sophia", "recipient": "Jackson"}  ]
	bchain.add( Block_v2(block = "4", coinbase = Coinbase, tx = Tx, nonce = "18292") )

	Coinbase = {"amount": "100.00", "recipient": "Sophia"}  
	Tx = [{"amount": "2.00", "from": "Jackson", "recipient": "Alexander"},
		{"amount": "6.00", "from": "Ryan", "recipient": "Carter"},
		{"amount": "4.00", "from": "Ryan", "recipient": "Riley"},
		{"amount": "9.95", "from": "Grace", "recipient": "Katherine"}  ]
	bchain.add( Block_v2(block = "5", coinbase = Coinbase, tx = Tx, nonce = "108899") )

	if rank == 0:
		bchain.show()

	i = 1
	Coinbase = {"amount": "100.00", "recipient": "Ander"} 
	bchain.get_block(i).coinbase = Coinbase

	if rank == 0:
		bchain.show()
		
	bchain.mine()

	if rank == 0:
		bchain.show()
