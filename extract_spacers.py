import re
import os

dir_path = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\identifying CRISPR\\CRISPRDetectOut"
out_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\identifying CRISPR\\cd_spacers"
files = os.listdir(dir_path)

for filename in files:
    file_path = os.path.join(dir_path, filename)

    with open(file_path, 'r') as file:
        ctr = 0
        read = file.read()
        for line in read.split('\n'):

            if line.startswith('Array'):
                #create a new output file that will store one crispr_sequence
                ctr += 1
                spacer_nr = 1
                file_match = re.search(r'(J\d+_)', filename)
                group = file_match.groups()
                out_filename = group[0] + str(ctr) + '.fasta'

                print(out_filename)

            match = re.search(r'^\s+\d+\s+\d+\s+\d+\.\d\s+\d+\s+[ACTG\.]+\s+([ACTG]+)', line)
            # print(match)
            if match:

                spacer = match.groups()
                file_path = os.path.join(out_dir, out_filename)
                with open(file_path, 'a') as out_file:
                    #write spacers to output file
                    out_file.write('>' + group[0] + '_' + str(spacer_nr))
                    out_file.write('\n')
                    out_file.write(spacer[0])
                    out_file.write('\n')
                    out_file.close()

                    spacer_nr += 1
