import numpy as np
import pandas as pd
import sys
import re


def read_dat_file(dat_file):
    with open(dat_file, 'r') as f:
        read = f.read()
    return read


def get_coordinates(line):
    line_match = re.search(r'(J\d+)\s(J\d+)\s(\d+)', line)
    groups = line_match.groups()
    first = groups[0]
    second = groups[1]
    distance = groups[2]
    return first, second, distance


def fill_dataframe(distance_matrix, read):
    for line in read.split('\n'):
        if line:
            first, second, distance = get_coordinates(line)
            distance_matrix.loc[first, second] = distance
            distance_matrix.loc[second, first] = distance


def save_to_meg(distance_matrix, list_of_files, matrix_size):

    with open('meg_file.meg', 'w') as f:
        f.write('#MEGA \n')
        f.write("TITLE: Lower--left triangular matrix \n")
        for file in list_of_files:
            string_line = '#' + file + '\n'
            f.write(string_line)
        f.write('\n')
        #write the distance matrix
        for i in range(1, matrix_size):
            for j in range(i):
                f.write(str(distance_matrix.iloc[i, j])+'\t')
            f.write('\n')
        f.write('\n')


list_of_files = sys.argv[1]
list_of_files = list_of_files.split(',')

dat_file = sys.argv[2]

matrix_size = len(list_of_files)

# create a dataframe of a specified size filled with zeros
data = np.zeros((matrix_size, matrix_size))
distance_matrix = pd.DataFrame(data=data, index=list_of_files, columns=list_of_files)

read = read_dat_file(dat_file)

fill_dataframe(distance_matrix, read)

save_to_meg(distance_matrix, list_of_files, matrix_size)

