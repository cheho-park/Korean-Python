import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

import Transpiler


class TranspilerTest(unittest.TestCase):
    def test_repeat_and_if_preprocess(self):
        code = """x = 1
반복 2번:
    출력(x)
만약 x 는 0 보다 크면:
    출력(\"ok\")
"""
        result = Transpiler.transpile(code)

        self.assertIn("for _ in range(2):", result)
        self.assertIn("if x > 0:", result)
        self.assertIn('print(\"ok\")', result)

    def test_keyword_in_multiline_string_is_ignored(self):
        code = """text = '''
반복 2번:
'''
출력(text)
"""
        result = Transpiler.transpile(code)

        self.assertIn("'''", result)
        self.assertNotIn("for _ in range(2):", result)
        self.assertIn("print(text)", result)

    def test_builtin_translation_on_call(self):
        code = """숫자 = 정수(입력())
출력(숫자)
"""
        result = Transpiler.transpile(code)

        self.assertIn("int(input())", result)
        self.assertIn("print(숫자)", result)

    def test_keyword_file_loads_from_module_path(self):
        module_path = Path(__file__).resolve().parent.parent / "Transpiler.py"
        current_dir = os.getcwd()

        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            try:
                spec = importlib.util.spec_from_file_location("transpiler_reload", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                self.assertTrue(module.KEYWORD_FILE.exists())
                self.assertIn("출력", module.keywords)
                result = module.transpile('출력(\"hello\")\n')
                self.assertIn('print("hello")', result)
            finally:
                os.chdir(current_dir)


if __name__ == "__main__":
    unittest.main()
