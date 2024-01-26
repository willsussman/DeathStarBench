echo "Taking down..."
# cd /home/ubuntu/DeathStarBench/socialNetwork
# cd ../../..
sudo docker-compose down --remove-orphans
yes | sudo docker volume prune