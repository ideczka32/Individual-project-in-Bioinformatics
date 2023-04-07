#!/bin/bash

file_dir="/home/ikups/GSAlign/orange_bact/"
prefix_list=()

for file1 in "$file_dir"*
do
  name_out=$(basename "$file1")
  name_out="${name_out%.*}"
  prefix_out="${name_out%%_*}"
  name_out="${prefix_out}.txt"
  echo "prefix out"
  echo "$prefix_out"
  prefix_list+=("$prefix_out")
  
  for file2 in "$file_dir"*
  do
    if [[ "$file1" != "$file2" && "$file1" < "$file2" ]]
    then
      name1=$(basename "$file1")
      name1="${name1%.*}"
      prefix1="${name1%%S*}"
      prefix3="${name1%%_*}"
      name2=$(basename "$file2")
      name2="${name2%.*}"
      prefix2="${name2%%_*}"
      
      out_name="${prefix1}${prefix2}"
      echo "$out_name"
      GSAlign -r "$file1" -q "$file2" -o "$out_name" 
      
      vcf_file="${out_name}.vcf"
      
      python get_GSAlign_out.py "./$vcf_file" "$prefix3" "$prefix2"
      

    fi
  done
done

echo "${prefix_list[@]}"
prefix_list_str=$(printf ",%s" "${prefix_list[@]}")
prefix_list_str=${prefix_list_str:1}

python make_distance_matrix.py "$prefix_list_str" "/home/ikups/GSAlign/meg_file.txt"

