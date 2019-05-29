"""
	Block by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/block.html

	Usage: python block.py [#block] [Nonce] [Data]
		Or:    mpirun -n 4 python block.py [#block] [Nonce] [Data]
"""

	
	

from hash import sha256
from mpi4py import MPI
import sys
import numpy 

difficulty = 4
pattern = "0" * difficulty

class Block(object):
	"""
	Building blocks of the Blockchain
	"""
	def __init__(self, block = 0, nonce = 0, data = "", previous = None):
		self.init = False
		self.next = None

		self.block = block
		self.nonce = nonce
		self.data = data
		self.previous = previous 
		
		if self.previous:
			if self.previous == "0" * 64:
				self.hash = sha256(str(self.block) + str(self.nonce) +  self.data  + self.previous)
			else:
				self.hash = sha256(str(self.block) + str(self.nonce) +  self.data  + self.previous.hash)
		else:
			self.hash = sha256(str(self.block) + str(self.nonce) +  self.data)


		self.valid = (self.hash[0:difficulty] == pattern)
		self.init = True


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
	def block(self):
		return self.__block

	@block.setter
	def block(self, block):
		self.__block = block
		self.update()
		point = self.next
		while point:
			point.update()
			point = point.next

	@property
	def nonce(self):
		return self.__nonce

	@nonce.setter
	def nonce(self, nonce):
		self.__nonce = nonce
		self.update()
		point = self.next
		while point:
			point.update()
			point = point.next

	@property
	def data(self):
		return self.__data

	@data.setter
	def data(self, data):
		self.__data = data
		self.update()
		point = self.next
		while point:
			point.update()
			point = point.next

	@property
	def previous(self):
		return self.__previous

	@previous.setter
	def previous(self, previous):
		self.__previous = previous
		self.update()
		point = self.next
		while point:
			point.update()
			point = point.next

	@property
	def hash(self):
		return self.__hash

	@hash.setter
	def hash(self, Hash):
		self.__hash = Hash
		point = self.next
		while point:
			point.update()
			point = point.next

	@property
	def next(self):
		return self.__next

	@next.setter
	def next(self, Next):
		self.__next = Next

	def mine(self):
		"""
		We are looking for a nonce number which make our hash starts with "0000"
	"""

		# Initialize MPI
		comm = MPI.COMM_WORLD
		size = comm.Get_size() # Returns the number of tasks in comm
		rank = comm.Get_rank()	# Returns the rank of the calling task

		rd = 0 # "Round"
		end = 0 

		start = rank * 10000
		status = MPI.Status()

		while(end == False):
			imin = rd * 10000 * size + start

			#print(rank, imin,imin + 10000)
			for i in range(imin, imin + 10000):

				if self.previous:
					if self.previous == "0" * 64:
						text_hash = sha256(str(self.block) + str(i) +  self.data  + self.previous)
					else:
						text_hash = sha256(str(self.block) + str(i) +  self.data  + self.previous.hash)
				else:
					text_hash = sha256(str(self.block) + str(i) +  self.data)

				s = comm.Iprobe(source = MPI.ANY_SOURCE, tag = 42, status = status)
				if s:
					data = comm.recv( source=status.source, tag = 42)
					#self.hash = data['hash']
					self.nonce = str(data['nonce'])
					end = True
					break	
				if (text_hash[0:difficulty] == pattern):
					#self.hash = text_hash
					self.nonce = str(i)
					for dst in range(size):
						if dst != rank:
							data = {'nonce': i, 'hash': text_hash}
							comm.send(data, dest = dst, tag = 42)
					end = True
					break	
			rd += 1

		self.valid = True

	def show(self):
		# Your result
		print("\n=================")
		print("=== Block =======")
		print("=================\n")
		print("Block: #{}".format(self.block))
		print("Nonce: {}".format(self.nonce)) 
		print("Data: {}".format(self.data))
		print("Hash: {}".format(self.hash))
		print("Valid: {}\n".format(self.valid))

## Unit test
if __name__ == "__main__":

	
	# Initialize MPI
	comm = MPI.COMM_WORLD
	size = comm.Get_size() # Returns the number of tasks in comm
	rank = comm.Get_rank()	# Returns the rank of the calling task
	argc = len(sys.argv)

	if (argc > 3):
		Block_num = sys.argv[1]
		Nonce = sys.argv[2]
		Data = sys.argv[3]
	else:
		Block_num = "1"
		Nonce = "72608"
		Data = ""
	
	block = Block(Block_num, Nonce, Data, None)

	if rank == 0:	
		block.show()

	block.mine()
	
	if rank == 0:
		block.show()

