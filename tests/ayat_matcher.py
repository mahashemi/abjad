import json
import xml.etree.ElementTree as ET
import os
import numpy as np
import abjad_calculator as ac
from abjad_calculator.common.utils import clean_text

cwd = os.getcwd()
# Parse the XML file
if os.path.exists(os.path.join(cwd,'quran-uthmani.xml')):
    tree = ET.parse(os.path.join(cwd,'quran-uthmani.xml'))
elif os.path.join(cwd,'tests', 'quran-uthmani.xml'):
    tree = ET.parse(os.path.join(cwd, 'tests', 'quran-uthmani.xml'))
else:
    raise FileExistsError("File not exists. Please run script from `abjad` folder")

def test(surah_number:int):
    # Get the root element
    root = tree.getroot()

    for title, ayats in ac.quran.items():
        surah_num = title.split('-')[1].strip().split(' ')[1].strip()
        if surah_num==surah_number or int(surah_num)==surah_number:
            print(title)
            break
    # Iterate through the elements
    for child in root:
        if child.attrib.get("index")==surah_number:
            for idx, grandchild in enumerate(child):
                usmani_text = grandchild.attrib.get('text')
                usmani_text = np.array(list(reversed(list(clean_text(usmani_text).replace(' ','').replace('ـ','')))))
                farman_ali_text = ayats[idx].get('arabic_text')
                farman_ali_text = np.array(list(reversed(list(clean_text(farman_ali_text).replace(' ','')))))
                if usmani_text.shape==farman_ali_text.shape:
                    is_match=(usmani_text==farman_ali_text)
                    # print(is_match)
                    print([f"{':'.join(g)}" for g in zip(usmani_text,farman_ali_text)])
                    if not any(is_match):
                        print(idx, 
                            usmani_text, 
                            farman_ali_text
                            )
                        break
                else:
                    print(f'shape mismatch: {idx}')
                    print([f"{':'.join(g)}" for g in zip(usmani_text,farman_ali_text)])
                    break