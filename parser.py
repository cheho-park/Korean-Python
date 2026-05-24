class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        if self.tokens[0] == "반복":
            return self.parse_repeat()

    def parse_repeat(self):
        count = self.tokens[1]

        count = count.replace("번:", "")

        return f"for _ in range({count}):"