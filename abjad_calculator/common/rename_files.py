#!/usr/bin/env python3
"""Script to rename Quran surah files to follow chapter_xxx_name.py pattern."""

import os
from pathlib import Path

# Mapping of current filename (without .py) to chapter number
surah_mapping = {
    'al_fatiha': 1,
    'al_baqara': 2,
    'al_imran': 3,
    'al_nisa': 4,
    'al_maida': 5,
    'al_anaam': 6,
    'al_araaf': 7,
    'al_anfaal': 8,
    'at_tauba': 9,
    'yunus': 10,
    'hud': 11,
    'al_rahmaan': 55,
    'al_waqia': 56,
    'al_mujadela': 58,
    'al_hashr': 59,
    'al_naba': 78,
    'al_naziyat': 79,
    'al_abas': 80,
    'al_takweer': 81,
    'al_infetaar': 82,
    'al_mutaffefin': 83,
    'al_insheqaq': 84,
    'al_burooj': 85,
    'al_tariq': 86,
    'al_aala': 87,
    'al_ghasheya': 88,
    'al_fajr': 89,
    'al_balad': 90,
    'al_shams': 91,
    'al_layl': 92,
    'al_zuha': 93,
    'al_shara': 94,
    'al_tin': 95,
    'al_alaq': 96,
    'al_qadr': 97,
    'al_bayyinah': 98,
    'al_zilzal': 99,
    'al_aadiyat': 100,
    'al_qaariyah': 101,
    'al_takasur': 102,
    'al_asr': 103,
    'al_humaza': 104,
    'al_fil': 105,
    'al_quraish': 106,
    'al_maun': 107,
    'al_kawthar': 108,
    'al_kafiroon': 109,
    'al_nasr': 110,
    'al_masad': 111,
    'al_ikhlas': 112,
    'al_falaq': 113,
    'al_nas': 114,
}

def main():
    script_dir = Path(__file__).parent
    
    print("Starting file renaming process...")
    print(f"Working directory: {script_dir}")
    print("-" * 60)
    
    renamed_count = 0
    skipped_count = 0
    
    for old_name, chapter_num in surah_mapping.items():
        old_file = script_dir / f"{old_name}.py"
        new_file = script_dir / f"chapter_{chapter_num:03d}_{old_name}.py"
        
        if old_file.exists():
            if new_file.exists():
                print(f"⚠️  SKIP: {new_file.name} already exists")
                skipped_count += 1
            else:
                old_file.rename(new_file)
                print(f"✓ Renamed: {old_name}.py -> {new_file.name}")
                renamed_count += 1
        else:
            print(f"✗ NOT FOUND: {old_name}.py")
    
    print("-" * 60)
    print(f"\nRenaming complete!")
    print(f"  Renamed: {renamed_count} files")
    print(f"  Skipped: {skipped_count} files")

if __name__ == "__main__":
    main()
