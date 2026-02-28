from langchain_community.document_loaders import PyMuPDFLoader
import re
from collections import defaultdict
import json
import os

def clean_pdf_header_footer(text: str) -> str:

    pattern = r"\d+\s*\n\s*Luận Ngữ - Khổng Tử --\s*Phùng Hoài Ngọc\s*biên giả\s*---\s*www\.vietnamvanhien\.net\s"
    cleaned_text = re.sub(pattern, "", text)
    
    return cleaned_text

def cre_dic():

    list_thien = [
    'Học nhi',
    'Vi chính',
    'Bát dật',
    'Lý nhân',
    'Công Dã Tràng',
    'Ung dã',
    'Thuật nhi',
    'Thái Bá',
    'Tử hãn',
    'Hương đảng',
    'Tiên tiến',
    'Nhan Uyên',
    'Tử Lộ',
    'Hiến vấn',
    'Vệ Linh công',
    'Quí thị',
    'Dương Hóa',
    'Vi Tử',
    'Tử Trương',
    'Nghiêu viết'
    ]
    list_thien_han=['学而','为政','八佾','里仁','公冶长','雍也','述而','泰伯','子罕','言乡党','先进','颜渊','子路','宪问','卫灵公','季氏','阳货','微子','子张','尧曰']


    dicc = defaultdict(dict)

    for i in range(20):
        dicc[f'Thiên {i+1}']['Tên thiên']= list_thien[i]
        dicc[f'Thiên {i+1}']['Chữ Hán']= list_thien_han[i]
        
    return dicc
        

def write_dic(dicc,Thien_du):
    for i in range(0,20):
        with open(f'data\preprocessed/test{i}.txt', mode='r', encoding='utf-8') as f:
            thien= f.read()
            thien = thien.replace('．', '.')
            thien = thien.replace('·', '.')
            thien = thien.replace('\xa0', ' ')
            thien = thien.replace('\u3000', ' ')
            # pattern = r'(?m)^\d+\.\d+.*?(?=^\d+\.\d+|\Z)'

            matches = re.split(r'\d+\.\s*\d+', thien)
            
            k = 1
            for j in range(1,len(matches)):
                
                new=matches[j].replace('·','.')

                if len(new)>15:
                    
                    if i+1 == 9:
                        if j==2:
                            continue
                    if i+1 in Thien_du:
                        if j==1:
                            continue
                    
                    dicc[f'Thiên {i+1}'][f'Bài {i+1}.{k}']= new
                    k+=1
    return dicc

def dele():
    for i in range(-1,21):
        if os.path.exists(f'data\preprocessed/test{i}.txt'):
            os.remove(f'data\preprocessed/test{i}.txt')


def main():
    if not os.path.exists(r"data\preprocessed"):
        os.makedirs(r"data\preprocessed")
    loadpdf= PyMuPDFLoader(r"data\raw\LuanNgu.pdf")
    data = loadpdf.load()
    
    text=''
    for i, doc in enumerate(data):
        doc = clean_pdf_header_footer(doc.page_content)
        doc =doc.replace('Ƣ','Ư')
        doc = doc.replace('ƣ','ư')
        text+=doc
        
    parts = re.split(r'Hết\s+thiên\s+\d+', text)
    
    for i,part in enumerate(parts):
        with open(f'data\preprocessed/test{i}.txt', mode='w', encoding='utf-8') as f:
            f.write(part)
            
    with open(r'data\preprocessed\test19.txt', mode='r', encoding='utf-8') as f:
        thien = f.read()
        thien20 = re.split(r'Hết\s+', thien)
        j = 0
        for i in range(19,21):
            with open(f'data\preprocessed/test{i}.txt', mode='w', encoding='utf-8') as ff:
                ff.write(thien20[j])
            j+=1
            
    with open(r'data\preprocessed\test0.txt', mode='r', encoding='utf-8') as f:
        thien = f.read()
        thien20 = re.split(r'Biên giả', thien)
        j = 0
        for i in range(-1,1):
            with open(f'data\preprocessed/test{i}.txt', mode='w', encoding='utf-8') as ff:
                ff.write(thien20[j])
            j+=1
    
    dicc = cre_dic()
    Thien_du= [2,4,5,6,10,11,12,13,14,15,16,17,18,19,20]
    dicc = write_dic(dicc,Thien_du)
    
    with open(r'data\preprocessed\test-1.txt', mode='r', encoding='utf-8') as f:
        thien = f.read()
        dicc['Lời mở đầu'] = thien
    
    with open(r'data\preprocessed\test20.txt', mode='r', encoding='utf-8') as f:
        thien = f.read()
        dicc['Lời Kết'] = thien
        
    with open(r'data\preprocessed\luanngu.json', mode='w', encoding='utf-8') as w:
        json.dump(dicc, w, ensure_ascii=False, indent=2)
    
    dele()
    
if __name__ == '__main__':
    main()