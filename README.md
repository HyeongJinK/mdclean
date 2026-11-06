# Markdown 정리 도구

macOS에서 Markdown 파일을 순서대로 검사해 목록 항목 사이의 공백 들여쓰기를 정리하고, 내용이 명확한 fenced code block에만 언어 식별자를 붙입니다. Python 표준 라이브러리만 사용합니다.

## macOS에서 실행

터미널에서 이 폴더로 이동한 뒤 아래처럼 실행합니다. 폴더 경로를 생략하면 macOS 폴더 선택 창이 열립니다.

```sh
python3 mdclean.py
```

먼저 미리보기만 수행합니다. 변경 전후를 보려면:

```sh
python3 mdclean.py "/경로/문서 폴더" --diff
```

원본은 유지하고 정리본을 별도 폴더에 저장하려면:

```sh
python3 mdclean.py "/경로/문서 폴더" --write --output "/경로/문서 폴더-cleaned"
```

하위 폴더도 포함해 Markdown 파일을 이름순으로 처리합니다. 이미 생성한 출력 폴더가 원본 폴더 안에 있으면 대상에서 제외되도록 원본 폴더 바깥 경로를 지정해야 합니다.

원본에 직접 저장하는 방식은 다음 명령으로만 허용되며, 각 파일 옆에 `.md.bak` 백업을 만듭니다.

```sh
python3 mdclean.py "/경로/문서 폴더" --write --in-place --backup
```

## 자동 정리 범위

- 같은 들여쓰기 수준의 목록 항목 사이에서 공백 문자만 들어 있는 줄을 제거합니다. 중첩 목록 및 fenced code block 안은 수정하지 않습니다.
- 명확한 패턴이 있을 때 Java, Kotlin, Rust, Go, JavaScript, TypeScript, JSP, HTML, XML, JSON, Python, C/C++, C#, PHP, Ruby, Swift, SQL, CSS, Gradle, Dockerfile, Bash, properties, YAML 식별자를 추정합니다. ASCII 구조도와 일반 로그/출력은 그대로 둡니다. 이미 언어가 지정된 fence는 건드리지 않습니다.
- 모호한 코드 조각에는 아무 식별자도 추가하지 않습니다. 변경 파일 목록은 실행 결과에 표시됩니다.

## 테스트

업로드 샘플을 `tests/fixtures/spring-framework-vs-boot.md`에 포함했습니다.

```sh
python3 -m unittest -v
```
