from io import StringIO
import tokenize as py_tokenize


def tokenize(code):
    result = []

    for token in py_tokenize.generate_tokens(StringIO(code).readline):
        if token.type in {
            py_tokenize.ENCODING,
            py_tokenize.INDENT,
            py_tokenize.DEDENT,
            py_tokenize.NL,
            py_tokenize.NEWLINE,
            py_tokenize.ENDMARKER,
            py_tokenize.COMMENT,
        }:
            continue

        result.append(token.string)

    return result
