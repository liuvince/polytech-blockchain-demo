"""
	blockchain by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/blockchain.html

	Usage: python blockchain.py
	Or:    mpirun -n 4 python blockchain.py
"""




from hash import sha256
from block1 import Block, difficulty, pattern
from block2 import Block_v2
from mpi4py import MPI
import sys
import numpy

class Blockchain(object):
	"""
		Blockchain class using Block class
	"""

	def __init__(self):
		self.head = self.tail = None
		self.dict = {}

	def get_block(self, i):
		return self.dict[i]

	def add(self,b):
		if self.tail == None:
			self.tail = b
		else:
			b.previous = self.head
			self.head.next = b
		self.head = b
		self.dict[int(b.block)] = b

	def mine(self):
		point = self.tail
		while point:
			point.mine()
			point = point.next

	def show(self):
		point = self.tail
		while point:
			point.show()
			point = point.next

		
## Unit test
if __name__ == "__main__":


	# Initialize MPI
	comm = MPI.COMM_WORLD
	size = comm.Get_size() # Returns the number of tasks in comm
	rank = comm.Get_rank()  # Returns the rank of the calling task

	bchain = Blockchain()

	bchain.add( Block_v2(1, 11316, "") )
	bchain.add( Block_v2(2, 35230, "") )
	bchain.add( Block_v2(3, 12937, "") )
	bchain.add( Block_v2(4, 35990, "") )
	bchain.add( Block_v2(5, 56265, "") )

	if rank == 0:
		bchain.show()

		print("We add the char 'f' to the first data")
		print("The blocks are not valid anymore\n")

	i = 1
	bchain.get_block(i).data = "f"

	if rank == 0:
		bchain.show()

	bchain.mine()

	if rank == 0:
		print("We mine the blockchain to find the good nonces")
		bchain.show()
