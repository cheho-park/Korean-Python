# Korean Python

한글 키워드로 작성한 `.kpy` 파일을 일반 Python 코드로 변환하는 작은 트랜스파일러 프로젝트입니다.

## Contributing

기여하고 싶다면 다음 순서로 진행해주세요.

1. 이 저장소를 Fork 합니다.
2. 기능을 수정하거나 추가합니다.
3. 변경사항을 commit 합니다.
4. Pull Request를 생성합니다.
5. PR에서 변경 내용을 설명해주세요.

## 개요

이 프로젝트의 목표는 **한글 문법으로 Python을 더 편하게 쓰는 환경**을 만드는 것입니다.
현재 구조는 다음 흐름으로 동작합니다.

`hello.kpy` → `Transpiler.py` → `hello.py` → 실행

이 트랜스파일러는 `Transpiler.py` 모듈 기준으로 키워드 매핑 파일을 로드하므로, 프로젝트 루트가 아닌 위치에서도 실행할 수 있습니다.

즉, 이 프로젝트는 인터프리터라기보다 **한글 Python 트랜스파일러**에 가깝습니다.

## 특징

- 한글 키워드를 Python 키워드로 변환
- `출력`, `입력`, `함수`, `만약`, `반복` 같은 기본 문법 지원
- `반복 3번:` 같은 자연스러운 표현 지원
- `만약 x 는 3 보다 크면:` 같은 비교 문법 지원
- `.py` 파일로 변환한 뒤 바로 실행 가능

## 파일 구조

- `main.py` : CLI 진입점
- `Transpiler.py` : 한글 Python → Python 변환기
- `keywords.json` : 한글 키워드 매핑 테이블
- `tokenizer.py` : 토큰 처리 보조 도구
- `hello.kpy` : 예제 소스 코드

## 사용법

### 1. Python 파일 생성

```bash
python main.py hello.kpy
```

기본적으로 `hello.py`가 생성됩니다.

### 2. 출력 파일 지정

```bash
python main.py hello.kpy -o build/hello.py
```

원하는 경로에 Python 파일을 저장할 수 있습니다.

### 3. 생성 후 바로 실행

```bash
python main.py hello.kpy --run
```

`.py` 파일을 만든 뒤 즉시 실행합니다.

## 문법 예시

### 출력

```kpy
출력("헬로우 월드")
```

```python
print("헬로우 월드")
```

### 입력

```kpy
이름 = 입력()
숫자 = 정수(입력())
```

```python
이름 = input()
숫자 = int(input())
```

### 함수

```kpy
함수 인사(이름):
    출력("안녕, " + 이름)
```

```python
def 인사(이름):
    print("안녕, " + 이름)
```

### 조건문

```kpy
만약 x 는 3 보다 크면:
    출력("큼")
```

```python
if x > 3:
    print("큼")
```

### 반복문

```kpy
반복 3번:
    출력("안녕")
```

```python
for _ in range(3):
    print("안녕")
```

## 지원 키워드

`keywords.json` 기준으로 다음 키워드들이 매핑됩니다.

- `출력` → `print`
- `입력` → `input`
- `함수` → `def`
- `반환` → `return`
- `만약` → `if`
- `다른` → `elif`
- `그렇지않으면` → `else`
- `반복` → `for`
- `동안` → `while`
- `정수` → `int`
- `실수` → `float`
- `문자열` → `str`
- `참` → `True`
- `거짓` → `False`

## 현재 상태

이 프로젝트는 아직 성장 중입니다.
지금은 다음 방향으로 확장할 수 있습니다.

- 더 많은 문법 지원
- 함수 호출/표현식 안정화
- 문자열, 괄호, 들여쓰기 처리 강화
- `parser_1.py` 정리 또는 통합
- 에러 메시지 개선

## 예제 실행

```bash
python main.py hello.kpy --run
```

입력값이 필요한 코드라면 실행 중 표준 입력을 받을 수 있습니다.

## 라이선스

이 프로젝트는 저장소에 포함된 `LICENSE` 파일을 따릅니다.

