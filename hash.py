"""
	SHA256 Hash by Vincent LIU and Samir SAYAH - MAIN - Polytech Sorbonne
	Inspired by: https://anders.com/blockchain/hash.html

	Usage: python hash.py [your_input]
"""


import hashlib
import sys 
  
def sha256(data):
    """
	.type data: str
	.rtype: str
    """
    
    result = hashlib.sha256(data.encode()) 
    return result.hexdigest()

## Unit test
if __name__ == "__main__":

	argc = len(sys.argv)

	if (argc > 1):
		Data = sys.argv[1]
	else:
		Data = "Vincent Et Samir"

	Hash = sha256(Data)

	# printing our result
	print("\n=================")
	print("== SHA256 Hash ==")
	print("=================\n") 
	print("Data: {}".format(Data))
	print("Hash: {}".format(Hash))
