from tokenizer import tokenize
from parser import Parser

code = "반복 5번:"

tokens = tokenize(code)

parser = Parser(tokens)

python_code = parser.parse()

print(python_code)