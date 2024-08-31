#!/bin/bash

test_cases='/opt/kgc-2024-challenge/challenge-tool/downloads/eswc-kgc-challenge-2024/track2/'
path_unzip='./opt/kgc-2024-challenge/challenge-tool/downloads/eswc-kgc-challenge-2024/track2/'
azure_dir='/mnt/tangent-wp2/kgc-2024-challenge/'

for FOLDER in "duplicated-values" "empty-values" "gtfs-madrid-bench" "gtfs-madrid-heterogeneity" "join_1-1" "join_1-N" "join_N-1" "join_N-M" "mappings" "properties" "records" ; do
	echo $FOLDER
	test="${test_cases}${FOLDER}"
	#./challenge-tool/exectool clean --root=${test}
	docker volume prune --force
	# TODO Change to runs=5
	# ./challenge-tool/exectool run --runs=3 --root=${test} #> ${FOLDER}.log.txt
	./challenge-tool/exectool stats --root=${test}
	target="${azure_dir}${FOLDER}"
	mkdir -p $target
	rm -r ${path_unzip}${FOLDER}/${sf_name}
	unzip ${test}/results.zip
	mv ${test}/results.zip ${target}/results-${FOLDER}.zip

	for subfolder in "$test"/*/; do
  		if [ -d "$subfolder" ]; then
			sf_name=$(basename "$subfolder")
			mv "${path_unzip}${FOLDER}/${sf_name}/results/stats.csv" "${target}/results-${FOLDER}-${sf_name}.csv"
			
			export STATS_FILE="${target}/results-${FOLDER}-${sf_name}.csv"
			export TEST_CASE="${FOLDER},${sf_name}"
			python3 read_stats.py

			tar -czvf "${FOLDER}-${sf_name}.tar.gz" "${subfolder}results/run_1/mappingtemplate/out.nt"
			mv "${FOLDER}-${sf_name}.tar.gz" "${target}/"
		fi
	done
	#./challenge-tool/exectool clean --root=${test}
done
