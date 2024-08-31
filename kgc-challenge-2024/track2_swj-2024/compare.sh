#!/bin/bash

for FOLDER in "check-gtfs"; do #"joins" "mappings" "properties" "records"; do # "empty-values" "duplicated-values" "gtfs-madrid-bench"; do
	echo "$FOLDER"
	cd $FOLDER
	for file in *.tar.gz; do
		echo $file
		base_name=$(basename "$file" .tar.gz)
        mkdir -p "$base_name"
        tar -xzf "$file" -C "$base_name"
	done
	cd ..

	for subfolder in "$FOLDER"/*/; do
  		if [ -d "$subfolder" ]; then
			sf_name=$(basename "$subfolder")
			echo "$sf_name"
			test_case=${sf_name##*-}
			echo "$test_case"
			sort ${FOLDER}/${sf_name}/opt/kgc-2024-challenge/challenge-tool/downloads/eswc-kgc-challenge-2024/track2/${FOLDER}/${test_case}/results/run_1/mappingtemplate/out.nt | uniq > results/${FOLDER}/${test_case}/out-mappingtemplate.nt
			export MAPPING_TEMPLATE="results/${FOLDER}/${test_case}/out-mappingtemplate.nt"
			export EXPECTED="results/${FOLDER}/${test_case}/out.nt"
			python3 compare.py
		fi
	done
done