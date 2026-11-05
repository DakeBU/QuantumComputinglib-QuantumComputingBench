"""Bounded Lean comment redaction checker, not a general lexer certificate.

Preserves strings and quoted identifiers; refuses unsupported raw strings and
character-literal syntax rather than asserting general lexical equivalence.
It changes only comments to UTF-16-width spaces and normalizes CRLF to LF.
"""
import re

def redact(text):
    parts = []
    i = 0
    comments = []
    while i < len(text):
        start = i
        if text.startswith('--', i):
            end = i + 2
            while end < len(text) and text[end] not in '\r\n':
                end += 1
            comments.append((i, end, 'line'))
        elif text.startswith('/-', i):
            end, depth = i + 2, 1
            while end < len(text) and depth:
                if text.startswith('/-', end):
                    depth += 1
                    end += 2
                elif text.startswith('-/', end):
                    depth -= 1
                    end += 2
                else:
                    end += 1
            if depth:
                raise ValueError('unterminated block comment')
            comments.append((i, end, 'block'))
        elif text[i] in ('"', '«'):
            close = '"' if text[i] == '"' else '»'
            end = i + 1
            while end < len(text):
                if close == '"' and text[end] == '\\':
                    end += 2
                    continue
                if text[end] == close:
                    end += 1
                    break
                end += 1
            else:
                raise ValueError('unterminated string or quoted identifier')
            parts.append(text[i:end])
            i = end
            continue
        else:
            if text.startswith('r#', i) or (text[i] == "'" and
                    re.match(r"'(?:[^'\r\n]|\\[^\r\n]+)'", text[i:])):
                raise ValueError('unsupported raw-string or character-literal syntax')
            parts.append(text[i])
            i += 1
            continue
        assert start == i and end > i
        parts.append(''.join(c if c in '\r\n' else ' ' * (len(c.encode('utf-16-le')) // 2)
                             for c in text[i:end]))
        i = end
    return ''.join(parts).replace('\r\n', '\n'), comments

def verify(raw, formal):
    expected, comments = redact(raw.decode('utf-8-sig'))
    if expected.encode('utf-8') != formal:
        raise ValueError('formal bytes differ from bounded comment-only redaction')
    return {'comment_regions': len(comments), 'line_comments': sum(t == 'line' for _, _, t in comments),
            'block_comments': sum(t == 'block' for _, _, t in comments),
            'formal_bytes_equal': True, 'general_Lean_lexer_proof': False}
