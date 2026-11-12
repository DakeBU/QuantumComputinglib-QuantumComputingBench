import unittest
from formal_redaction import redact, verify

class BoundedRedactionTests(unittest.TestCase):
    def test_plain_code_unchanged(self):
        text = "theorem t (x' : Int) : x' = x' := rfl\n"
        self.assertEqual(redact(text), (text, []))
    def test_line_comment(self):
        self.assertEqual(redact('x --ab\ny')[0], 'x     \ny')
    def test_nested_block(self):
        self.assertEqual(redact('/-a/-b-/c-/x')[0], ' ' * 11 + 'x')
    def test_strings_and_escapes(self):
        text = '"--/- \\" x" --tail\n'
        self.assertEqual(redact(text)[0], '"--/- \\" x"       \n')
    def test_quoted_identifier(self):
        self.assertEqual(redact('«a--/-b» --c\n')[0], '«a--/-b»    \n')
    def test_unicode_comment_and_crlf(self):
        self.assertEqual(redact('--雪😀\r\nx')[0], ' ' * 5 + '\nx')
    def test_unterminated_regions_rejected(self):
        for text in ('/- missing', '"missing', '«missing'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                redact(text)
    def test_unsupported_syntax_rejected(self):
        for text in ("'x'", 'r#"x"#'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                redact(text)
    def test_actual_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            verify(b'x --a\n', b'y    \n')

if __name__ == '__main__':
    unittest.main()
