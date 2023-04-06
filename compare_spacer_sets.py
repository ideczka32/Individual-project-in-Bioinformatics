import os

def check_if_exists(longer_list, element):
    ctr = 0
    for el in longer_list:
        ctr += 1
        if el == element:

            return True, ctr
    return False, ctr

file_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\identifying CRISPR\\cd_spacers"

f1 = input('first file: ')
f2 = input('second file: ')
f1 = f1 + '.fasta'
f2 = f2 + '.fasta'
f1_path = os.path.join(file_dir, f1)
f2_path = os.path.join(file_dir, f2)
f1_spacers = []
f2_spacers = []
with open(f1_path, 'r') as file1:
    read = file1.read()
    for line in read.split('\n'):
        if not line.startswith('>'):
            f1_spacers.append(line[:-1])
    file1.close()
with open(f2_path, 'r') as file2:
    read = file2.read()
    for line in read.split('\n'):
        if not line.startswith('>'):
            f2_spacers.append(line[:-1])
    file2.close()
f1_spacers.pop()
f2_spacers.pop()

if len(f1_spacers) > len(f2_spacers):
    ctr = 0
    for el in f2_spacers:
        ctr += 1
        exists, pos = check_if_exists(f1_spacers, el)
        if exists:
            print('Spacer {} exists in f2 at position {}'.format(ctr, pos))

        else:
            print('no spacer {} in f2'.format(ctr))
else:
    ctr = 0
    for el in f1_spacers:
        ctr += 1
        exists, pos = check_if_exists(f2_spacers, el)
        if exists:
            print('Spacer {} exists in f1 at position {}'.format(ctr, pos))

        else:
            print('no spacer {} in f1'.format(ctr))