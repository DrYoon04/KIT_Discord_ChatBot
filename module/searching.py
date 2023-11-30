import os
from _datetime import datetime
from llama_index.llms import OpenAI
from llama_index import StorageContext, load_index_from_storage
now = datetime.now()
date = now.strftime("%Y-%m-%d")
import openai
file_path = '/Users/dryoon04/Documents/GitHub/KIT_Discord_ChatBot/api_key.txt'
# 파일 열기 (읽기 모드로 열기)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽어오기
    file_content = file.read()
os.environ["OPENAI_API_KEY"] = file_content
openai.api_key = os.getenv("OPENAI_API_KEY")

# loader = SimpleDirectoryReader('../data', recursive=True, exclude_hidden=True)
# documents = loader.load_data()
# llm = OpenAI(model="gpt-4-1106-preview", temperature=0)

# service_context = ServiceContext.from_defaults(llm=llm)
# vector_index = VectorStoreIndex.from_documents(documents, service_context=service_context)
# print("공지사항 인덱싱 완료")
# vector_index.storage_context.persist("notice_index")
storage_context = StorageContext.from_defaults(persist_dir="/module/notice_index")
new_index = load_index_from_storage(storage_context)
new_query_engine = new_index.as_query_engine()
def shool_notice(quary):
    response = new_query_engine.query(f"{quary},제목과 링크,날짜로 알려줄것, 오늘 날짜 : {date}")
    return response
