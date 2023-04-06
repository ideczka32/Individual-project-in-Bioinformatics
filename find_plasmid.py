import os
import re
import pandas as pd

data_dir_path = "C:\\Users\\Idzia\\Desktop\\PROJEKT\\bact_sequences"
files = os.listdir(data_dir_path)

df_columns = ['bact ID', 'depth', 'is circular']
data_list = []

for f in files:
    file_path = os.path.join(data_dir_path,f)
    with open(file_path, 'r') as file:
        read = file.read()
        for line in read.split('\n'):
            if line.startswith('>'):
                is_circular = re.match(r'>(J\d+_\d+)\slength=\d+\sdepth=(\d+.\d+)x\scircular=(.+)$', line)
                if is_circular:
                    groups = is_circular.groups()
                    data_list.append(groups)

df = pd.DataFrame(data_list, columns=df_columns)
df['depth'] = pd.to_numeric(df['depth'])

# dataframe.loc[df['bact_ID '] == bact_identifier, 'start']
plasmid_df_1 = df.loc[df['depth'] >= 5.0]
plasmid_df_2 = df.loc[df['depth'] <= 0.5]
plasmid_df = pd.concat([plasmid_df_1, plasmid_df_2], axis=0)
print(plasmid_df)


#depth treshold= 5


