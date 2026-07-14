from pathlib import Path
import sys

from Transpiler import transpile


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    filename = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("hello.kpy")

    if not filename.exists():
        print(f"파일을 찾을 수 없습니다: {filename}")
        return 1

    code = filename.read_text(encoding="utf-8")
    python_code = transpile(code)

    print("=== PYTHON CODE ===")
    print(python_code)
    print("\n=== OUTPUT ===")

    try:
        exec(compile(python_code, str(filename), "exec"), {"__name__": "__main__"})
    except EOFError:
        print("표준 입력이 필요하지만 현재 입력이 비어 있습니다.")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
