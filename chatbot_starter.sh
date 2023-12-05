#!/bin/bash

conda activate discord
echo "Discord ChatBot Starter"
echo "-----------------------"
echo "Starting..."
#기다리기
sleep 3


# 파이썬 파일이 있는 디렉터리 경로
directory_path="/home/dryoon/KIT_Discord_ChatBot"

# Git 저장소로 이동
cd "$directory_path"
echo "Git repository: $directory_path"
echo "-----------------------"
echo "변경사항 확인중..."
# Git 저장소에서 최신 변경사항 가져오기
git pull
echo "확인완료"
echo "-----------------------"
# 실행할 파이썬 파일 이름
python_file="main.py"

# 파이썬 파일 실행
python "$python_file"
echo "실행중..."
