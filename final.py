import pandas as pd
import os
import re
import find_plasmid


def match_ID(line):
    match_ID = re.search(r'J\d+__\d+\s+(J\d+_\d+)\s+', line)
    groups = match_ID.groups()
    ID = groups[0]
    return ID


def match_startend(line):
    match = re.search(r'^J\d+__\d+\s+J\d+_\d+\s+\d+.\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+(\d+)', line)
    groups = match.groups()
    start = groups[0]
    end = groups[1]

    return start, end


def check_prophages(line, dataframe):
    hit = False
    phage_start = 0
    phage_stop = 0
    bact_identifier = ' '
    if line.startswith('J'):
        # get blast bact_ID and coordinates
        bact_identifier = match_ID(line)
        start, end = match_startend(line)
        # print('bacteria', bact_identifier, 'start', start, 'end', end)
        # get start & stop values for prophages in a given bactera
        df_start = dataframe.loc[df['bacteria ID'] == bact_identifier, 'start']
        df_stop = dataframe.loc[df['bacteria ID'] == bact_identifier, 'stop']
        df_startstop = pd.concat([df_start, df_stop], axis=1)
        # print(df_startstop)
        # check if hit matches with any of the regions
        rslt_df = df_startstop[df_startstop['start'] <= float(start)]
        # print(rslt_df)
        rslt_df = rslt_df[rslt_df['stop'] >= float(end)]

        if rslt_df.empty == False:
            hit = True
            np_arr = rslt_df.to_numpy()
            phage_start = np_arr[0][0]
            phage_stop = np_arr[0][1]
            # print(line)
            # print('is a hit against prophage found in bacteria {} at position {} {}'.format(bact_identifier,
            #                                                                                 phage_start,
            #                                                                                 phage_stop))
    return hit, bact_identifier, phage_start, phage_stop


def check_plasmids(line, plasmid_df):
    # checks if there is a hit against plasmid
    hit = False
    bact_hit = ''
    if line.startswith('J'):
        bact_hit = match_ID(line)
        if bact_hit in plasmid_df['bact ID'].values:
            hit = True
            print(line)
            print('is a hit against plasmid found in bacteria {}'.format(bact_hit))
            print('\n')
    return hit, bact_hit


def get_spacer_nr(line):
    spacer = 0
    ident = 0
    match = re.search(r'^J\d+__(\d+)\s+J\d+_\d+\s+(\d+.\d+)\s+', line)
    if match:
        group = match.groups()
        spacer = group[0]
        ident = group[1]
    return spacer, ident


def no_hit_spac(sheet_name, spacers_list, spacers):
    for el in spacers_list:
        spacers.remove(el)

    spacers_string = ' '.join(str(v) for v in spacers)
    with open('unknown_spacers.txt', 'a') as file:
        file.write(sheet_name +': ' + spacers_string+ '\n')
        file.close()


def check_hits(read_blast, dataframe, plasmid_df, bact_id, CRISPR_ID, output_dataframe):
    # check if there are any hits with prophages
    check_prophages(read_blast, dataframe)
    check_plasmids(read_blast, plasmid_df)
    spacers = []
    no_hit_spacers = []

    for line in read_blast.split('\n'):
        plasm_hit, bact_plasm_hit = check_plasmids(line, plasmid_df)
        prophage_hit, pro_bact, pro_start, pro_stop = check_prophages(line, dataframe)
        spacer, ident = get_spacer_nr(line)
        if spacer not in spacers:
            spacers.append(spacer)
        if plasm_hit:
            output_dataframe = output_dataframe.append(
                {'bacteria ID': bact_id, 'CRISPR ID': CRISPR_ID, 'spacer in CRISPR nr': spacer,
                 'target bact ID': bact_plasm_hit, 'start': 0, 'stop': 0, '% ident': ident,
                 'hit against': 'plasmid'}, ignore_index=True)
            if spacer not in no_hit_spacers:
                no_hit_spacers.append(spacer)
        if prophage_hit:
            output_dataframe = output_dataframe.append(
                {'bacteria ID': bact_id, 'CRISPR ID': CRISPR_ID, 'spacer in CRISPR nr': spacer,
                 'target bact ID': pro_bact, 'start': pro_start, 'stop': pro_stop, '% ident': ident,
                 'hit against': 'prophage'}, ignore_index=True)
            if spacer not in no_hit_spacers:
                no_hit_spacers.append(spacer)

    return output_dataframe, no_hit_spacers,spacers


# write excel with annotated phages  to pandas dataframe
df = pd.read_excel('prophages_updated.xlsx')


blast_dir = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\bact_blast_hits_upd_cd"
files = os.listdir(blast_dir)

plasmid_df = find_plasmid.plasmid_df
out_df_columns = ['bacteria ID', 'CRISPR ID', 'spacer in CRISPR nr', 'target bact ID',
                  'start', 'stop', '% ident', 'hit against']

with pd.ExcelWriter("C:\\Users\\Idzia\\Desktop\\PROJEKT\\identifying CRISPR\\SPACERS_known_2.xlsx") as writer:
    for filename in files:
        file_path = os.path.join(blast_dir, filename)
        out_df = pd.DataFrame(columns=out_df_columns)

        with open(file_path, 'r') as file:
            read = file.read()
            bact_source = re.search(r'((J\d+)_(\d+))', filename)
            b = bact_source.groups()
            bact_id = b[1]
            CRISPR_id = b[2]
            sheet_name = bact_id + '_' + CRISPR_id
            # print('currently checking bacteria {} CRISPR nr {} '.format(bact_id, CRISPR_id))
            out_df, no_hit_spacers, spacers = check_hits(read, df, plasmid_df, bact_id, CRISPR_id, out_df)
            # print(out_df)
            out_df.to_excel(writer, sheet_name=sheet_name)
            no_hit_spac(sheet_name, no_hit_spacers, spacers)