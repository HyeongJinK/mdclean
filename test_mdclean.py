import unittest

from mdclean import clean_markdown, infer_language


class CleanerTests(unittest.TestCase):
    def test_normalizes_indented_blank_between_peer_items(self):
        source = "- one\n    \n- two\n"
        self.assertEqual(clean_markdown(source).text, "- one\n- two\n")

    def test_removes_plain_blank_between_peer_items(self):
        source = "- one\n\n- two\n"
        self.assertEqual(clean_markdown(source).text, "- one\n- two\n")

    def test_keeps_nested_lists_and_code_unchanged(self):
        source = "- parent\n  - child\n    \n    code\n"
        self.assertEqual(clean_markdown(source).text, source)

    def test_adds_java_and_xml_labels(self):
        source = "```\npublic class Demo {\n}\n```\n\n```\n<dependencies>\n</dependencies>\n```\n"
        self.assertEqual(clean_markdown(source).text, "```java\npublic class Demo {\n}\n```\n\n```xml\n<dependencies>\n</dependencies>\n```\n")

    def test_does_not_label_diagram_or_output(self):
        self.assertIsNone(infer_language(["A", " |", " v", "B"]))
        self.assertIsNone(infer_language(["Tomcat started on port 8080"]))

    def test_detects_common_languages(self):
        examples = {
            "kotlin": ["fun main() {", "    println(\"hi\")", "}"],
            "rust": ["fn main() {", "    println!(\"hi\");", "}"],
            "go": ["package main", "func main() {}"],
            "javascript": ["const message = 'hi';", "console.log(message);"],
            "typescript": ["const count: number = 1;"],
            "jsp": ["<%@ page contentType=\"text/html\" %>", "<%= user.getName() %>"],
            "html": ["<!DOCTYPE html>", "<html><body>Hello</body></html>"],
            "python": ["def main():", "    print('hi')"],
            "sql": ["SELECT id, name FROM users;"],
        }
        for expected, body in examples.items():
            with self.subTest(language=expected):
                self.assertEqual(infer_language(body), expected)

    def test_sample_fixture_is_stable_and_only_fixes_known_patterns(self):
        from pathlib import Path
        sample = Path(__file__).parent / "tests/fixtures/spring-framework-vs-boot.md"
        original = sample.read_text(encoding="utf-8")
        first = clean_markdown(original)
        second = clean_markdown(first.text)
        self.assertEqual(first.text, second.text)
        self.assertGreaterEqual(first.text.count("```java"), 4)
        self.assertGreaterEqual(first.text.count("```xml"), 2)
        self.assertIn("```\n                 Spring Boot", first.text)  # ASCII architecture diagram preserved
        self.assertIn("- Spring Framework 라이브러리 추가\n- 필요한 의존성 버전 관리", first.text)


if __name__ == "__main__":
    unittest.main()
