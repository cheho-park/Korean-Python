import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import main


class MainTest(unittest.TestCase):
    def test_source_file_missing(self):
        with mock.patch.object(sys, "argv", ["main.py", "missing.kpy"]):
            self.assertEqual(main.main(), 1)

    def test_generate_output_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "example.kpy"
            output_path = Path(temp_dir) / "output.py"
            source_path.write_text('출력(\"hi\")\n', encoding="utf-8")

            with mock.patch.object(sys, "argv", ["main.py", str(source_path), "-o", str(output_path)]):
                self.assertEqual(main.main(), 0)
                self.assertTrue(output_path.exists())
                self.assertIn("print(\"hi\")", output_path.read_text(encoding="utf-8"))

    def test_invalid_generated_python_is_not_written(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "invalid.kpy"
            output_path = Path(temp_dir) / "output.py"
            source_path.write_text("만약 참\n    출력(\"hi\")\n", encoding="utf-8")

            with mock.patch.object(sys, "argv", ["main.py", str(source_path), "-o", str(output_path)]):
                self.assertEqual(main.main(), 1)
                self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
