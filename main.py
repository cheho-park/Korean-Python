from parser_1 import Parser
import sys


# 간단한 tokenizer
def tokenize(code):
    return code.split()


def main():
    # 파일 인자 확인
    # if len(sys.argv) < 2:
    #     print("사용법: python main.py 파일.kpy")
    #     return

    # filename = sys.argv[1]
    filename = "hello.kpy"

    # 파일 읽기
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    # 토큰화
    tokens = tokenize(code)

    print("=== TOKENS ===")
    print(tokens)

    # 파싱
    parser = Parser(tokens)

    python_code = parser.parse()

    print("\n=== PYTHON CODE ===")
    print(python_code)

    print("\n=== OUTPUT ===")

    # 실행
    exec(python_code)


if __name__ == "__main__":
    main()