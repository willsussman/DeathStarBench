dirname=/home/ubuntu/DeathStarBench/socialNetwork/sweeps
mkdir "$dirname"
cd "$dirname"

threads=1
# conns=100
duration=30s
script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/compose-post.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-home-timeline.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/read-user-timeline.lua
# script=/home/ubuntu/DeathStarBench/socialNetwork/wrk2/scripts/social-network/mixed-workload.lua
urls=http://localhost:8080/wrk2-api/post/compose
# urls=http://localhost:8080/wrk2-api/home-timeline/read
# urls=http://localhost:8080/wrk2-api/user-timeline/read
# urls="http://localhost:8080/wrk2-api/post/compose http://localhost:8080/wrk2-api/home-timeline/read http://localhost:8080/wrk2-api/user-timeline/read"
# rate=100

echo "Setting defaults..."
for candidate in "${candidates[@]}" # TODO: move this to docker-compose.yml
do
    sudo docker update --memory 16G --memory-swap 16G $candidate
done

echo "Starting..."
# for i in {1..5}; do echo $i; done
for conns in {1..1001..50}; do
    mkdir "conns=$conns"
    cd "conns=$conns"
    for rate in {1..2001..50}; do
        mkdir "rate=$rate"
        cd "rate=$rate"

        echo conns=$conns rate=$rate
        /home/ubuntu/DeathStarBench/wrk2/wrk -D exp \
            -t $threads \
            -c $conns \
            -d $duration \
            -L \
            -s $script $urls \
            -R $rate \
            -P \
            > wrk.txt 2>&1
        
        cd ..
    done
    cd ..
done
