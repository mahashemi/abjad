#!/usr/bin/env python3
"""Script to rename files from chapter_xxx_al_name.py to chapter_xxx_name.py"""

from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    
    print("Renaming files to remove 'al_' and 'at_' prefixes...")
    print(f"Working directory: {script_dir}")
    print("-" * 60)
    
    renamed_count = 0
    
    # Get all chapter files
    for file_path in sorted(script_dir.glob("chapter_*.py")):
        old_name = file_path.name
        
        # Skip if already processed
        if old_name.startswith("chapter_") and "_al_" in old_name:
            new_name = old_name.replace("_al_", "_")
            new_path = file_path.parent / new_name
            
            if not new_path.exists():
                file_path.rename(new_path)
                print(f"✓ Renamed: {old_name} -> {new_name}")
                renamed_count += 1
        elif old_name.startswith("chapter_") and "_at_" in old_name:
            new_name = old_name.replace("_at_", "_")
            new_path = file_path.parent / new_name
            
            if not new_path.exists():
                file_path.rename(new_path)
                print(f"✓ Renamed: {old_name} -> {new_name}")
                renamed_count += 1
    
    print("-" * 60)
    print(f"\nRenaming complete! Renamed {renamed_count} files")

if __name__ == "__main__":
    main()
