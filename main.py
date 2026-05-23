import json

# 키워드 불러오기
with open("keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

# kpy 파일 읽기
with open("helloㅁㄴㅇㄹ.kpy", "r", encoding="utf-8") as f:
    code = f.read()

# 키워드 변환
for k, v in keywords.items():
    code = code.replace(k, v)

print("변환된 코드:")
print(code)

print("\n실행 결과:")
exec(code) 