#!/usr/bin/env python3
import csv
import os
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

DOWNLOAD_DIR = "/Users/safcado/SB_publications/txt"
CSV_FILE = "/Users/safcado/SB_publications/SB_publication_PMC.csv"

def extract_pmc_id(url):
    match = re.search(r'PMC(\d+)', url)
    return match.group(1) if match else None

def download_page_as_txt(pmc_id, title=""):
    target_file = os.path.join(DOWNLOAD_DIR, f"PMC{pmc_id}.txt")
    if os.path.exists(target_file):
        print(f"⏭ Skip: PMC{pmc_id}.txt")
        return True

    print(f"📥 PMC{pmc_id}: {title[:40]}...")
    
    page_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        response = requests.get(page_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main article content
        article = soup.find('div', class_='article') or soup.find('article') or soup.find('main')
        if not article:
            article = soup
        
        # Remove script and style elements
        for script in article(["script", "style"]):
            script.decompose()
        
        text = article.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"✓ Downloaded: PMC{pmc_id}.txt")
        return True
            
    except Exception as e:
        print(f"✗ Error PMC{pmc_id}: {e}")
        return False

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found")
        return
    
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    
    downloaded = failed = 0
    
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            pmc_id = extract_pmc_id(row.get('Link', ''))
            if pmc_id:
                if download_page_as_txt(pmc_id, row.get('Title', '')):
                    downloaded += 1
                else:
                    failed += 1
                time.sleep(1)  # Be nice to the server
            else:
                failed += 1
    
    print(f"\n📊 Summary: {downloaded} downloaded, {failed} failed")

if __name__ == "__main__":
    main()