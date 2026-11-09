"""Safe, source-bound mathematical prose for the public quantum exercise book.

Explicit TeX is rendered as TeX. Legacy algebra is recognized by a bounded
grammar, not by asking a model to rewrite a mathematical statement. Unknown
words and ambiguous notation stay literal. Every generated formula retains its
exact source substring and digest for inspection.
"""
from __future__ import annotations

import hashlib
import html
import re
from dataclasses import dataclass
from urllib.parse import urlsplit


def _esc(value):
    return html.escape(str(value), quote=True)


def text_hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


_GREEK = {name: '\\' + name for name in (
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta', 'eta',
    'theta', 'vartheta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi',
    'rho', 'sigma', 'tau', 'upsilon', 'phi', 'varphi', 'chi', 'psi', 'omega')}
_FUNCTIONS = {'sin', 'cos', 'tan', 'exp', 'log', 'ln', 'sqrt', 'min', 'max',
              'rank', 'det', 'dim', 'diag', 'conj', 'Re', 'Im', 'Tr', 'normSq',
              'pairNorm', 'degree', 'natDegree'}
_LABELS = {'out', 'in', 'bit', 'old', 'new', 'newbond', 'oldbond', 'left', 'right', 'row', 'column'}
_BINARY = {'=': (1, '='), '≠': (1, r'\ne '), '<=': (1, r'\le '),
           '>=': (1, r'\ge '), '≤': (1, r'\le '), '≥': (1, r'\ge '),
           '<': (1, '<'), '>': (1, '>'), '≈': (1, r'\approx '),
           '+': (2, '+'), '-': (2, '-'), '−': (2, '-'),
           '*': (3, r'\cdot '), '·': (3, r'\cdot '), '/': (3, '/'),
           '⊗': (3, r'\otimes '), '∘': (3, r'\circ ')}
_TOKEN = re.compile(r'\s*(<=|>=|[A-Za-z]+|[Α-ω]|\d+(?:\.\d+)?|[^\s])')
_PROTECTED = re.compile(
    r'(?:https?://|mailto:|www\.)[^\s]+|(?:[A-Za-z]:[\\/]|(?<!\S)/)[\w./\\-]+'
    r'|\b\d{4}-\d{2}-\d{2}\b|\b[\w.-]+\.(?:py|lean|json|html|toml|md)\b')
_UNSAFE_TEX = re.compile(
    r'\\(?:href|url|class|cssId|style|html\w*|require|includegraphics|input|include|'
    r'openout|write|read|def|gdef|edef|xdef|let|newcommand|renewcommand|csname|'
    r'catcode|color|colorbox|fcolorbox|bbox)\b', re.IGNORECASE)
# A single given block-encoding formula needs bra/ket typography that the
# arithmetic grammar deliberately does not infer. Match these exact tokens
# (with whitespace variations) rather than converting arbitrary ket prose.
_GIVEN_BLOCK_COMPRESSION = re.compile(
    r'(?<![\w^])(?P<lhs>B\s*=\s*)?'
    r'\(\s*<\s*0\s*\^\s*a\s*\|\s*tensor\s+I\s*\)\s*'
    r'U\s*\(\s*\|\s*0\s*\^\s*a\s*>\s*tensor\s+I\s*\)'
    r'(?!\w)')


@dataclass(frozen=True)
class AlgebraSpan:
    start: int
    end: int
    source: str
    tex: str


class _Algebra:
    """Small arithmetic grammar: no word segmentation, evaluation or rewriting."""
    def __init__(self, text, start):
        self.text, self.start, self.pos, self.count = text, start, start, 0
        self.interesting = False
        self.invalid = False
        self.allow_labels = False

    def peek(self):
        match = _TOKEN.match(self.text, self.pos)
        if match is None or match.end() - self.start > 320 or self.count >= 120:
            return None
        return match.group(1), match.start(1), match.end()

    def take(self):
        token = self.peek()
        if token:
            self.pos, self.count = token[2], self.count + 1
        return token

    @staticmethod
    def name(raw, *, labels=False):
        if re.fullmatch(r'\d+(?:\.\d+)?', raw):
            return raw
        if len(raw) == 1 and raw.isalpha():
            return raw
        if raw in _GREEK:
            return _GREEK[raw] + ' '
        if raw in _FUNCTIONS:
            return r'\operatorname{' + raw + '}'
        if labels and raw in _LABELS:
            return r'\mathrm{' + raw + '}'
        return None

    def atom(self, depth):
        if depth > 12:
            return None
        token = self.peek()
        if token is None:
            return None
        raw = token[0]
        if raw in ('+', '-', '−'):
            checkpoint = self.pos
            self.take()
            right = self.atom(depth + 1)
            if right is None:
                self.pos = checkpoint
                return None
            return ('-' if raw == '−' else raw) + right
        if raw in ('(', '[', '{'):
            value = self.group(depth + 1)
        else:
            value = self.name(raw, labels=self.allow_labels)
            if raw in _FUNCTIONS:
                following = _TOKEN.match(self.text, token[2])
                if following is None or following.group(1) not in {'(', '^', '_'}:
                    value = None
            if value is not None:
                self.take()
        if value is None:
            return None
        scripts = set()
        while (next_token := self.peek()) is not None:
            op = next_token[0]
            checkpoint = self.pos
            if op in ('^', '_'):
                if op in scripts:
                    self.invalid = True
                    return None
                self.take()
                exponent = self.peek()
                if exponent and exponent[0] in ('(', '{'):
                    suffix = self.group(depth + 1, bare=True)
                elif exponent and exponent[0] in ('-', '+', '−'):
                    suffix = self.atom(depth + 1)
                elif exponent and exponent[0] in ('*', '†', 'ᵀ'):
                    self.take()
                    suffix = {'*': '*', '†': r'\dagger', 'ᵀ': r'\mathsf{T}'}[exponent[0]]
                elif exponent:
                    suffix = r'\dagger' if exponent[0] == 'dagger' else self.name(exponent[0], labels=True)
                    if suffix is not None:
                        self.take()
                else:
                    suffix = None
                if suffix is None:
                    self.pos = checkpoint
                    break
                self.interesting = True
                scripts.add(op)
                value += op + '{' + suffix + '}'
            elif op in ('†', 'ᵀ', '²', '³', '⁻¹', '!'):
                if op != '!' and '^' in scripts:
                    self.invalid = True
                    return None
                self.take()
                self.interesting = True
                if op != '!':
                    scripts.add('^')
                value += {'†': r'^{\dagger}', 'ᵀ': r'^{\mathsf{T}}',
                          '²': '^{2}', '³': '^{3}', '⁻¹': '^{-1}', '!': '!'}[op]
            elif op in ('(', '[') and next_token[1] == self.pos:
                args = self.group(depth + 1)
                if args is None:
                    self.pos = checkpoint
                    break
                self.interesting = True
                value += args
            else:
                break
        return value

    def group(self, depth, bare=False):
        checkpoint = self.pos
        previous_labels = self.allow_labels
        self.allow_labels = previous_labels or bare
        token = self.take()
        if token is None or token[0] not in ('(', '[', '{'):
            self.pos = checkpoint
            self.allow_labels = previous_labels
            return None
        left = token[0]
        self.allow_labels = self.allow_labels or left == '['
        right = {'(': ')', '[': ']', '{': '}'}[left]
        parts = []
        while True:
            term = self.expr(1, depth + 1)
            if term is None:
                self.pos = checkpoint
                self.allow_labels = previous_labels
                return None
            parts.append(term)
            token = self.take()
            if token is None:
                self.pos = checkpoint
                self.allow_labels = previous_labels
                return None
            if token[0] == right:
                break
            if token[0] != ',':
                self.pos = checkpoint
                self.allow_labels = previous_labels
                return None
        inside = ','.join(parts)
        self.allow_labels = previous_labels
        if bare:
            return inside
        return {'(': r'\left(', '[': r'\left[', '{': r'\left\{'}[left] + inside + {
            ')': r'\right)', ']': r'\right]', '}': r'\right\}'}[right]

    def expr(self, minimum=1, depth=0):
        if depth > 12:
            return None
        left = self.atom(depth + 1)
        if left is None:
            return None
        while (token := self.peek()) is not None:
            op = token[0]
            if op in _BINARY and _BINARY[op][0] >= minimum:
                checkpoint = self.pos
                precedence, tex = _BINARY[op]
                self.take()
                right = self.expr(precedence + 1, depth + 1)
                if right is None:
                    self.pos = checkpoint
                    break
                self.interesting = True
                left += tex + right
            # Immediate numeric-variable or scripted/grouped juxtaposition:
            # 2k+1, A†A and f(x)g(x). Never segment an English word into letters.
            elif (token[1] == self.pos and len(op) == 1 and op.isalpha()
                  and (left[-1:].isdigit() or left.endswith(('}', r'\right)', r'\right]')))):
                right = self.atom(depth + 1)
                if right is None:
                    break
                left += right
            else:
                break
        return left


def algebra_spans(value):
    """Return exact offsets of unambiguous legacy algebra; preserve the rest."""
    protected = [(m.start(), m.end()) for m in _PROTECTED.finditer(value)]
    spans, i = [], 0
    while i < len(value):
        blocked = next((end for start, end in protected if start <= i < end), None)
        if blocked is not None:
            i = blocked
            continue
        fixed = _GIVEN_BLOCK_COMPRESSION.match(value, i)
        if fixed and not any(start < fixed.end() and stop > i for start, stop in protected):
            tex = (('B=' if fixed['lhs'] else '')
                   + r'\left(\langle 0^{a}|\otimes I\right)U'
                   + r'\left(|0^{a}\rangle\otimes I\right)')
            spans.append(AlgebraSpan(i, fixed.end(), fixed.group(), tex))
            i = fixed.end()
            continue
        after_range = i >= 2 and value[i - 2:i] == '..'
        if ((i and (value[i - 1].isalnum() or value[i - 1] in '_^./:\\') and not after_range)
                or not (value[i].isalnum() or value[i] in '(-')):
            i += 1
            continue
        parser = _Algebra(value, i)
        tex = parser.expr()
        end = parser.pos
        # An unknown word, partial identifier or dangling script is not math.
        if (tex is not None and parser.interesting and not parser.invalid and end > i
                and not (end < len(value) and (value[end].isalnum() or value[end] in '_^'))
                and not any(start < end and stop > i for start, stop in protected)):
            spans.append(AlgebraSpan(i, end, value[i:end], tex))
            i = end
        else:
            word = re.match(r'[A-Za-z0-9]+', value[i:])
            i += len(word.group()) if word else 1
    return spans


def _valid_tex(tex):
    if len(tex) > 24_000 or _UNSAFE_TEX.search(tex) or '\x00' in tex:
        return False
    level = 0
    for match in re.finditer(r'(?<!\\)[{}]', tex):
        level += 1 if match.group() == '{' else -1
        if level < 0:
            return False
    return level == 0


def math_html(source, tex, *, display=False):
    """A TeX presentation retains the exact source and never accepts raw HTML."""
    if not _valid_tex(tex):
        return '<code class="qcb-math-literal" data-math-source>' + _esc(source) + '</code>'
    tag = 'div' if display else 'span'
    kind = 'qcb-equation' if display else 'qcb-math-token'
    left, right = (r'\[', r'\]') if display else (r'\(', r'\)')
    return ('<' + tag + ' class="' + kind + '" data-qcb-math-source="' + _esc(source)
            + '" data-qcb-math-sha256="' + text_hash(source) + '" data-qcb-math-tex="'
            + _esc(tex) + '">' + left + _esc(tex) + right + '</' + tag + '>')


def _plain(value):
    spans, parts, pos = algebra_spans(value), [], 0
    for span in spans:
        parts += [_esc(value[pos:span.start]), math_html(span.source, span.tex)]
        pos = span.end
    parts.append(_esc(value[pos:]))
    return ''.join(parts)


def _inline(value):
    parts, plain, i = [], [], 0

    def flush():
        if plain:
            parts.append(_plain(''.join(plain)))
            plain.clear()

    while i < len(value):
        if value[i] == '[':
            link = re.match(r'\[([^\]\n]+)\]\(([^\s()]+)\)', value[i:])
            if link:
                label, url = link.groups()
                parsed = urlsplit(url)
                if (parsed.scheme in {'https', 'http'} and parsed.netloc and '\\' not in url
                        or url.startswith('#') and re.fullmatch(r'#[\w-]+', url)):
                    flush()
                    parts.append('<a href="' + _esc(url) + '" rel="noopener noreferrer">'
                                 + _inline(label) + '</a>')
                    i += link.end()
                    continue
        if value[i] == '`':
            marker = re.match(r'`+', value[i:]).group()
            end = value.find(marker, i + len(marker))
            if end >= 0:
                flush()
                parts.append('<code data-math-source>' + _esc(value[i + len(marker):end]) + '</code>')
                i = end + len(marker)
                continue
        delimiters = [(r'\(', r'\)', False), (r'\[', r'\]', True), ('$$', '$$', True)]
        matched = False
        for left, right, display in delimiters:
            if not value.startswith(left, i):
                continue
            flush()
            end = value.find(right, i + len(left))
            if end < 0:
                parts.append('<code class="qcb-math-literal" data-math-source>' + _esc(value[i:]) + '</code>')
                i = len(value)
            else:
                source = value[i:end + len(right)]
                body = value[i + len(left):end]
                # Display math inside a paragraph is a styled span, not invalid div nesting.
                rendered = math_html(source, body, display=display)
                if display:
                    rendered = rendered.replace('<div ', '<span ', 1).replace('</div>', '</span>')
                parts.append(rendered)
                i = end + len(right)
            matched = True
            break
        if matched:
            continue
        if value.startswith(r'\$', i):
            flush()
            parts.append('<code class="qcb-literal-dollar" data-math-source>$</code>')
            i += 2
            continue
        if value[i] == '$':
            end = value.find('$', i + 1)
            body = value[i + 1:end] if end >= 0 else ''
            if (body and '\n' not in body and not body[0].isspace() and not body[-1].isspace()
                    and (end + 1 == len(value) or not value[end + 1].isalnum())):
                flush()
                parts.append(math_html(value[i:end + 1], body))
                i = end + 1
            else:
                flush()
                parts.append('<code class="qcb-literal-dollar" data-math-source>$</code>')
                i += 1
            continue
        for marker, tag in (('**', 'strong'), ('*', 'em')):
            # This reader accepts only word-delimited editorial emphasis.
            # Intraword stars are multiplication, and stars adjacent to braces
            # or punctuation may be mathematical operators/wildcard elements.
            # Markdown's broad delimiter rules are unsafe for this legacy
            # corpus: C={*}, A*B*C and A^* must retain every operator.
            if (value.startswith(marker, i) and i + len(marker) < len(value)
                    and value[i + len(marker)].isalpha()
                    and (i == 0 or value[i - 1].isspace() or value[i - 1] in '([{\"\'')):
                end = value.find(marker, i + len(marker))
                if (end > i + len(marker) and not value[end - 1].isspace()
                        and (end + len(marker) == len(value)
                             or not value[end + len(marker)].isalnum()
                             and value[end + len(marker)] not in '_*')):
                    flush()
                    parts.append('<' + tag + '>' + _inline(value[i + len(marker):end]) + '</' + tag + '>')
                    i = end + len(marker)
                    matched = True
                    break
        if not matched:
            plain.append(value[i])
            i += 1
    flush()
    return ''.join(parts)


def render_prose(value):
    """Render limited Markdown and exact mathematical notation, with HTML off."""
    value = str(value)
    lines, blocks, i = value.splitlines(), [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        fence = re.fullmatch(r'\s*(`{3,}|~{3,})\s*([\w+-]*)\s*', line)
        if fence:
            marker, language = fence.groups()
            content = []
            i += 1
            while i < len(lines) and lines[i].strip() != marker:
                content.append(lines[i])
                i += 1
            i += int(i < len(lines))
            blocks.append('<pre class="qcb-code"><code data-math-source class="language-' + _esc(language) + '">' + _esc('\n'.join(content)) + '</code></pre>')
            continue
        display = next(((a, b) for a, b in ((r'\[', r'\]'), ('$$', '$$')) if line.strip().startswith(a)), None)
        if display:
            left, right = display
            gathered = [line.strip()[len(left):]]
            i += 1
            while right not in gathered[-1] and i < len(lines):
                gathered.append(lines[i])
                i += 1
            joined = '\n'.join(gathered)
            end = joined.find(right)
            if end >= 0 and not joined[end + len(right):].strip():
                blocks.append(math_html(left + joined[:end] + right, joined[:end], display=True))
            else:
                blocks.append('<pre class="qcb-math-literal"><code data-math-source>' + _esc(left + joined) + '</code></pre>')
            continue
        heading = re.fullmatch(r'(#{1,4})\s+(.+)', line)
        if heading:
            level = min(6, len(heading[1]) + 2)
            blocks.append('<h' + str(level) + '>' + _inline(heading[2]) + '</h' + str(level) + '>')
            i += 1
            continue
        bullet = re.match(r'^\s*(?:[-*]|\d+[.)])\s+(.+)$', line)
        if bullet:
            ordered = bool(re.match(r'^\s*\d', line))
            tag, items = ('ol' if ordered else 'ul'), []
            while i < len(lines):
                match = re.match(r'^\s*(\d+[.)])\s+(.+)$' if ordered else r'^\s*([-*])\s+(.+)$', lines[i])
                if match is None:
                    break
                items.append('<li data-qcb-list-marker="' + _esc(match[1]) + '">' + _inline(match[2]) + '</li>')
                i += 1
            blocks.append('<' + tag + '>' + ''.join(items) + '</' + tag + '>')
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip():
            if re.match(r'^\s*(?:```|~~~|#{1,4}\s|[-*]\s|\d+[.)]\s|\$\$|\\\[)', lines[i]):
                break
            paragraph.append(lines[i])
            i += 1
        blocks.append('<p>' + _inline('\n'.join(paragraph)) + '</p>')
    return '<div class="qcb-prose qcb-math-prose" data-qcb-text-sha256="' + text_hash(value) + '">' + '\n'.join(blocks) + '</div>'


def question_equations(record_id, question):
    """Render an explicitly authored notation view of one exact question.

    This is editorial presentation, not a new proof or an answer. In particular
    a false diagnostic proposition remains displayed as the claim to assess.
    """
    annotation = _QUESTION_COMPANIONS.get(record_id)
    if annotation is None:
        return ''
    if text_hash(question) != annotation['source_sha256']:
        raise ValueError('Question notation is stale; review the changed mathematical source.')
    return ('<section class="qcb-equation-guide" data-qcb-notation-for="' + _esc(record_id)
            + '" data-qcb-notation-source="' + annotation['source_sha256'] + '">'
            + '<h4>Mathematical notation</h4><p>' + _esc(annotation['legend']) + '</p>'
            + math_html(question, annotation['tex'], display=True) + '</section>')


def notation_source_bindings():
    return {key: value['source_sha256'] for key, value in _QUESTION_COMPANIONS.items()}


# Explicit editorial notation companions; exact source binding is mandatory.
_QUESTION_COMPANIONS = {'qcb-core-sp-005': {'source_sha256': '94fd6a74390704a7fd29461bf7d810e001fc629b5f06801e7c053e215426f63f',
                     'tex': '\\begin{gathered}m(b)=\\sqrt{f(b0)^2+f(b1)^2},\\\\\\sum_b '
                            'm(b)^2=\\sum_w f(w)^2\\end{gathered}',
                     'legend': 'Here b0 and b1 mean appending the last bit to the prefix b.'},
 'qcb-core-sp-009': {'source_sha256': '78ebafeabb50155e0ecd8755a16b90ea5420c7d724d5518bb5f64e194cc5de0f',
                     'tex': '\\begin{gathered}AA^{\\mathsf '
                            'T}=I_l,\\\\U_{(b,j),a}=A_{a,(b,j)}\\in\\mathbb '
                            'C,\\\\U^{\\dagger}U=I_l\\end{gathered}',
                     'legend': 'The real entry of A is embedded into the complex field in U. The '
                               'output row is (bit,new bond).'},
 'qcb-core-be-111': {'source_sha256': '4fe075669e24fdec2b3f964b17c04a0a2cddcdca2ff44c8f0300e58d58765108',
                     'tex': '\\begin{gathered}P(e)_{r,c}=\\mathbf 1_{\\{r=e(c)\\}},\\\\P(s\\circ '
                            'f)=P(s)P(f)\\end{gathered}',
                     'legend': 'The map f acts first, followed by s; the matrices act on column '
                               'vectors.'},
 'qcb-core-sp-104': {'source_sha256': '9df15b576a82eb5455544479ab5a763585c295e405407d58cce47e59bd640639',
                     'tex': '\\begin{gathered}k\\in\\mathbb N,\\quad p,q\\in\\mathbb '
                            'R[X],\\\\\\deg p,\\deg q\\le '
                            '2k+1,\\\\p^{(j)}(-1)=q^{(j)}(-1),\\\\p^{(j)}(0)=q^{(j)}(0)\\quad(0\\le '
                            'j\\le k),\\\\\\text{claim: }p=q.\\end{gathered}',
                     'legend': 'The derivative order j is an integer. Order zero is the polynomial '
                               'itself.'},
 '2b3f25f2-db0a-4494-a887-14d7111eaf6a': {'source_sha256': 'c3cb5109d3a64ca8198feb77ef869f59fe0aa10bb2534a30835f7ec09caf76c5',
                                          'tex': '\\begin{gathered}AA^{\\mathsf '
                                                 'T}=I_l,\\\\M(v)=\\sum_{a\\in\\mathrm{Fin}(l)}v_a^2,\\\\\\text{claim: '
                                                 '}M(vA)=M(v)\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'b0c5d76c-2aa7-4818-8009-c451c9c1081a': {'source_sha256': '1f0f4d47e412e605d26eeaa5df468cc2ffb51ab994d94a40d24035858354e300',
                                          'tex': '\\begin{gathered}AA^{\\mathsf T}=I_l,\\quad '
                                                 'M(w)=\\sum_iw_i^2,\\\\\\text{claim: }M(vA)=1\\ '
                                                 '\\text{for every }v\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '87a548fd-6c07-4b71-a224-c374ec1005f5': {'source_sha256': 'f35654aee42f79c57cbc75bacf5f5c2ff05cde0a22aa40117d36835ccb9909b8',
                                          'tex': '\\begin{gathered}AA^{\\mathsf '
                                                 'T}=I_l,\\\\V_{(j,b),a}=A_{a,(b,j)}\\in\\mathbb '
                                                 'C,\\\\\\text{claim: }V^\\dagger '
                                                 'V=I_l\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'c947872c-f1ae-4f09-9ff9-0d535c93b11c': {'source_sha256': '959aeeb52ce5f870cba7b2789f9b033bcda42945d84c760201501c7d00e8ee2b',
                                          'tex': '\\begin{gathered}AA^{\\mathsf '
                                                 'T}=[1],\\\\U_{(b,j),0}=A_{0,(b,j)},\\\\V_{(j,b),0}=A_{0,(b,j)},\\\\\\text{claim: '
                                                 '}V=U\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'd883d091-46d3-4f97-9dd7-b560d53238f0': {'source_sha256': 'd14022ffa7c4476ab327e22df77249273dfa6242fb388d01929ff1277e3aaf5c',
                                          'tex': '\\begin{gathered}AA^{\\mathsf '
                                                 'T}=I_l,\\\\U_{\\mathrm{out},a}=A_{a,\\mathrm{out}}\\in\\mathbb '
                                                 'C,\\\\\\text{claim: '
                                                 '}UU^\\dagger=I_{\\mathrm{Fin}(2)\\times\\mathrm{Fin}(r)}\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '5a644ea9-ef08-4026-8c7b-90a9e6dc2481': {'source_sha256': 'a121a2d935145fd84dd4d9d29d17900ee684e0660ad08da859894abbebd271d0',
                                          'tex': '\\begin{gathered}AA^{\\mathsf '
                                                 'T}=I_l,\\\\U_{\\mathrm{out},a}=A_{a,\\mathrm{out}}\\in\\mathbb '
                                                 'C,\\\\Q=UU^\\dagger,\\quad\\text{claim: '
                                                 '}Q^2=Q\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'ce8fd401-a4af-4c95-bef4-cbc5b42c7314': {'source_sha256': '3d53bf37e47084ab614de9365e1fc41b231efc8dc2e6a7e058d20fa8863c13f8',
                                          'tex': '\\begin{gathered}m(f)(b)=\\sqrt{f(b,0)^2+f(b,1)^2},\\\\N(g)=\\sum_w '
                                                 'g(w)^2,\\\\\\text{claim: '
                                                 '}N(m(f))=N(f)\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '94f36e25-6def-4b77-8bf8-7056c2425df5': {'source_sha256': 'fa0dea808b35a402c09ffc92c95231ff5c2a03b6357fa28bb329b37c63d76e2b',
                                          'tex': '\\begin{gathered}m(f)=\\sqrt{f(0)^2+f(1)^2},\\\\\\text{claim: '
                                                 '}m(f+g)=m(f)+m(g)\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'b1234a5b-fe27-4add-bbe4-cb130e138af6': {'source_sha256': 'f92ed12d84a80ae6f256e44b7fbeeaa4b0c5bf78f77c2333c2edf6cb5aaf7e62',
                                          'tex': '\\begin{gathered}k=(x,(c,s)),\\\\U_p\\,{}^{\\prime}(r,k)=U_p(J^{-1}(r),J^{-1}(k)),\\\\\\text{claim: '
                                                 '}U_p\\,{}^{\\prime}(r,k)=\\begin{cases}1&r=(p_s(x),(c,s)),\\\\0&\\text{otherwise}.\\end{cases}\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '93904687-6d03-43fe-b130-193a4f90ab4e': {'source_sha256': '5f6021f4ad33ee82fd4d74f65b45afb2d214b4b77d48a94b4ec8be871a7d4f0c',
                                          'tex': '\\begin{gathered}k=(x,(c,s)),\\quad '
                                                 'C=S=X=\\{\\mathrm{false},\\mathrm{true}\\},\\\\\\text{claim: '
                                                 '}U_p\\,{}^{\\prime}(r,k)=\\begin{cases}1&r=(p_c(x),(c,s)),\\\\0&\\text{otherwise}.\\end{cases}\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'badaa09e-22b6-482f-b277-b0ab8c1f28e7': {'source_sha256': '9d63a6c4be3b38784e6bf2d945a9e3027e56170f3713f369b500f7c34eae40a2',
                                          'tex': '\\begin{gathered}q_s=p_s^{-1},\\\\\\text{claim: '
                                                 '}U_qU_p=I_A\\\\\\text{and}\\quad '
                                                 'U_pU_q=I_A\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '9653f2d7-5af9-420b-a8af-30ad44c0f651': {'source_sha256': 'ad537ca8bbaf15535a1c73210a0dabe0ab4f31051167c0ecb85b2858f81f7644',
                                          'tex': '\\begin{gathered}q_s=(p_{\\neg '
                                                 's})^{-1},\\\\\\text{claim: '
                                                 '}U_qU_p=I_A\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '976c9922-4202-4a48-a885-4d5a6d21656f': {'source_sha256': '85934e768f66cfc0fa9f02b479868b5087b540c87f14b6d80969f970d4ce2e19',
                                          'tex': '\\begin{gathered}r_s=q_s\\circ '
                                                 'p_s,\\\\\\text{claim: }U_pU_q=U_r\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 'd67d7a90-a228-4d10-b10a-2e2957f00cd2': {'source_sha256': 'cfe37f4c9ac6d06b93d2b9924a89603a7671d8e93a0b593f2999601e81286c69',
                                          'tex': '\\begin{gathered}r_s=q_s\\circ '
                                                 'p_s,\\\\\\text{claim: }U_qU_p=U_r\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '8a8bdc71-dcd2-42e9-a564-19b2d0530fdf': {'source_sha256': '943bb3f023b5273634b64686ad487994956adad5be926bff01ebb47dd7debca2',
                                          'tex': '\\begin{gathered}p,q\\in\\mathbb R[X],\\quad '
                                                 '\\deg p,\\deg q\\le '
                                                 '2k+1,\\\\p^{(j)}(-1)=q^{(j)}(-1),\\\\p^{(j)}(0)=q^{(j)}(0)\\ '
                                                 '(0\\le j\\le k),\\\\\\text{claim: '
                                                 '}p=q\\quad\\text{for all }k\\in\\mathbb '
                                                 'N.\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'},
 '645ccfc8-9c4b-4e41-b51b-b330748fc34e': {'source_sha256': '07590fcdd1e34bcb49c5847773b83a4e539ce86d4041dc9f759387cc3b38e673',
                                          'tex': '\\begin{gathered}p,q\\in\\mathbb R[X],\\quad '
                                                 '\\deg p,\\deg q\\le '
                                                 '2k+2,\\\\p^{(j)}(-1)=q^{(j)}(-1),\\\\p^{(j)}(0)=q^{(j)}(0)\\ '
                                                 '(0\\le j\\le k),\\\\\\text{claim: '
                                                 '}p=q\\quad\\text{for all }k\\in\\mathbb '
                                                 'N.\\end{gathered}',
                                          'legend': 'The displayed claim is the proposition to '
                                                    'assess. All assumptions and conventions in '
                                                    'the question still apply.'}}
