import sys

input_file = sys.argv[1]
prefix_1 = sys.argv[2]
prefix_2 = sys.argv[3]

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
with open('meg_file.txt', 'a') as meg_file:
    meg_file.write(info)




