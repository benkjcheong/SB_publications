#!/usr/bin/env python3
import csv
import os
import re

CSV_FILE = "/Users/safcado/SB_publications/SB_publication_PMC.csv"
TXT_DIR = "/Users/safcado/SB_publications/txt"

def extract_pmc_id(url):
    match = re.search(r'PMC(\d+)', url)
    return match.group(1) if match else None

def main():
    # Get PMC IDs from CSV
    csv_pmcs = set()
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            pmc_id = extract_pmc_id(row.get('Link', ''))
            if pmc_id:
                csv_pmcs.add(pmc_id)
    
    # Get PMC IDs from txt files
    txt_pmcs = set()
    for filename in os.listdir(TXT_DIR):
        if filename.startswith('PMC') and filename.endswith('.txt'):
            pmc_id = filename[3:-4]  # Remove 'PMC' prefix and '.txt' suffix
            txt_pmcs.add(pmc_id)
    
    # Find missing
    missing_in_txt = csv_pmcs - txt_pmcs
    extra_in_txt = txt_pmcs - csv_pmcs
    
    print(f"Total PMCs in CSV: {len(csv_pmcs)}")
    print(f"Total PMCs in txt files: {len(txt_pmcs)}")
    print(f"Missing from txt files: {len(missing_in_txt)}")
    print(f"Extra in txt files: {len(extra_in_txt)}")
    
    if missing_in_txt:
        print("\nMissing PMC IDs:")
        for pmc_id in sorted(missing_in_txt):
            print(f"  PMC{pmc_id}")
    
    if extra_in_txt:
        print("\nExtra PMC IDs in txt files:")
        for pmc_id in sorted(extra_in_txt):
            print(f"  PMC{pmc_id}")

if __name__ == "__main__":
    main()