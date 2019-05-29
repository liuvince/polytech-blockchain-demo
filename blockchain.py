"""
	blockchain by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
		Inspired by: https://anders.com/blockchain/blockchain.html

		Usage: python blockchain.py
		Or:    mpirun -n 4 python blockchain.py
"""




from hash import sha256
from block import Block, difficulty, pattern
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
			b.previous = "0" * 64
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

	bchain.add( Block(1, 11316, "") )
	bchain.add( Block(2, 35230, "") )
	bchain.add( Block(3, 12937, "") )
	bchain.add( Block(4, 35990, "") )
	bchain.add( Block(5, 56265, "") )

	if rank == 0:
		bchain.show()

	i = 1
	bchain.get_block(i).data = "f"

	if rank == 0:
		bchain.show()

	bchain.mine()

	if rank == 0:
		bchain.show()
