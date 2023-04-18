import numpy as np
import pandas as pd
import sys
import re


def read_dat_file(dat_file):
    """reads data file containing number of mutations for each possible pair"""
    with open(dat_file, 'r') as f:
        file_content = f.read()
    return file_content


def get_coordinates(line):
    """reads the data from each line"""
    line_match = re.search(r'(J\d+)\s(J\d+)\s(\d+)', line)
    groups = line_match.groups()
    first = groups[0]
    second = groups[1]
    distance = groups[2]
    return first, second, distance


def fill_dataframe(distance_matrix, read):
    """fills the dataframe with calculated distances"""
    for line in read.split('\n'):
        if line:
            first, second, distance = get_coordinates(line)
            distance_matrix.loc[first, second] = distance
            distance_matrix.loc[second, first] = distance


def save_to_meg(distance_matrix, list_of_files, matrix_size, meg_file):
    """saves the left triangular distance matrix to the .meg, file"""
    with open(meg_file, 'w') as f:
        f.write('#MEGA \n')
        f.write("TITLE: Lower--left triangular matrix \n")
        for file in list_of_files:
            string_line = '#' + file + '\n'
            f.write(string_line)
        f.write('\n')
        # write in the distance matrix
        for i in range(1, matrix_size):
            for j in range(i):
                f.write(str(distance_matrix.iloc[i, j])+'\t')
            f.write('\n')
        f.write('\n')
        f.write('\n')


print("MAKE_DISTANCE_MATRIX CODE NOW")

# get list of all the bacteria prefixes in the folder
prefix_list = sys.argv[1]
prefix_list = prefix_list.split(',')

# get the data file with distances assigned to  bacteria pairs
dat_file = sys.argv[2]

#get the .meg file name
spl = dat_file.split('.')
meg_name = spl[0]
meg_name = meg_name + '.meg'

# create a dataframe of size equal to the number of bacteria  in the folder filled with zeros
matrix_size = len(prefix_list)
data = np.zeros((matrix_size, matrix_size))
distance_matrix = pd.DataFrame(data=data, index=prefix_list, columns=prefix_list)

read = read_dat_file(dat_file)

fill_dataframe(distance_matrix, read)

save_to_meg(distance_matrix, prefix_list, matrix_size, meg_name)

