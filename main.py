from pathlib import Path
import sys
import argparse

from Transpiler import transpile


def main():
    parser = argparse.ArgumentParser(
        description="한글 Python 파일을 Python 코드로 변환합니다."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default="hello.kpy",
        help="변환할 .kpy 파일 경로",
    )
    parser.add_argument(
        "-o",
        "--out",
        help="생성할 .py 파일 경로",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="생성된 Python 파일을 바로 실행",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    filename = Path(args.source)

    if not filename.exists() or not filename.is_file():
        print(f"파일을 찾을 수 없습니다: {filename}")
        return 1

    try:
        code = filename.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"파일을 읽는 동안 오류가 발생했습니다: {exc}")
        return 1

    python_code = transpile(code)

    output_path = Path(args.out) if args.out else filename.with_suffix(".py")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(python_code, encoding="utf-8")
    except OSError as exc:
        print(f"출력 파일을 생성하는 동안 오류가 발생했습니다: {exc}")
        return 1

    print(f"생성 완료: {output_path}")

    if args.run:
        print("\n=== OUTPUT ===")
        try:
            exec(compile(python_code, str(output_path), "exec"), {"__name__": "__main__"})
        except EOFError:
            print("표준 입력이 필요하지만 현재 입력이 비어 있습니다.")
            return 2
        except Exception as exc:
            print(f"생성된 코드 실행 중 오류가 발생했습니다: {exc}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
