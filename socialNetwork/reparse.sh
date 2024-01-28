if [ "$#" -ne 1 ]; then
    echo "usage: reparse.sh DIRECTORY"
    exit 1
fi


mems=( "512M" "256M" "128M" "64M" "32M" "16M" "8M" ) # minimum: 6M
# mems=( "512M" "256M" )
candidates=(
    "user-mongodb"
    "url-shorten-memcached"
    "user-timeline-mongodb"
    "media-mongodb"
    "post-storage-memcached"
    "home-timeline-redis"
    "user-memcached"
    "social-graph-mongodb"
    "social-graph-redis"
    "url-shorten-mongodb"
    "post-storage-mongodb"
    "user-timeline-redis"
    "media-memcached"

    # "social-graph-service"
    # "compose-post-service"
    # "post-storage-service"
    # "user-timeline-service"
    # "url-shorten-service"
    # "user-service"
    # "media-service"
    # "text-service"
    # "unique-id-service"
    # "user-mention-service"
    # "home-timeline-service"
    # "nginx-thrift"
    # "media-frontend"
)

dirname="$1"
# mkdir "$dirname"
# cd "$dirname"
# mkdir logs

# threads=1
# conns=100
# duration=30s
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua
# # script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua
# # script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-user-timeline.lua
# # script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/mixed-workload.lua
# urls=http://localhost:8080/wrk2-api/post/compose
# # urls=http://localhost:8080/wrk2-api/home-timeline/read
# # urls=http://localhost:8080/wrk2-api/user-timeline/read
# # urls="http://localhost:8080/wrk2-api/post/compose http://localhost:8080/wrk2-api/home-timeline/read http://localhost:8080/wrk2-api/user-timeline/read"
# rate=100
# echo "/home/ubuntu/DeathStarBench/wrk2/wrk -D exp -t $threads -c $conns -d $duration -L -s $script $urls -R $rate -P" > "$dirname"/load.txt

# echo "Setting defaults..."
# for candidate in "${candidates[@]}" # TODO: move this to docker-compose.yml
# do
#     sudo docker update --memory 16G --memory-swap 16G $candidate
# done

# echo "Starting..."
for candidate in "${candidates[@]}"
do
    # echo $candidate
    # mkdir $candidate
    # cd $candidate
    for mem in "${mems[@]}"
    do
        # mkdir $mem
        # cd $mem

        echo $candidate $mem

        # mkdir bitplots
        # mkdir webhook_data

        # echo "Working..."
        # /home/ubuntu/DeathStarBench/wrk2/wrk -D exp \
        #     -t $threads \
        #     -c $conns \
        #     -d $duration \
        #     -L \
        #     -s $script $urls \
        #     -R $rate \
        #     -P \
        #     > "$dirname"/combos/$candidate/$mem/wrk.txt 2>&1 &

        # echo "[$(date)] Start" > "$dirname"/combos/$candidate/$mem/timing.txt

        # echo "[$(date)] Sleeping 15..."
        # sleep 15

        # echo "Injecting..."
        # echo "[$(date)] sudo docker update --memory $mem --memory-swap $mem $candidate" >> "$dirname"/combos/$candidate/$mem/timing.txt
        # tail -n 1 "$dirname"/combos/$candidate/$mem/timing.txt
        # sudo docker update --memory $mem --memory-swap $mem $candidate

        # echo "[$(date)] Sleeping 15..."
        # sleep 15

        # echo "[$(date)] Stop" >> "$dirname"/combos/$candidate/$mem/timing.txt

        # echo "Restoring default..."
        # sudo docker update --memory 16G --memory-swap 16G $candidate

        # echo "Saving..."
        # # curl -o webhook_data.txt http://localhost:5000/query-file # -s for silent
        # cd webhook_data
        # curl -s -o user_mongodb_webhook_data.txt http://localhost:5000/user-mongodb-query-file
        # curl -s -o url_shorten_memcached_webhook_data.txt http://localhost:5000/url-shorten-memcached-query-file
        # curl -s -o user_timeline_mongodb_webhook_data.txt http://localhost:5000/user-timeline-mongodb-query-file
        # curl -s -o media_mongodb_webhook_data.txt http://localhost:5000/media-mongodb-query-file
        # curl -s -o post_storage_memcached_webhook_data.txt http://localhost:5000/post-storage-memcached-query-file
        # curl -s -o home_timeline_redis_webhook_data.txt http://localhost:5000/home-timeline-redis-query-file
        # curl -s -o user_memcached_webhook_data.txt http://localhost:5000/user-memcached-query-file
        # curl -s -o social_graph_mongodb_webhook_data.txt http://localhost:5000/social-graph-mongodb-query-file
        # curl -s -o social_graph_redis_webhook_data.txt http://localhost:5000/social-graph-redis-query-file
        # curl -s -o url_shorten_mongodb_webhook_data.txt http://localhost:5000/url-shorten-mongodb-query-file
        # curl -s -o post_storage_mongodb_webhook_data.txt http://localhost:5000/post-storage-mongodb-query-file
        # curl -s -o user_timeline_redis_webhook_data.txt http://localhost:5000/user-timeline-redis-query-file
        # curl -s -o media_memcached_webhook_data.txt http://localhost:5000/media-memcached-query-file
        # cd ..
        # sudo docker ps -a &> "$dirname"/combos/$candidate/$mem/ps.txt

        echo "Parsing..."
        python /home/ubuntu/DeathStarBench/socialNetwork/parse.py "$dirname" $candidate $mem &> "$dirname"/combos/$candidate/$mem/parse.txt
        # cd ..
    done
    # cd ..
done

echo "Done!"
# echo "Summarizing..."
# python /home/ubuntu/DeathStarBench/socialNetwork/summary.py "$dirname" &> "$dirname"/summary.txt

# echo "Saving logs..."
# sudo docker ps -a &> "$dirname"/final_ps.txt
# IFS=$'\n' read -d '' -r -a containers < <(awk '{print $NF}' "$dirname"/final_ps.txt)
# for container in "${containers[@]:1}"; do
#     echo "$container"
#     sudo docker logs --timestamps "$container" &> logs/"$container".log
# done