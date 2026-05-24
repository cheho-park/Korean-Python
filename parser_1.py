class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # 현재 토큰 보기
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # 토큰 하나 소비
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    # 전체 파싱
    def parse(self):
        result = []

        while self.peek() is not None:
            token = self.peek()

            if token == "반복":
                result.append(self.parse_repeat())

            # elif token == "만약":
            #     result.append(self.parse_if())

            elif token is not None and token.startswith("출력"):
                result.append(self.parse_print())

            else:
                result.append(self.consume())

        return "\n".join(result)

    # 반복 5번:
    def parse_repeat(self):
        self.consume()  # 반복

        count = self.consume()
        if count is None:
            raise SyntaxError("반복문에 숫자가 필요합니다")

        count = count.replace("번:", "")

        return f"for _ in range({count}):"

    # 만약 x 는 3 보다 크면:
    def parse_if(self):
        self.consume()  # 만약

        left = self.consume()     # x
        self.consume()            # 는 / 은
        right = self.consume()    # 3
        self.consume()            # 보다

        compare = self.consume()  # 크면:

        if compare == "크면:":
            operator = ">"
        elif compare == "작으면:":
            operator = "<"
        else:
            raise SyntaxError("알 수 없는 비교 문법")

        return f"if {left} {operator} {right}:"

    # 출력("안녕")
    def parse_print(self):
        token = self.consume()

        content = token.replace("출력", "", 1)

        return f"print{content}"