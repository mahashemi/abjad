import pandas as pd
import json
import os
cwd = os.getcwd()
debug_dir = os.path.join(cwd, "debug")
dirs = os.listdir(debug_dir)
data = []
for dir in dirs:
    if '-' in dir:
        surah_number = f"{int(dir.split('-')[1].strip().split(' ')[1].strip()):03d}"
        total_qamari = 0
        total_malfuzi = 0
        total_bayenati = 0
        json_dir = os.path.join(debug_dir, dir)
        json_folders = os.listdir(json_dir)
        for json_folder in json_folders:
            if json_folder.isnumeric():
                json_file = os.path.join(json_dir, json_folder, 'result.json')
                with open(json_file,'r') as fp:
                    json_data = json.load(fp=fp)
                    total_qamari += json_data.get('total_qamari_value')
                    total_malfuzi += json_data.get('total_malfuzi_value')
                    total_bayenati += json_data.get('total_bayenati_value')
        data.append({'surah_number': surah_number, 'surah': dir, 'total_qamari': total_qamari, 'total_malfuzi': total_malfuzi, 'total_bayenati': total_bayenati})

pd.DataFrame(data=data).to_excel('verification.xlsx',index=False)

