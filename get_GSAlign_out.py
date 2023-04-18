'''this code counts the number of mutations from GSAlign output and later saves it into meg file'''
import sys

input_file = sys.argv[1]
prefix_1 = sys.argv[2]
prefix_2 = sys.argv[3]
analys_ID = sys.argv[4]

out_file_name = analys_ID + '.txt'

print("GET GSALIGN CODE NOW")

with open(input_file, 'r') as f:
    data = f.read()
    mutation_ctr = 0
    for line in data.split('\n'):
        if not line.startswith('#'):
            mutation_ctr += 1
    #subtract the count for last empty line
    mutation_ctr -= 1

#add the info necessary to build a meg file in the future
info = prefix_1 + ' ' + prefix_2 + ' ' + str(mutation_ctr)
print('INFO: ', info)
with open(out_file_name, 'a') as meg_file:
    meg_file.write(info)
    meg_file.write('\n')




