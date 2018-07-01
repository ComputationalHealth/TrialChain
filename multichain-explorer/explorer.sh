#!/bin/bash

multichaind $CHAIN_NAME@$CHAIN_MASTER:$CHAIN_NET_PORT -daemon 1 

echo "rpcuser=$CHAIN_RPC_USER" > /root/.multichain/$CHAIN_NAME/multichain.conf
echo "rpcpassword=$CHAIN_RPC_PASSWORD" >> /root/.multichain/$CHAIN_NAME/multichain.conf
echo "rpcallowip=$CHAIN_RPC_IP" >> /root/.multichain/$CHAIN_NAME/multichain.conf
echo "rpcport=$CHAIN_RPC_PORT" >> /root/.multichain/$CHAIN_NAME/multichain.conf

cd /root/multichain-explorer && python -m Mce.abe --config chain.conf --commit-bytes 100000 --no-serve

python -m Mce.abe --config chain.conf
