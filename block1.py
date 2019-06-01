"""
	Block by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/block.html

	Usage: python block1.py [#block] [Nonce] [Data]
	Or:    mpirun -n 4 python block1.py [#block] [Nonce] [Data]
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
	def __init__(self, block = 0, nonce = 0, data = ""):

		self.block = block
		self.nonce = nonce
		self.data = data
			
	@property
	def hash(self):
		return sha256(str(self.block) + str(self.nonce) +  self.data)

	@property
	def valid(self):
		return self.hash[:difficulty] == pattern

	def text_hash(self, i):
		return sha256(str(self.block) + str(i) +  self.data)

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

    			text_hash = self.text_hash(i)

    			flag = comm.Iprobe(source = MPI.ANY_SOURCE, tag = 42, status = status)
		    	if flag:
		    		data = comm.recv( source=status.source, tag = 42)
	    			self.nonce = str(data['nonce'])
                                end = True
                                break
			if (text_hash[0:difficulty] == pattern):
				self.nonce = str(i)
				for dst in range(size):
			        	if dst != rank:
			    			data = {'nonce': i}
		    				comm.send(data, dest = dst, tag = 42)
                                end = True
				break	
		rd += 1


	def show(self):
		# Your result
		print("\n=================")
		print("===== Block =====")
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
		Nonce = ""
		Data = ""

	# Create a Block object with given parameters	
	block = Block(Block_num, Nonce, Data)

	if rank == 0:
		print("\nBefore mining:")
		block.show()

	block.mine()
	
	if rank == 0:
		print("After mining:")
		block.show()

