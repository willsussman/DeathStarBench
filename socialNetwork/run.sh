dirname=/home/ubuntu/DeathStarBench/socialNetwork/experiments/"$(date)" # --iso-8601=seconds
mkdir "$dirname"
/home/ubuntu/DeathStarBench/socialNetwork/experiment.sh "$dirname" &> "$dirname"/experiment.txt
