import io
import json
import re
import tokenize

with open("keywords.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)


_repeat_pattern = re.compile(r"^(?P<indent>\s*)반복\s+(?P<count>.+?)번:\s*$")
_if_pattern = re.compile(
    r"^(?P<indent>\s*)만약\s+(?P<left>.+?)\s+(?:는|은)\s+(?P<right>.+?)\s+보다\s+(?P<compare>크면|작으면):\s*$"
)


def _rewrite_line(code_line: str) -> str:
    repeat_match = _repeat_pattern.match(code_line)
    if repeat_match:
        return f"{repeat_match.group('indent')}for _ in range({repeat_match.group('count')}):"

    if_match = _if_pattern.match(code_line)
    if if_match:
        operator = ">" if if_match.group("compare") == "크면" else "<"
        return (
            f"{if_match.group('indent')}if {if_match.group('left')} "
            f"{operator} {if_match.group('right')}:"
        )

    return code_line


def _preprocess(code: str) -> str:
    return "\n".join(_rewrite_line(line) for line in code.splitlines())


def transpile(code: str) -> str:
    code = _preprocess(code)

    tokens = tokenize.generate_tokens(io.StringIO(code).readline)

    new_tokens = []

    for token in tokens:
        token_type = token.type
        token_string = token.string

        if token_type == tokenize.NAME:
            token_string = keywords.get(token_string, token_string)

        new_tokens.append((token_type, token_string))

    return tokenize.untokenize(new_tokens)
