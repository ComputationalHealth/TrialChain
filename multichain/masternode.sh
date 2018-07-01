#!/bin/bash

if [ -f /root/.multichain/$CHAIN_NAME ]; then
	echo "Chain already exists, starting daemon..."
else
	multichain-util create $CHAIN_NAME -default-network-port=$CHAIN_NET_PORT -default-rpc-port=$CHAIN_RPC_PORT
	echo "rpcuser=$CHAIN_RPC_USER" > /root/.multichain/$CHAIN_NAME/multichain.conf
	echo "rpcpassword=$CHAIN_RPC_PASSWORD" >> /root/.multichain/$CHAIN_NAME/multichain.conf
	echo "rpcallowip=$CHAIN_RPC_IP" >> /root/.multichain/$CHAIN_NAME/multichain.conf
	echo "rpcallowip=$CHAIN_RPC_NB_IP" >> /root/.multichain/$CHAIN_NAME/multichain.conf
fi

multichaind $CHAIN_NAME
