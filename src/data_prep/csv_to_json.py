import json
import csv
from collections import defaultdict
import os

if not os.path.exists(r"data\preprocessed\HanViet.json"):

    if not os.path.exists(r"data\preprocessed"):
        os.makedirs(r"data\preprocessed")
    
    dic = defaultdict(list)
    csv_path = r"data\raw\vi_dictionary.csv"
    json_path = r"data\preprocessed\HanViet.json"

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            word = row['word'].strip().lower()
            mean = row['meaning'].strip()
            ex = row['example'].strip()
            
            dic[word].append({
                'Nghĩa': mean,
                'Ví dụ': ex
            })

    with open(json_path, mode='w', encoding='utf-8') as w:
        json.dump(dic, w, ensure_ascii=False, indent=2)