import os
import re

file_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\identifying CRISPR\\cd_spacers"
files = os.listdir(file_dir)

spacers_dict = {}

def check_dict(spac_dic, lin):
    for key in spac_dic.keys():
        ctr = 0
        for val in spac_dic[key]:
            # print(key)
            # print(val)
            ctr += 1
            if val == lin:
                print('found the same spacer in {} at nr {}'.format(key,ctr))

for filename in files:
    file_path = os.path.join(file_dir, filename)
    with open(file_path, 'r') as file:
        read = file.read()
        bact_source = re.search(r'((J\d+)_(\d+))', filename)
        b = bact_source.groups()
        bact_id = b[1]
        CRISPR_id = b[2]
        sheet_name = bact_id + '_' + CRISPR_id
        spacers_dict[sheet_name] = []

        for line in read.split('\n'):
            if not line.startswith('>'):
                spacers_dict[sheet_name].append(line)
        file.close()
        spacers_dict[sheet_name].pop()

f = input('file to check')
f = f+'.fasta'
f_path = os.path.join(file_dir,f)

with open(f_path, 'r') as f_to_check:
    f_read = f_to_check.read()
    spacer_nr = 0
    for line in f_read.split('\n'):
        if line.startswith('A') or line.startswith('C') or line.startswith('T') or line.startswith('G'):
            spacer_nr += 1
            print('checking spacer nr: ', spacer_nr)
            check_dict(spacers_dict, line)

