def tokenize(code):
    lines = code.splitlines()

    result = []

    for line in lines:
        result.append(line.strip())

    return result