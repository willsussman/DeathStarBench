sudo docker build /home/ubuntu/DeathStarBench/socialNetwork -t webhook-receiver -f /home/ubuntu/DeathStarBench/socialNetwork/Dockerfile-webhook-receiver --no-cache
make -C /home/ubuntu/DeathStarBench/wrk2

echo "Bringing up..."
sudo docker-compose up -d

# Register users and construct social graphs
cd /home/ubuntu/DeathStarBench/socialNetwork # because init_social_graph.py has relative paths
python3 /home/ubuntu/DeathStarBench/socialNetwork/scripts/init_social_graph.py \
    --graph=socfb-Reed98
    # --graph=<socfb-Reed98, ego-twitter, or soc-twitter-follows-mun>
