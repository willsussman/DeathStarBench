if [ "$#" -ne 1 ]; then
    echo "usage: reparse.sh DIRECTORY"
    exit 1
fi


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
    for mem in "${mems[@]}"
    do
        echo $candidate mem=$mem
        echo "Parsing..."
        python /home/ubuntu/DeathStarBench/socialNetwork/parse.py "$dirname" $candidate mem $mem &> "$dirname"/combos/$candidate/$mem/parse.txt
    done

    for cpu in "${cpus[@]}"
    do
        echo $candidate cpu=$cpu
        echo "Parsing..."
        python /home/ubuntu/DeathStarBench/socialNetwork/parse.py "$dirname" $candidate cpu $cpu &> "$dirname"/combos/$candidate/$cpu/parse.txt
    done
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
