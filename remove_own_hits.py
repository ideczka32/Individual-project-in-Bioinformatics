import re
import os

dir_path = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\hits_blast_ourbact_cct"
out_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\hits_updated_2_cct"
files = os.listdir(dir_path)

for filename in files:
    file_path = os.path.join(dir_path,filename)
    with open(file_path, 'r') as file:
        read = file.read()
        #identify source bacteria ID
        bact_source = re.search(r'(J\d+_\d+)', filename)
        b = bact_source.groups()
        bact_id = b[0]
        #search for self matches
        for line in read.split('\n'):
            match = re.search(r'Contig\d+_\d+:\d+\s+(J\d+_\d+)', line)
            if match:

                groups = match.groups()
                if bact_id != groups[0]:

                    out_file_path = os.path.join(out_dir,filename)
                    with open(out_file_path, 'a') as out_file:
                        out_file.write(line)
                        out_file.write('\n')




# import re
# import os
#
# dir_path = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\hits_blast_outbact_cd"
# out_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\hits_updated_2_cd"
# files = os.listdir(dir_path)
#
# for filename in files:
#     file_path = os.path.join(dir_path,filename)
#     with open(file_path, 'r') as file:
#         read = file.read()
#         #identify source bacteria ID
#         bact_source = re.search(r'(J\d+_\d+)', filename)
#         b = bact_source.groups()
#         bact_id = b[0]
#         #search for self matches
#         for line in read.split('\n'):
#             match = re.search(r'J\d+__\d+\s+(J\d+_\d+)', line)
#             if match:
#
#                 groups = match.groups()
#                 if bact_id == groups[0]:
#                     print(line)
#                 if bact_id != groups[0]:
#
#                     out_file_path = os.path.join(out_dir,filename)
#                     with open(out_file_path, 'a') as out_file:
#                         out_file.write(line)
#                         out_file.write('\n')
#
#
#
#
