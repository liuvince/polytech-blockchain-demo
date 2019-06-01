"""
	blockchain by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/blockchain.html
"""


from hash import sha256
from block1 import Block, difficulty, pattern

class Block_v2(Block):
	"""
		Block with previous attribute
	"""

	def __init__(self, block = 0, nonce = 0, data = ""):
		Block.__init__(self, block, nonce, data)
		self.previous = self.next = None
	
	@property
	def hash(self):
		s = self.previous.hash if self.previous else "0" * 64
		return sha256(str(self.block) + str(self.nonce) +  str(self.data) + s)
  
	def text_hash(self, i):
		s = self.previous.hash if self.previous else "0" * 64
		return sha256(str(self.block) + str(i) + str(self.data) +  s)

	def show(self):
                # Your result
                print("\n=================")
                print("===== Block =====")
                print("=================\n")
                print("Block: #{}".format(self.block))
                print("Nonce: {}".format(self.nonce))
                print("Data: {}".format(self.data))
		if self.previous:
			print("Previous: {}".format(self.previous.hash))
		else:
			print("Previous: " + "0" * 64)
                print("Hash: {}".format(self.hash))
                print("Valid: {}\n".format(self.valid))

