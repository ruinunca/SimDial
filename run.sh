#!/bin/bash

set -exu

for idx in 0 1 2 3 4 5 6 7 8 9; do
	# # generate the training & test data
	python multiple_domains.py $idx 1500

	# # generate the adaptation data
	for data_size in 15; do
		python multiple_domains.py $idx $data_size

		cd ./1500_data_fixed_${idx}/

		# # combine dialog log
		cat restaurant-MixSpec-1500.json weather-MixSpec-1500.json bus-MixSpec-1500.json > r_w_b.json
		sed -i 's/\]\[/,/g' r_w_b.json
		cat r_w_b.json movie-MixSpec-${data_size}.json > r_w_b_${data_size}m.json
		sed -i 's/\]\[/,/g' r_w_b_${data_size}m.json 


		# # combine database
		cat restaurant-MixSpec-1500-DB.json weather-MixSpec-1500-DB.json bus-MixSpec-1500-DB.json >r_w_b-DB.json 
		sed -i 's/\]\[/,/g' r_w_b-DB.json
		cat r_w_b-DB.json movie-MixSpec-${data_size}-DB.json > r_w_b_${data_size}m-DB.json 
		sed -i 's/\]\[/,/g' r_w_b_${data_size}m-DB.json


		# # combine OTGY(slot values) file
		if [ -f "../1500_data_fixed_0/r_w_b-OTGY.json" ]; then
			cp -f ../1500_data_fixed_0/r_w_b-OTGY.json ./
		else
			python3 ../combine_domain.py -data_path ./ -target_domain ''
		fi

		if [ -f "../1500_data_fixed_0/r_w_b_${data_size}m-OTGY.json" ]; then
			cp -f ../1500_data_fixed_0/r_w_b_${data_size}m-OTGY.json ./r_w_b_${data_size}m-OTGY.json
		else
			python3 ../combine_domain.py -data_path ./
		fi

		cd ../

	done
done



