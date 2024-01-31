if [ "$#" -ne 1 ]; then
    echo "usage: experiment.sh DIRECTORY"
    exit 1
fi

dirname="$1"
echo "$dirname"

# mems=( "512M" "256M" "128M" "64M" "32M" "16M" "8M" ) # "off" # minimum: 6M
# cpus=( "1" "0.5" "0.25" "0.125" "0.0625" "0.03125" "0.015625" )
mems=( "512M" "256M" ) # "off" # minimum: 6M
cpus=( "1" "0.5" )
candidates=(
    "user-mongodb"
    "url-shorten-memcached"
    # "user-timeline-mongodb"
    # "media-mongodb"
    # "post-storage-memcached"
    # "home-timeline-redis"
    # "user-memcached"
    # "social-graph-mongodb"
    # "social-graph-redis"
    # "url-shorten-mongodb"
    # "post-storage-mongodb"
    # "user-timeline-redis"
    # "media-memcached"

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
)

# dirname=/home/ubuntu/DeathStarBench/socialNetwork/experiments/"$(date)"
# mkdir "$dirname"
# cd "$dirname"
mkdir "$dirname"/logs
mkdir "$dirname"/webhook_data
mkdir "$dirname"/combos

threads=1
conns=100
duration=30s
script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-user-timeline.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/mixed-workload.lua
urls=http://localhost:8080/wrk2-api/post/compose
# urls=http://localhost:8080/wrk2-api/home-timeline/read
# urls=http://localhost:8080/wrk2-api/user-timeline/read
# urls="http://localhost:8080/wrk2-api/post/compose http://localhost:8080/wrk2-api/home-timeline/read http://localhost:8080/wrk2-api/user-timeline/read"
rate=100
echo "/home/ubuntu/DeathStarBench/wrk2/wrk -D exp -t $threads -c $conns -d $duration -L -s $script $urls -R $rate -P" > "$dirname"/load.txt

echo "Setting defaults..." # TODO: move this to docker-compose.yml
for candidate in "${candidates[@]}"
do
    sudo docker update --memory 16G --memory-swap 16G $candidate
    sudo docker update --cpus 1 $candidate
done

# cd combos
echo "Starting..."
for candidate in "${candidates[@]}"
do
    # echo $candidate
    mkdir "$dirname"/combos/$candidate
    # cd $candidate
    for mem in "${mems[@]}"
    do
        mkdir "$dirname"/combos/$candidate/mems
        mkdir "$dirname"/combos/$candidate/mems/$mem
        # cd $mem

        echo $candidate mem=$mem

        mkdir "$dirname"/combos/$candidate/mems/$mem/bitplots
        # mkdir webhook_data

        echo "[$(date)] Buffer 30..."
        sleep 30

        echo "Working..."
        cd "$dirname"/combos/$candidate/mems/$mem
        /home/ubuntu/DeathStarBench/wrk2/wrk -D exp \
            -t $threads \
            -c $conns \
            -d $duration \
            -L \
            -s $script $urls \
            -R $rate \
            -P \
            > "$dirname"/combos/$candidate/mems/$mem/wrk.txt 2>&1 &

        echo "[$(date)] Start" > "$dirname"/combos/$candidate/mems/$mem/timing.txt

        echo "[$(date)] Sleeping 15..."
        sleep 15

        echo "Injecting..."
        # if [ "$mem" = "off" ]; then
        #     echo "[$(date)] sudo docker stop $candidate" >> "$dirname"/combos/$candidate/$mem/timing.txt
        #     tail -n 1 "$dirname"/combos/$candidate/$mem/timing.txt
        #     sudo docker stop $candidate
        # else
        echo "[$(date)] sudo docker update --memory $mem --memory-swap $mem $candidate" >> "$dirname"/combos/$candidate/mems/$mem/timing.txt
        tail -n 1 "$dirname"/combos/$candidate/mems/$mem/timing.txt
        sudo docker update --memory $mem --memory-swap $mem $candidate
        # fi

        echo "[$(date)] Sleeping 15..."
        sleep 15

        echo "[$(date)] Stop" >> "$dirname"/combos/$candidate/mems/$mem/timing.txt

        echo "Restoring..."
        # if [ "$mem" = "off" ]; then
        #     sudo docker start $candidate
        # else
        sudo docker update --memory 16G --memory-swap 16G $candidate
        sudo docker restart $candidate
        # fi

        echo "Saving..."
        sudo docker ps -a &> "$dirname"/combos/$candidate/mems/$mem/ps.txt
        # curl -o webhook_data.txt http://localhost:5000/query-file # -s for silent

        # echo "Parsing..."
        # python /home/ubuntu/DeathStarBench/socialNetwork/parse.py "$dirname" $candidate $mem &> "$dirname"/combos/$candidate/$mem/parse.txt
        # cd ..
    done
    # cd ..

    # echo $candidate
    # mkdir "$dirname"/combos/$candidate
    # cd $candidate
    for cpu in "${cpus[@]}"
    do
        mkdir "$dirname"/combos/$candidate/cpu
        mkdir "$dirname"/combos/$candidate/cpu/$cpu
        # cd $mem

        echo $candidate cpu=$cpu

        mkdir "$dirname"/combos/$candidate/cpu/$cpu/bitplots
        # mkdir webhook_data

        echo "[$(date)] Buffer 30..."
        sleep 30

        echo "Working..."
        cd "$dirname"/combos/$candidate/cpu/$cpu
        /home/ubuntu/DeathStarBench/wrk2/wrk -D exp \
            -t $threads \
            -c $conns \
            -d $duration \
            -L \
            -s $script $urls \
            -R $rate \
            -P \
            > "$dirname"/combos/$candidate/cpu/$cpu/wrk.txt 2>&1 &

        echo "[$(date)] Start" > "$dirname"/combos/$candidate/cpu/$cpu/timing.txt

        echo "[$(date)] Sleeping 15..."
        sleep 15

        echo "Injecting..."
        # if [ "$mem" = "off" ]; then
        #     echo "[$(date)] sudo docker stop $candidate" >> "$dirname"/combos/$candidate/$mem/timing.txt
        #     tail -n 1 "$dirname"/combos/$candidate/$mem/timing.txt
        #     sudo docker stop $candidate
        # else
        echo "[$(date)] sudo docker update --cpus $cpu $candidate" >> "$dirname"/combos/$candidate/$cpu/timing.txt
        tail -n 1 "$dirname"/combos/$candidate/cpu/$cpu/timing.txt
        sudo docker update --cpus $cpu $candidate
        # fi

        echo "[$(date)] Sleeping 15..."
        sleep 15

        echo "[$(date)] Stop" >> "$dirname"/combos/$candidate/cpu/$cpu/timing.txt

        echo "Restoring..."
        # if [ "$mem" = "off" ]; then
        #     sudo docker start $candidate
        # else
        sudo docker update --cpus 1 $candidate
        sudo docker restart $candidate
        # fi

        echo "Saving..."
        sudo docker ps -a &> "$dirname"/combos/$candidate/cpu/$cpu/ps.txt
        # curl -o webhook_data.txt http://localhost:5000/query-file # -s for silent

        # echo "Parsing..."
        # python /home/ubuntu/DeathStarBench/socialNetwork/parse.py "$dirname" $candidate $mem &> "$dirname"/combos/$candidate/$mem/parse.txt
        # cd ..
    done
    # cd ..
done
# cd ..

echo "Saving webhook data..."
# cd webhook_data
curl -s -o "$dirname"/webhook_data/user_mongodb_webhook_data.txt http://localhost:5000/user-mongodb-query-file
curl -s -o "$dirname"/webhook_data/url_shorten_memcached_webhook_data.txt http://localhost:5000/url-shorten-memcached-query-file
# curl -s -o "$dirname"/webhook_data/user_timeline_mongodb_webhook_data.txt http://localhost:5000/user-timeline-mongodb-query-file
# curl -s -o "$dirname"/webhook_data/media_mongodb_webhook_data.txt http://localhost:5000/media-mongodb-query-file
# curl -s -o "$dirname"/webhook_data/post_storage_memcached_webhook_data.txt http://localhost:5000/post-storage-memcached-query-file
# curl -s -o "$dirname"/webhook_data/home_timeline_redis_webhook_data.txt http://localhost:5000/home-timeline-redis-query-file
# curl -s -o "$dirname"/webhook_data/user_memcached_webhook_data.txt http://localhost:5000/user-memcached-query-file
# curl -s -o "$dirname"/webhook_data/social_graph_mongodb_webhook_data.txt http://localhost:5000/social-graph-mongodb-query-file
# curl -s -o "$dirname"/webhook_data/social_graph_redis_webhook_data.txt http://localhost:5000/social-graph-redis-query-file
# curl -s -o "$dirname"/webhook_data/url_shorten_mongodb_webhook_data.txt http://localhost:5000/url-shorten-mongodb-query-file
# curl -s -o "$dirname"/webhook_data/post_storage_mongodb_webhook_data.txt http://localhost:5000/post-storage-mongodb-query-file
# curl -s -o "$dirname"/webhook_data/user_timeline_redis_webhook_data.txt http://localhost:5000/user-timeline-redis-query-file
# curl -s -o "$dirname"/webhook_data/media_memcached_webhook_data.txt http://localhost:5000/media-memcached-query-file

# curl -s -o "$dirname"/webhook_data/social_graph_service_webhook_data.txt http://localhost:5000/social-graph-service-query-file
# curl -s -o "$dirname"/webhook_data/compose_post_service_webhook_data.txt http://localhost:5000/compose-post-service-query-file
# curl -s -o "$dirname"/webhook_data/post_storage_service_webhook_data.txt http://localhost:5000/post-storage-service-query-file
# curl -s -o "$dirname"/webhook_data/user_timeline_service_webhook_data.txt http://localhost:5000/user-timeline-service-query-file
# curl -s -o "$dirname"/webhook_data/url_shorten_service_webhook_data.txt http://localhost:5000/url-shorten-service-query-file
# curl -s -o "$dirname"/webhook_data/user_service_webhook_data.txt http://localhost:5000/user-service-query-file
# curl -s -o "$dirname"/webhook_data/media_service_webhook_data.txt http://localhost:5000/media-service-query-file
# curl -s -o "$dirname"/webhook_data/text_service_webhook_data.txt http://localhost:5000/text-service-query-file
# curl -s -o "$dirname"/webhook_data/unique_id_service_webhook_data.txt http://localhost:5000/unique-id-service-query-file
# curl -s -o "$dirname"/webhook_data/user_mention_service_webhook_data.txt http://localhost:5000/user-mention-service-query-file
# curl -s -o "$dirname"/webhook_data/home_timeline_service_webhook_data.txt http://localhost:5000/home-timeline-service-query-file
# # curl -s -o "$dirname"/webhook_data/nginx_thrift_webhook_data.txt http://localhost:5000/nginx-thrift-query-file
# # curl -s -o "$dirname"/webhook_data/media_frontend_webhook_data.txt http://localhost:5000/media-frontend-query-file

echo "Parsing..."
/home/ubuntu/DeathStarBench/socialNetwork/reparse.sh "$dirname" &> "$dirname"/reparse.txt
echo "Summarizing..."
python /home/ubuntu/DeathStarBench/socialNetwork/summary.py "$dirname" &> "$dirname"/summary.txt

echo "Saving logs..."
sudo docker ps -a &> "$dirname"/final_ps.txt
IFS=$'\n' read -d '' -r -a containers < <(awk '{print $NF}' "$dirname"/final_ps.txt)
for container in "${containers[@]:1}"; do
    echo "$container"
    sudo docker logs --timestamps "$container" &> "$dirname"/logs/"$container".log
done

echo "Done!"
