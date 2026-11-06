#!/usr/bin/env python3
"""Conservative Markdown cleanup with preview-first, non-destructive output."""
from __future__ import annotations

import argparse
import difflib
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

FENCE = re.compile(r"^(?P<indent> {0,3})(?P<mark>`{3,}|~{3,})(?P<info>.*)$")
LIST = re.compile(r"^(?P<indent> *)(?:[-+*]|\d+[.)])\s+")


@dataclass
class Result:
    text: str
    changes: list[str]


def infer_language(body: list[str]) -> str | None:
    text = "\n".join(body).strip()
    if not text:
        return None
    # Strong signatures only: tree/sequence diagrams and plain output remain untouched.
    if re.search(r"(?m)^\s*(?:[+|].*[+|]|[|+v^]--+|[-+]{3,})\s*$", text) and not re.search(r"(?m)^\s*(?:<\w|\{|public |@\w)", text):
        return None
    # Web templates and markup: specialize before the generic XML tag rule.
    if re.search(r"<%[=!?@]?|<%--", text):
        return "jsp"
    if re.search(r"(?is)<!doctype\s+html|<html\b|<(?:head|body|div|main|section|article|form|input|button|script|style)\b", text):
        return "html"
    if re.search(r"^\s*<\?xml\b|^\s*</?[A-Za-z][\w:.-]*(?:\s|>|/)", text, re.M):
        return "xml"
    if re.search(r"(?m)^\s*(?:\{|\[)\s*$", text) and re.search(r'"[\w-]+"\s*:', text):
        return "json"
    # Kotlin and JVM languages.
    if re.search(r"(?m)^\s*(?:fun\s+main\s*\(|data\s+class\s+|sealed\s+(?:class|interface)\s+|object\s+\w+|val\s+\w+\s*:|var\s+\w+\s*=)", text):
        return "kotlin"
    if re.search(r"(?m)^\s*(?:package\s+[\w.]+;|import\s+[\w.*]+;|public\s+(?:class|interface|enum|record)\s+|class\s+\w+\s*\{|@SpringBootApplication|@Configuration|@Bean\b)", text):
        return "java"
    # Rust, Go, then JavaScript/TypeScript. TypeScript checks precede JS.
    if re.search(r"(?m)^\s*(?:fn\s+main\s*\(|use\s+[\w:]+\s*;|pub\s+(?:fn|struct|enum|mod)\b|let\s+mut\s+|impl(?:<[^>]+>)?\s+\w+)", text):
        return "rust"
    if re.search(r"(?m)^\s*(?:package\s+main\b|func\s+main\s*\(|func\s+\w+\s*\(|import\s+\(\s*$|type\s+\w+\s+struct\s*\{)", text):
        return "go"
    if re.search(r"(?m)^\s*(?:interface\s+\w+\s*\{|type\s+\w+\s*=|(?:const|let|var)\s+\w+\s*:\s*(?:string|number|boolean|\w+\[)|function\s+\w+\s*\([^)]*:\s*\w+)", text):
        return "typescript"
    if re.search(r"(?m)^\s*(?:export\s+default\b|export\s+(?:const|function|class)\b|(?:const|let|var)\s+\w+\s*=|function\s+\w+\s*\(|console\.(?:log|error)\s*\(|document\.(?:querySelector|getElementById))", text):
        return "javascript"
    if re.search(r"(?m)^\s*(?:def\s+\w+\s*\(|from\s+\w+\s+import\s+|if\s+__name__\s*==|class\s+\w+\s*:\s*$|print\s*\()", text):
        return "python"
    if re.search(r"(?m)^\s*(?:#include\s*[<\"]|int\s+main\s*\(|std::\w+|using\s+namespace\s+std\s*;)", text):
        return "cpp" if re.search(r"std::|using\s+namespace\s+std|#include\s*<iostream>", text) else "c"
    if re.search(r"(?m)^\s*(?:using\s+System\s*;|namespace\s+[\w.]+\s*\{|public\s+static\s+void\s+Main\s*\()", text):
        return "csharp"
    if re.search(r"(?m)^\s*<\?php\b|\$\w+\s*=\s*\$", text):
        return "php"
    if re.search(r"(?m)^\s*(?:require\s+['\"]|puts\s+['\"]|def\s+\w+\s*$|end\s*$)", text) and not re.search(r"(?m)^\s*def\s+\w+\s*\(", text):
        return "ruby"
    if re.search(r"(?m)^\s*(?:import\s+Foundation|func\s+\w+\s*\([^)]*\)\s*(?:->|\{)|guard\s+let\s+)", text):
        return "swift"
    if re.search(r"(?im)^\s*(?:select\s+.+\s+from\s+|insert\s+into\s+|create\s+table\s+|update\s+\w+\s+set\s+)", text):
        return "sql"
    if re.search(r"^\s*@(?:media|import|keyframes)\b|^[.#][\w-]+(?:\s+[.#]?[\w-]+)?\s*\{", text, re.M) and re.search(r"^\s*[\w-]+\s*:\s*[^:;]+;", text, re.M):
        return "css"
    if re.search(r"(?m)^\s*(?:plugins\s*\{|dependencies\s*\{|implementation\s+['\"]|id\s+['\"]org\.springframework)", text):
        return "gradle"
    if re.search(r"(?m)^\s*(?:FROM\s+\S+|RUN\s+\S+|COPY\s+\S+|WORKDIR\s+\S+)", text) and re.search(r"(?m)^\s*FROM\s+", text):
        return "dockerfile"
    if re.search(r"(?m)^\s*(?:\$\s+|#!.*(?:sh|bash)|(?:java|mvn|gradle|curl)\s+-[\w])", text):
        return "bash"
    if re.search(r"(?m)^\s*(?:server\.port=|spring\.[\w.-]+=)", text):
        return "properties"
    if re.search(r"(?m)^\s*(?:---\s*$|(?:server|spring|management|logging|apiVersion|kind|metadata|spec):\s*(?:$|[^/])|\s{2,}[\w-]+:\s)", text) and not re.search(r"(?m)^\s*(?:\||\+|v|[-+]{3,})", text):
        return "yaml"
    return None


def clean_markdown(source: str) -> Result:
    lines = source.splitlines(keepends=True)
    out: list[str] = []
    changes: list[str] = []
    in_fence = False
    fence_mark = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line.rstrip("\r\n"))
        if not in_fence and m:
            in_fence, fence_mark = True, m.group("mark")
            info = m.group("info").strip()
            body: list[str] = []
            j = i + 1
            close_re = re.compile(r"^ {0,3}" + re.escape(fence_mark[0]) + "{" + str(len(fence_mark)) + r",}\s*$")
            while j < len(lines) and not close_re.match(lines[j].rstrip("\r\n")):
                body.append(lines[j].rstrip("\r\n")); j += 1
            lang = infer_language(body) if not info else None
            out.append(line)
            if lang:
                # Keep fence indentation and delimiter; add only an inferred language.
                out[-1] = m.group("indent") + fence_mark + lang + ("\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else "")
                changes.append(f"added {lang} fence")
            out.extend(lines[i+1:j])
            if j < len(lines): out.append(lines[j]); i = j
            in_fence = False
            i += 1
            continue
        # Remove blank separators (with or without spaces) between peer list items.
        if line.strip() == "":
            prev = next((x for x in reversed(out) if x.strip()), "")
            nxt = next((x for x in lines[i+1:] if x.strip()), "")
            a, b = LIST.match(prev), LIST.match(nxt)
            if a and b and len(a.group("indent")) == len(b.group("indent")):
                changes.append("removed blank separator between peer list items")
                i += 1
                continue
        out.append(line); i += 1
    return Result("".join(out), changes)


def markdown_files(root: Path):
    # Stable, sequential order; skip generated output and hidden directories.
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".markdown", ".mdown"} and not any(p.startswith(".") for p in path.relative_to(root).parts):
            yield path


def process(root: Path, output: Path | None, write: bool, in_place: bool, backup: bool) -> list[tuple[Path, list[str]]]:
    report = []
    for src in markdown_files(root):
        raw = src.read_bytes()
        encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
        text = raw.decode(encoding)
        result = clean_markdown(text)
        if result.text != text:
            report.append((src, result.changes))
            if write:
                if in_place:
                    if backup:
                        shutil.copy2(src, src.with_suffix(src.suffix + ".bak"))
                    src.write_bytes(result.text.encode(encoding))
                else:
                    assert output is not None
                    target = output / src.relative_to(root)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(result.text.encode(encoding))
    return report


def choose_directory() -> Path | None:
    try:
        import tkinter as tk
        from tkinter import filedialog
        app = tk.Tk(); app.withdraw()
        value = filedialog.askdirectory(title="Markdown 파일이 있는 폴더 선택")
        app.destroy()
        return Path(value) if value else None
    except Exception as exc:
        print(f"폴더 선택 창을 열 수 없습니다: {exc}", file=sys.stderr)
        return None


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Markdown 목록 들여쓰기 정리 및 코드 fence 언어 추정")
    p.add_argument("directory", nargs="?", type=Path, help="대상 폴더 (생략하면 macOS 폴더 선택 창)")
    p.add_argument("--write", action="store_true", help="변경 결과 저장 (기본값은 미리보기)")
    p.add_argument("--output", type=Path, help="원본을 보존할 별도 출력 폴더")
    p.add_argument("--in-place", action="store_true", help="원본에 저장; --backup 필수")
    p.add_argument("--backup", action="store_true", help="덮어쓰기 전 .bak 백업 생성")
    p.add_argument("--diff", action="store_true", help="변경 내용 미리보기")
    args = p.parse_args(argv)
    root = args.directory or choose_directory()
    if not root: return 2
    root = root.expanduser().resolve()
    if not root.is_dir(): p.error(f"폴더가 아닙니다: {root}")
    if args.in_place and (not args.write or not args.backup): p.error("--in-place에는 --write와 --backup이 모두 필요합니다")
    if args.write and not args.in_place and not args.output: p.error("저장하려면 --output 경로를 지정하거나 --in-place --backup을 사용하세요")
    if args.output and args.output.expanduser().resolve().is_relative_to(root): p.error("출력 폴더는 대상 폴더 바깥에 지정하세요")
    if args.diff:
        for src in markdown_files(root):
            old = src.read_text(encoding="utf-8-sig")
            new = clean_markdown(old).text
            if old != new:
                print(f"--- {src}\n+++ 정리 결과")
                sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True)))
    report = process(root, args.output.expanduser().resolve() if args.output else None, args.write, args.in_place, args.backup)
    print(f"검사 완료: 변경 대상 {len(report)}개 파일")
    for path, actions in report:
        print(f"- {path.relative_to(root)}: {', '.join(dict.fromkeys(actions))}")
    if args.write and not args.in_place: print(f"저장 위치: {args.output.expanduser().resolve()}")
    elif not args.write: print("미리보기만 수행했습니다. 저장하려면 --write와 --output을 지정하세요.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
