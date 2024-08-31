#!/bin/sh

append_rep_data()
{	
    ID=$1
    NUM_REP=${2:-3}

    mv ./outbox/$ID/1/time.txt ./outbox/$ID/time.txt

    for ((i=2;i<=NUM_REP;i++)); do
	tail -n 1 ./outbox/$ID/$i/time.txt >> ./outbox/$ID/time.txt
	rm -r ./outbox/$ID/$i
    done
}

exec_test()
{
    SCALE=$1
    FORMAT=$2
    NUM_REP=${3:-3}
    M_ID=$4
    CONFIG=$5
    TEST_ID="${SCALE}-${FORMAT}"

    for ((i=1;i<=NUM_REP;i++)); do
	echo "FOR ${TEST_ID} with MAPPING ${M_ID}"
	echo "EXECUTING REPETITION ${i}/${NUM_REP}"
	CONFIGS=$CONFIG TEST_ID=$TEST_ID SCALE=$SCALE FORMAT=$FORMAT REP_ID=$i MAPPINGS=$M_ID docker compose up --force-recreate morph-kgc
	docker compose down
	echo "sleeping for 2 secs"
	sleep 2
    done

    T_ID="${TEST_ID}-${M_ID}"

    append_rep_data $T_ID $NUM_REP
    echo "sleeping for 2 secs"
    sleep 2
}

docker system prune --force

# Build the rdf-template docker image
docker compose build --no-cache

# scale, format, reps, mapping, config

exec_test 1 csv 3 gtfs-csv-noselfjoin config
exec_test 10 csv 3 gtfs-csv-noselfjoin config
# exec_test 100 csv 3 gtfs-csv-noselfjoin config

exec_test 1 xml 3 gtfs-xml-noselfjoin config
exec_test 10 xml 3 gtfs-xml-noselfjoin config
# exec_test 100 xml 3 gtfs-xml-noselfjoin config

exec_test 1 json 3 gtfs-json-noselfjoin config
exec_test 10 json 3 gtfs-json-noselfjoin config
# exec_test 100 json 3 gtfs-json-noselfjoin config

