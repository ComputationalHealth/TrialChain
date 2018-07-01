FROM ubuntu:16.04

RUN apt-get -qqy update && apt-get -qqy install vim wget

WORKDIR /root

RUN wget https://www.multichain.com/download/multichain-1.0.2.tar.gz
RUN tar -xvzf multichain-1.0.2.tar.gz && rm -rf multichain-1.0.2.tar.gz

COPY masternode.sh /root/masternode.sh
COPY clientnode.sh /root/clientnode.sh

RUN mv multichain-1.0.2/multichaind multichain-1.0.2/multichain-cli multichain-1.0.2/multichain-util /usr/local/bin \
	&& mkdir /root/.multichain \
	&& chmod +x masternode.sh \
	&& chmod +x clientnode.sh

ENV CHAIN_NAME=defaultchain
ENV CHAIN_NET_PORT=8570
ENV CHAIN_RPC_PORT=8571
ENV CHAIN_MASTER=multichain-master

ENV CHAIN_RPC_USER=rpcuser
ENV CHAIN_RPC_PASSWORD=CHANGEME
ENV CHAIN_RPC_IP=10.5.0.0/24

EXPOSE 8570
EXPOSE 8571

ENTRYPOINT './masternode.sh'