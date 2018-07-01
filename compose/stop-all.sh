docker-compose -f explorer-compose.yml -p tc_explorer down
docker-compose -f client-compose.yml -p tc_client down
docker-compose -f master-compose.yml -p tc_master down -v 
