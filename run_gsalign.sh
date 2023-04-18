#!/bin/bash

echo "Enter the path to the directory but whithout quotation marks please!"
read file_dir

echo "Type the analysis ID"
read analysis_ID

prefix_list=()

for file1 in "$file_dir"/*
do
  echo "file1"
  echo "$file1"
  extension="${file1##*.}"
  echo "$extension"
  if [[ "$extension" == "fasta" || "$extension" == "fa" ]]; then
    echo "x"
    echo "$file1"
    echo "x"
    name_out=$(basename "$file1")
    name_out="${name_out%.*}"
    prefix_out="${name_out%%_*}"
    name_out="${prefix_out}.txt"
    echo "prefix out"
    echo "$prefix_out"
    prefix_list+=("$prefix_out")

    for file2 in "$file_dir"/*
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

        python get_GSAlign_out.py "./$vcf_file" "$prefix3" "$prefix2" "$analysis_ID"


      fi
    done
  fi
done

echo "${prefix_list[@]}"
prefix_list_str=$(printf ",%s" "${prefix_list[@]}")
prefix_list_str=${prefix_list_str:1}

extension=".txt"
filename="${analysis_ID}${extension}"
echo "filename"
echo "$filename"

python make_distance_matrix.py "$prefix_list_str" "$filename" 

echo "ANALYSIS IS OVER. CHECK YOUR .meg FILE"
