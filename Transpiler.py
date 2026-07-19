from pathlib import Path
import io
import json
import re
import tokenize
from typing import Optional

KEYWORD_FILE = Path(__file__).resolve().parent / "keywords.json"
with KEYWORD_FILE.open("r", encoding="utf-8") as f:
    keywords = json.load(f)


_repeat_pattern = re.compile(r"^(?P<indent>\s*)반복\s+(?P<count>.+?)번:\s*$")
_if_pattern = re.compile(
    r"^(?P<indent>\s*)만약\s+(?P<left>.+?)\s+(?:는|은)\s+(?P<right>.+?)\s+보다\s+(?P<compare>크면|작으면):\s*$"
)

_ALWAYS_TRANSLATE = {
    "만약",
    "다른",
    "그렇지않으면",
    "반복",
    "동안",
    "함수",
    "반환",
    "클래스",
    "시도",
    "예외발생",
    "최종적으로",
    "불러오다",
    "프롬",
    "글로벌",
    "그리고",
    "또는",
    "아님",
    "델",
    "멈춤",
    "계속",
    "통과",
    "비동기",
    "기다려",
    "매치",
    "경우",
}
_LITERAL_TRANSLATE = {"참", "거짓", "비어있음"}
_BUILTIN_CALL_NAMES = {
    "출력",
    "입력",
    "정수",
    "실수",
    "문자열",
    "리스트",
    "튜플",
    "딕셔너리",
    "집합",
    "불",
    "범위",
    "길이",
    "타입",
    "열거",
    "압축",
    "정수로",
    "실수로",
    "문자열로",
    "절대값",
    "최대",
    "최소",
    "합계",
}


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


def _scan_multiline_string_state(line: str, current_state: Optional[str]) -> Optional[str]:
    index = 0
    while index < len(line):
        if current_state is None:
            if line[index] == "#":
                break
            if line.startswith("'''", index) or line.startswith('"""', index):
                current_state = line[index : index + 3]
                index += 3
                continue
            index += 1
        else:
            if line.startswith(current_state, index):
                current_state = None
                index += 3
                continue
            if line[index] == "\\":
                index += 2
            else:
                index += 1
    return current_state


def _preprocess(code: str) -> str:
    lines = []
    multiline_state: Optional[str] = None

    for line in code.splitlines():
        if multiline_state is None:
            lines.append(_rewrite_line(line))
        else:
            lines.append(line)

        multiline_state = _scan_multiline_string_state(line, multiline_state)

    return "\n".join(lines)


def _previous_meaningful_token(tokens, index: int):
    idx = index - 1
    while idx >= 0:
        if tokens[idx].type not in {
            tokenize.ENCODING,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.COMMENT,
        }:
            return tokens[idx]
        idx -= 1
    return None


def _next_meaningful_token(tokens, index: int):
    idx = index + 1
    while idx < len(tokens):
        if tokens[idx].type not in {
            tokenize.ENCODING,
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.COMMENT,
        }:
            return tokens[idx]
        idx += 1
    return None


def _should_translate_name(token_string: str, tokens, index: int) -> bool:
    if token_string in _ALWAYS_TRANSLATE or token_string in _LITERAL_TRANSLATE:
        return True

    if token_string in _BUILTIN_CALL_NAMES:
        previous = _previous_meaningful_token(tokens, index)
        if previous is not None and previous.type == tokenize.OP and previous.string == ".":
            return False

        next_token = _next_meaningful_token(tokens, index)
        if next_token is not None and next_token.type == tokenize.OP and next_token.string == "(":
            return True

    return False


def transpile(code: str) -> str:
    code = _preprocess(code)

    tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    new_tokens = []

    for index, token in enumerate(tokens):
        token_string = token.string

        if token.type == tokenize.NAME and _should_translate_name(token_string, tokens, index):
            token_string = keywords.get(token_string, token_string)

        new_tokens.append(
            tokenize.TokenInfo(
                token.type,
                token_string,
                token.start,
                token.end,
                token.line,
            )
        )

    return tokenize.untokenize(new_tokens)
