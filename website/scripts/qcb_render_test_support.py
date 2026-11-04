"""Independent recovery of source text from server-rendered math spans in tests."""
import hashlib
from html.parser import HTMLParser


def recover_prose_source(page, original):
    target = hashlib.sha256(original.encode()).hexdigest()

    class SourceReader(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.depth = 0
            self.math_depth = 0
            self.parts = []
            self.found = False

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if not self.depth:
                if attrs.get('data-qcb-text-sha256') == target and not self.found:
                    self.depth = 1
                    self.found = True
                return
            if tag == 'br':
                if not self.math_depth:
                    self.parts.append('\n')
                return
            if self.math_depth:
                self.math_depth += 1
            elif 'data-qcb-math-source' in attrs:
                self.parts.append(attrs['data-qcb-math-source'])
                self.math_depth = 1
            elif tag == 'p' and self.parts:
                self.parts.append('\n\n')
            self.depth += 1

        def handle_endtag(self, tag):
            if self.depth:
                self.depth -= 1
                if self.math_depth:
                    self.math_depth -= 1

        def handle_data(self, data):
            if self.depth and not self.math_depth:
                self.parts.append(data)

    parser = SourceReader()
    parser.feed(page)
    if not parser.found:
        raise AssertionError('No rendering bound to this exact original question/answer.')
    return ''.join(parser.parts)
