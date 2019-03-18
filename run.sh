#!/bin/bash

set -exu

for idx in 0; do
	for data_size in 150; do
		# python multiple_domains.py $idx $data_size

		cd ./1500_data_fixed_${idx}/
		cat restaurant-MixSpec-1500.json weather-MixSpec-1500.json bus-MixSpec-1500.json > r_w_b.json
		cat restaurant-MixSpec-1500-DB.json weather-MixSpec-1500-DB.json bus-MixSpec-1500-DB.json >r_w_b-DB.json 

		sed -i 's/\]\[/,/g' r_w_b-DB.json
		sed -i 's/\]\[/,/g' r_w_b.json
		cp ../1500_data_fixed_2/r_w_b-OTGY.json ./

		cat r_w_b.json movie-MixSpec-${data_size}.json rest_pitt-MixSpec-${data_size}.json > r_w_b_${data_size}m_${data_size}rslot.json
		cat r_w_b-DB.json movie-MixSpec-${data_size}-DB.json rest_pitt-MixSpec-${data_size}-DB.json > r_w_b_${data_size}m_${data_size}rslot-DB.json 

		sed -i 's/\]\[/,/g' r_w_b_${data_size}m_${data_size}rslot.json 
		sed -i 's/\]\[/,/g' r_w_b_${data_size}m_${data_size}rslot-DB.json
		cp ../1500_data_fixed_2/r_w_b_15m_15rslot-OTGY.json ./r_w_b_${data_size}m_${data_size}rslot-OTGY.json

		cd ../

	done
done

# for idx in 0; do
# 	for data_size in 150; do
# 		python multiple_domains.py $idx $data_size

# 		cd ./1500_data_fixed_${idx}/

# 		cat restaurant-MixSpec-1500.json bus-MixSpec-1500.json movie-MixSpec-1500.json > r_b_m.json
# 		cat restaurant-MixSpec-1500-DB.json bus-MixSpec-1500-DB.json movie-MixSpec-1500-DB.json >r_b_m-DB.json 

# 		sed -i 's/\]\[/,/g' r_b_m-DB.json
# 		sed -i 's/\]\[/,/g' r_b_m.json
# 		cp ../1500_data_fixed_2/r_b_m-OTGY.json ./

# 		cat r_b_m.json weather-MixSpec-${data_size}.json > r_b_m_${data_size}w.json
# 		cat r_b_m-DB.json weather-MixSpec-${data_size}-DB.json > r_b_m_${data_size}w-DB.json 

# 		sed -i 's/\]\[/,/g' r_b_m_${data_size}w.json 
# 		sed -i 's/\]\[/,/g' r_b_m_${data_size}w-DB.json
# 		cp ../1500_data_fixed_2/r_b_m_15w-OTGY.json ./r_b_m_${data_size}w-OTGY.json

# 		cd ../

# 	done
# done

# for idx in 2; do
# 	for data_size in 15; do
# 		# python multiple_domains.py $idx $data_size

# 		cd ./1500_data_fixed_${idx}/

# 		cat restaurant-MixSpec-1500.json weather-MixSpec-1500.json movie-MixSpec-1500.json > r_w_m.json
# 		cat restaurant-MixSpec-1500-DB.json weather-MixSpec-1500-DB.json movie-MixSpec-1500-DB.json >r_w_m-DB.json 

# 		sed -i 's/\]\[/,/g' r_w_m-DB.json
# 		sed -i 's/\]\[/,/g' r_w_m.json

# 		cat r_w_m.json bus-MixSpec-${data_size}.json > r_w_m_${data_size}b.json
# 		cat r_w_m-DB.json bus-MixSpec-${data_size}-DB.json > r_w_m_${data_size}b-DB.json 

# 		sed -i 's/\]\[/,/g' r_w_m_${data_size}b.json 
# 		sed -i 's/\]\[/,/g' r_w_m_${data_size}b-DB.json

# 		cp ../1500_data_fixed_2/r_b_m_15w-OTGY.json ./r_w_m_${data_size}w-OTGY.json
# 		cp ../1500_data_fixed_2/r_w_m-OTGY.json ./
# 		cd ../

# 	done
# done

# for idx in 3 4 5 6 7 8 9 1 2; do
# 	for data_size in 15; do
# 		# python multiple_domains.py $idx $data_size

# 		cd ./1500_data_fixed_${idx}/

# 		cat bus-MixSpec-1500.json weather-MixSpec-1500.json movie-MixSpec-1500.json > b_w_m.json
# 		cat bus-MixSpec-1500-DB.json weather-MixSpec-1500-DB.json movie-MixSpec-1500-DB.json > b_w_m-DB.json 

# 		sed -i 's/\]\[/,/g' b_w_m-DB.json
# 		sed -i 's/\]\[/,/g' b_w_m.json

# 		cat b_w_m.json restaurant-MixSpec-${data_size}.json > b_w_m_${data_size}r.json
# 		cat b_w_m-DB.json restaurant-MixSpec-${data_size}-DB.json > b_w_m_${data_size}r-DB.json 

# 		sed -i 's/\]\[/,/g' b_w_m_${data_size}r.json 
# 		sed -i 's/\]\[/,/g' b_w_m_${data_size}r-DB.json

# 		cp ../1500_data_fixed_2/r_b_m_15w-OTGY.json ./b_w_m_${data_size}r-OTGY.json
# 		cp ../1500_data_fixed_2/b_w_m-OTGY.json ./

# 		cd ../

# 	done
# done


# for idx in 1 2 3 4 5 6 7 8 9; do
# 	for data_size in 15; do
# 		cd ./1500_data_fixed_${idx}/


# 		cat restaurant-MixSpec-1500.json movie-MixSpec-${data_size}.json rest_pitt-MixSpec-${data_size}.json > rest_${data_size}m_${data_size}rslot.json
# 		cat restaurant-MixSpec-1500-DB.json movie-MixSpec-${data_size}-DB.json rest_pitt-MixSpec-${data_size}-DB.json > rest_${data_size}m_${data_size}rslot-DB.json 

# 		sed -i 's/\]\[/,/g' rest_${data_size}m_${data_size}rslot.json 
# 		sed -i 's/\]\[/,/g' rest_${data_size}m_${data_size}rslot-DB.json
# 		# cp ../1500_data_fixed_2/rest_15m_15rslot-OTGY.json ./rest_${data_size}m_${data_size}rslot-OTGY.json

# 		cd ../

# 	done
# done