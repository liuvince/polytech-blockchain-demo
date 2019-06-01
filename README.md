# blockchain-demo

We tried to implement [Anders's](https://github.com/anders94) blockchain demo in Python in order to get familiar with blockchain.

## Getting Started with SHA256
```
python hash.py [your input]
```

Inspired by [Anders - Hash](https://anders.com/blockchain/hash.html)

## Block
```
python block1.py [#block] [Nonce] [Data]
```
Or, with MPI:
```
mpirun -n 4 python block1.py [#block] [Nonce] [Data]
```

Inspired by [Anders - Block](https://anders.com/blockchain/block.html)

## Blockchain
```
python blockchain.py
```
Or, with MPI:
```
mpirun -n 4 python blockchain.py
```
Inspired by [Anders - Blockchain](https://anders.com/blockchain/blockchain.html)

## Adding Tokens and Coinbase to our Blockchain
```
python block3.py
```
Or, with MPI:
```
mpirun -n 4 python block3.py
```
Inspired by [Anders - Blockchain with Tokens and Coinbase](https://anders.com/blockchain/coinbase.html)

## Adding public and private key pairs and signing to our Blockchain
```
python block4.py
```
Or, with MPI:
```
mpirun -n 4 python block4.py
```
Inspired by [Anders - public and private keys with blockchain]https://anders.com/blockchain/public-private-keys/blockchain.html)




