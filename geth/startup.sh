#!/bin/sh

geth --cache=2048 --maxpeers=40 --rpc --rpcaddr $GETH_HOST --rpcvhosts "a,b,*" --rpcport $GETH_RPC_PORT --rpcapi="eth,net,web3,personal,admin"
