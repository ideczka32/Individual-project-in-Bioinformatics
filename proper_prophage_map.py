import os
import re
from Bio import SeqIO
import pandas as pd


def extract_information(line):
    """extracts the important information from every BLAST hit"""
    info = re.search(r'<unknown\s+(J\d+)_(\d+)\s+(\d+)\.\d+\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+(\d+)\s+',line)
    info_groups = info.groups()
    target_bact = info_groups[0]
    target_bact_contig = info_groups[1]
    identity = info_groups[2]
    al_length = info_groups[3]
    start_in_target = info_groups[4]
    stop_in_target = info_groups[5]
    return target_bact, target_bact_contig, identity, al_length, start_in_target, stop_in_target

def decide_if_add(identity, al_length, perfect_al_length):
    """decides whether the hits is important enough to add to the prophage map """
    perc_perf_al = int(al_length)/int(perfect_al_length)
    if int(identity) < 99:
        return False
    if int(perc_perf_al) < 0.95:
        return False
    return True


prophages_hits_dict = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\prophages_bact_hits\\out_2"
bacteria_dict = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\bact_sequences"

files_prop = os.listdir(prophages_hits_dict)
files_bact = os.listdir(bacteria_dict)

# for each bacteria check the blast hits and make a prophage map
dfs ={}

for bacteria in files_bact:
    print(bacteria)
    bact_source = re.search(r'(J\d+)_S\d+', bacteria)
    groups = bact_source.groups()
    bacteria_ID = groups[0]
    df_cloumns = ['contig','prophage ID', 'start', 'stop']
    df = pd.DataFrame(columns=df_cloumns)
    # read all the prophage blast files and look for hits located in bacteria
    for prophage in files_prop:
        prophage_ID = prophage[:-4]
        file_path = os.path.join(prophages_hits_dict, prophage)

        with open(file_path, 'r') as p:
            prophage_file = p.read()
            line_ctr = True
            for line in prophage_file.split('\n'):
                if line.startswith('<'):
                    t_bact, t_bact_con, identity, al_length, start_in_t, stop_in_t = extract_information(line)
                    if line_ctr:
                        perfect_al_length = al_length
                        line_ctr = False
                    if bacteria_ID == t_bact:
                        #there was a hit against analyzed bacteria
                        if decide_if_add(identity=identity, al_length=al_length, perfect_al_length=perfect_al_length):
                            print('adding line:')
                            print(line)
                            df = df.append({'contig': t_bact_con, 'prophage ID': prophage_ID, 'start': start_in_t, 'stop': stop_in_t }, ignore_index=True)
    dfs[bacteria_ID] = df
with pd.ExcelWriter('prophages_upd.xlsx') as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name)


