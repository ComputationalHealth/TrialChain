FROM ethereum/client-go:v1.8.6

ENV GETH_HOST=localhost
ENV GETH_RPC_PORT=8545

WORKDIR /root

COPY startup.sh startup.sh
RUN chmod +x startup.sh

EXPOSE 30303
EXPOSE 8545

ENTRYPOINT "/root/startup.sh"
