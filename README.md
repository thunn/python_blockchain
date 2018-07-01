# Instructions

Run server by navigating to the repo directory and running `python server.py` this will 
run a flask server on the local machine (ensure [Flask](https://github.com/pallets/flask) is installed).

To send a transaction:
	`curl "localhost:5000/txion" \
     	-H "Content-Type: application/json" \
     	-d '{"from": "NAME1", "to":"NAME2", "amount": 1}'`

To mine a block:
	`curl localhost:5000/mine`

To review the blockchain:
	`curl localhost:5000/blocks`

This code was created based on a tutorial by [Gerald Nash](https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b)

