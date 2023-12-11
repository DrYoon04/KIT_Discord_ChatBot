import os
import re
import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from html_table_parser import parser_functions
from tqdm import tqdm
from elasticsearch import Elasticsearch
from langchain.text_splitter import CharacterTextSplitter

now = datetime.now()
date = now.strftime("%Y")
time = str(date)
print("공지사항 로딩중")

# Web scraping for 공지사항
url1 = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do?mode=list&&articleLimit=100&article.offset=0"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

html = requests.get(url1, headers=headers)
soup = BeautifulSoup(html.content, 'html.parser')
data = soup.find('div', {'class': 'board-list01'})

table = data.find('table')
p = parser_functions.make2d(table)
df = pd.DataFrame(p[1:], columns=p[0])

# Data cleaning
count = 0
for i in df['번호']:
    if i == '':
        count += 1

df = df.drop(df.index[0:count])
df = df.reset_index(drop=True)
df = df.drop(['조회', '첨부', '작성자'], axis=1)

for i in df['제목']:
    pretreatment = i.split('\n')
    clean_text = pretreatment[0]
    df['제목'] = df['제목'].replace(i, clean_text)

title = data.find_all('td', {'class': 'title left'})
main_url = "https://www.kumoh.ac.kr/ko/sub06_01_01_01.do"

for i in range(len(title)):
    title[i] = title[i].find('a')
    title[i] = title[i]['href']
    title[i] = main_url + title[i]

title = title[count:]
df['url'] = title

df.to_csv("module/data/notice_new.csv", encoding="utf-8")
print("공지사항 로딩완료")

# Remove duplicates from CSV files
file1_path = 'module/data/notice_new.csv'
file2_path = 'module/data/notice.csv'
key_column = '제목'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df = pd.concat([df1, df2]).drop_duplicates(subset=key_column, keep=False)

# Scrape details and save to Elasticsearch
title_url = {}
for i in range(len(df)):
    title_url[df['제목'][i]] = df['url'][i]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

for title, url in tqdm(title_url.items()):
    clean_title = re.sub('[^a-zA-Z0-9가-힣\s]', '', title)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    board_contents = soup.find('div', class_='board-contents')
    text_content = board_contents.get_text(separator='\n', strip=True)
    text_content = re.sub(r'\n', '', text_content)

    file_name = f"module/data/notice_txt/{clean_title}.txt"
    df.loc[df['제목'] == title, '본문'] = text_content

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"url : {url}\n{text_content}")

os.remove('module/data/notice.csv')
os.rename('module/data/notice_new.csv', 'module/data/notice.csv')

# Elasticsearch connection and index creation
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
if es.ping():
    print('Yay Connect')
else:
    print('Awww it could not connect!')

index_name = 'txt_data_index'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Indexing text data in Elasticsearch
folder_path = 'module/data/notice_txt'
file_list = os.listdir(folder_path)
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)

for i, file_name in enumerate(file_list):
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    chunks = text_splitter.split_text(data)

    for j, chunk in enumerate(chunks):
        document = {
            'text': chunk.strip(),
            'file_name': file_name
        }
        es.index(index=index_name, id=i * len(file_list) + j + 1, body=document)
