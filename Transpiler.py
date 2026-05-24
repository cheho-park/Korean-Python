import io
import json
import tokenize
import re

with open("keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

def transpile(code: str) -> str:
    # Apply replacements sequentially
    code = re.sub(
        r"반복\s+(\d+)번:",
        r"for _ in range(\1):",
        code
        )
    print(code)
    code = re.sub(
        r"만약\s+([^\s]+)\s+(?:는|은)\s+([^\s]+)\s+보다\s+크면:",
        r"if \1 > \2:",
        code
    )
    print(code)

    tokens = tokenize.generate_tokens(io.StringIO(code).readline)

    new_tokens = []

    for token in tokens:
        token_type = token.type
        token_string = token.string

        if token_type == tokenize.NAME:
            token_string = keywords.get(token_string, token_string)

        new_tokens.append(
            (
                token_type,
                token_string
            )
        )

    return tokenize.untokenize(new_tokens)