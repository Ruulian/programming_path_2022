FILES=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/*/run.sh
FILES_ARRAY=( $FILES )
NB=${#FILES_ARRAY[@]}
DONE=0
for i in ${FILES}
do
    bash $i
    echo -ne "\r[\x1b[92m+\x1b[0m] Deploying challenges "
    for h in $(seq 1 $(($DONE*10)));
    do
        echo -ne "#"
    done
    
    ((DONE=DONE+1))
    POURCENT=$(bc <<<"scale=0; (($DONE*100)) /$NB")

    for t in $(seq 1 $((($NB - $DONE)*10)));
    do 
        echo -ne "."
    done
    echo -ne "($POURCENT%)"
    sleep 2
done
echo -ne "\n[\x1b[92m+\x1b[0m] Challenges successfully deployed\n"