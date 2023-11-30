import base64

def encode_file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            # 파일 읽기
            file_content = file.read()

            # base64로 인코딩
            encoded_content = base64.b64encode(file_content)

            return encoded_content.decode('utf-8')  # 문자열로 디코딩하여 반환

    except FileNotFoundError:
        return f"파일이 {file_path} 경로에 존재하지 않습니다."

if __name__ == "__main__":
    file_path = ("discord_api_token.txt")  # 실제 파일 경로로 변경해주세요
    encoded_data = encode_file_to_base64(file_path)

    if not encoded_data.startswith("파일이"):
        print(f"{file_path} 파일을 base64로 인코딩한 결과:\n{encoded_data}")
    else:
        print(encoded_data)
