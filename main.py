import io
import json
import tokenize

with open("keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

with open("hello.kpy", "r", encoding="utf-8") as f:
    code = f.read()

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

python_code = tokenize.untokenize(new_tokens)

print(python_code)

exec(python_code)