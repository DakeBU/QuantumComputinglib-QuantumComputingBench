"""Mathematical presentation regressions; these are not new Lean proofs."""
import hashlib
import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'benchmarks/quantumcomputingbench/src'))
from website.scripts import qcb_math as math


class Parsed(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.math = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.tags.append((tag, data))
        if 'data-qcb-math-source' in data:
            self.math.append(data)


class MathPresentationTests(unittest.TestCase):
    def test_actual_legacy_algebra_keeps_orientation_and_precedence(self):
        cases = {
            'A * A^T = 1': r'A\cdot A^{T}=1',
            'x^(k+1)': r'x^{k+1}',
            'x^{k+1}': r'x^{k+1}',
            'N*M*(22*M+30*N+29)': r'N\cdot M\cdot \left(22\cdot M+30\cdot N+29\right)',
            'v(j)/j!': r'v\left(j\right)/j!',
            'A†A=I': r'A^{\dagger}A=I',
            'A⊗B=C': r'A\otimes B=C',
            'a/(b+c)': r'a/\left(b+c\right)',
            'a-b-c': 'a-b-c',
            'a^(-1)': 'a^{-1}',
            'x²+y²=1': 'x^{2}+y^{2}=1',
            '(x-a)^i': r'\left(x-a\right)^{i}',
            '(A^T)^T': r'\left(A^{T}\right)^{T}',
            '-x^2': '-x^{2}',
            '(-x)^2': r'\left(-x\right)^{2}',
            'cos^2(t/2)+sin^2(t/2)=1': r'\operatorname{cos}^{2}\left(t/2\right)+\operatorname{sin}^{2}\left(t/2\right)=1',
            'B[row,c]^2': r'B\left[\mathrm{row},c\right]^{2}',
        }
        for source, tex in cases.items():
            with self.subTest(source=source):
                spans = math.algebra_spans(source)
                self.assertEqual([(s.source, s.tex) for s in spans], [(source, tex)])

    def test_english_paths_dates_and_model_names_are_not_algebra(self):
        for text in ('A difficult task', 'a well-defined function', 'one-to-one',
                     'post-training', '1-based indexing', 'Qwen3-14B model',
                     '2026-11-04', 'https://example.org/a^2', 'www.example.org/x^2',
                     '/tmp/foo.py', r'C:\work\proof.lean', 'proof.json', 'AA',
                     'teacher outputs and student inputs', 'phase-aware compilation'):
            with self.subTest(text=text):
                self.assertEqual(math.algebra_spans(text), [])

    def test_given_block_compression_has_bra_ket_typography_without_added_claims(self):
        from website.scripts.qcb_render_test_support import recover_prose_source
        body = r'\left(\langle 0^{a}|\otimes I\right)U\left(|0^{a}\rangle\otimes I\right)'
        cases = {
            'B=(<0^a| tensor I)U(|0^a> tensor I)': 'B=' + body,
            '(<0^a| tensor I) U (|0^a> tensor I)': body,
            'B = ( < 0 ^ a | tensor I ) U ( | 0 ^ a > tensor I )': 'B=' + body,
        }
        for source, tex in cases.items():
            with self.subTest(source=source):
                spans = math.algebra_spans(source)
                self.assertEqual([(s.source, s.tex) for s in spans], [(source, tex)])
                rendered = math.render_prose(source)
                self.assertEqual(recover_prose_source(rendered, source), source)
                self.assertEqual(Parsed(rendered).math[0]['data-qcb-math-tex'], tex)
        for source in ('(<0^b| tensor I)U(|0^b> tensor I)',
                       '(<0^a| tensor J)U(|0^a> tensor I)',
                       '(<0^a| tensor I)V(|0^a> tensor I)'):
            self.assertFalse(any(r'\langle' in s.tex for s in math.algebra_spans(source)))
        self.assertNotIn('alpha', body)
        self.assertNotIn('epsilon', body)

    def test_prose_labels_and_rank_properties_are_not_subtraction(self):
        for source in ('b-with-last-bit-0', 'b-with-last-bit-1', 'rank-1', 'bit-0',
                       'old-bond', 'new-bond', 'out-of-domain', 'The rank-1 table'):
            with self.subTest(source=source):
                self.assertEqual(math.algebra_spans(source), [])
        self.assertEqual([s.source for s in math.algebra_spans('rank(A)-1')], ['rank(A)-1'])
        self.assertEqual([s.source for s in math.algebra_spans('A_{out,a}')], ['A_{out,a}'])
        self.assertEqual([s.source for s in math.algebra_spans('0..2^n-1')], ['2^n-1'])

    def test_source_offsets_and_metadata_retain_every_original_character(self):
        text = 'Assume A * A^T = 1. Compare x^(k+1) and a/(b+c).'
        spans = math.algebra_spans(text)
        rendered = Parsed(math.render_prose(text)).math
        self.assertEqual(len(spans), len(rendered))
        for span, attrs in zip(spans, rendered):
            self.assertEqual(text[span.start:span.end], span.source)
            self.assertEqual(attrs['data-qcb-math-source'], span.source)
            self.assertEqual(attrs['data-qcb-math-tex'], span.tex)
            self.assertEqual(attrs['data-qcb-math-sha256'], math.text_hash(span.source))

    def test_currency_does_not_join_across_amounts(self):
        rendered = math.render_prose('The costs are $5 and $7; a formula is $x^2$.')
        parsed = Parsed(rendered)
        self.assertEqual([m['data-qcb-math-tex'] for m in parsed.math], ['x^2'])
        self.assertEqual(rendered.count('qcb-literal-dollar'), 2)
        self.assertEqual(Parsed(math.render_prose(r'Price \$5.')).math, [])

    def test_explicit_inline_display_and_multiline_math(self):
        text = r'Inline \(\frac{x}{y}\) and $x^2$.' + '\n\n' + '$$\n' + r'\begin{pmatrix}1&0\\0&1\end{pmatrix}' + '\n$$'
        parsed = Parsed(math.render_prose(text))
        self.assertEqual(len(parsed.math), 3)
        self.assertEqual(parsed.math[2]['data-qcb-math-tex'].strip(), r'\begin{pmatrix}1&0\\0&1\end{pmatrix}')
        self.assertTrue(any(tag == 'div' and a.get('class') == 'qcb-equation' for tag, a in parsed.tags))

    def test_lean_fences_and_inline_code_are_not_typeset(self):
        rendered = math.render_prose('```lean\nexact h -- x^2 and \\(y\\)\n```\n\nUse `x^(k+1)` literally.')
        parsed = Parsed(rendered)
        self.assertEqual(parsed.math, [])
        self.assertTrue(any(tag == 'code' and 'data-math-source' in a for tag, a in parsed.tags))
        self.assertIn('exact h', rendered)

    def test_unclosed_fence_and_delimiter_remain_readable_code(self):
        for text in ('```lean\nby\n exact h', r'Unclosed \(x^2', '$$\nx^2'):
            with self.subTest(text=text):
                parsed = Parsed(math.render_prose(text))
                self.assertEqual(parsed.math, [])
                self.assertTrue(any(tag == 'code' for tag, _ in parsed.tags))

    def test_unsafe_tex_and_html_cannot_create_live_markup_or_links(self):
        inputs = ('<script>alert(1)</script>', '<img src=x onerror=alert(1)>',
                  r'\(\href{javascript:alert(1)}{x}\)', r'\(\style{background:url(x)}{x}\)',
                  r'\(\require{html}\)', r'\(\newcommand{\x}{x}\x\)',
                  '[bad](javascript:alert(1))', '[bad](data:text/html,boom)')
        for text in inputs:
            with self.subTest(text=text):
                parsed = Parsed(math.render_prose(text))
                self.assertFalse(any(tag in {'script', 'img', 'style', 'iframe'} for tag, _ in parsed.tags))
                self.assertFalse(any(tag == 'a' for tag, _ in parsed.tags))
                self.assertFalse(any('onerror' in attrs for _, attrs in parsed.tags))
                if text.startswith(r'\('):
                    self.assertEqual(parsed.math, [])

    def test_limited_markdown_preserves_math_inside_emphasis_and_lists(self):
        parsed = Parsed(math.render_prose('## Reasoning\n\n**Use x^(k+1)**.\n\n- First A†A=I\n- Next x^2\n\n1. Explain\n2. Prove\n\n[Paper](https://example.org/paper)'))
        tags = [tag for tag, _ in parsed.tags]
        for tag in ('h4', 'strong', 'ul', 'ol', 'a'):
            self.assertIn(tag, tags)
        self.assertEqual(len(parsed.math), 3)

    def test_multiplication_adjoint_and_wildcard_stars_are_never_emphasis(self):
        from website.scripts.qcb_render_test_support import recover_prose_source
        cases = (
            'A*B*C and N*M*(22*M+30*N+29).',
            'C={*}, S={false,true}, X={0,1,2}; set p_true=X and q_true=X.',
            'The mixtures (a*row_i + b*row_j) and (c*row_i + d*row_j) have factor (a*d - b*c).',
            'Write f(x)*g(x) and A^*A, then use 2*q+b.',
            'Let (G, .) and (H, *) be groups; x*y*z is their product.',
        )
        for source in cases:
            with self.subTest(source=source):
                rendered = math.render_prose(source)
                self.assertEqual(recover_prose_source(rendered, source), source)
                self.assertFalse(any(tag in {'em', 'strong'} for tag, _ in Parsed(rendered).tags))
        # Conventional editorial emphasis remains supported at word boundaries.
        tags = [tag for tag, _ in Parsed(math.render_prose('*Reason carefully*; **Use x^2**.')).tags]
        self.assertIn('em', tags)
        self.assertIn('strong', tags)

    def test_unbalanced_braces_and_deep_grammar_fail_readably(self):
        parsed = Parsed(math.render_prose(r'\(x^{2\)'))
        self.assertEqual(parsed.math, [])
        self.assertIn('qcb-math-literal', math.render_prose(r'\(x^{2\)'))
        text = '(' * 200 + 'x^2' + ')' * 200
        self.assertLessEqual(len(math.algebra_spans(text)), 1)

    def test_ambiguous_repeated_scripts_never_emit_invalid_or_reinterpreted_tex(self):
        for source in ('x^2^3', 'x²^3', 'p_i^lambda_i', 'x_i_j', 'A^T†'):
            with self.subTest(source=source):
                self.assertEqual(math.algebra_spans(source), [])

    def test_annotations_bind_actual_questions_and_do_not_reveal_polarity(self):
        from qcb_curriculum import load_catalog
        _, items, _ = load_catalog()
        packet = json.loads((ROOT / 'benchmarks/quantumcomputingbench/tracks/lean/learning-validity/v1/cohort.json').read_text())
        questions = {key: value['question'] for key, value in items.items()}
        questions.update({p['probe_id']: p['question'] for p in packet['probes']})
        for record, expected in math.notation_source_bindings().items():
            question = questions[record]
            self.assertEqual(math.text_hash(question), expected)
            rendered = math.question_equations(record, question)
            parsed = Parsed(rendered)
            self.assertEqual(len(parsed.math), 1)
            self.assertEqual(parsed.math[0]['data-qcb-math-source'], question)
            self.assertNotIn('Reference decision', rendered)
            with self.assertRaisesRegex(ValueError, 'stale'):
                math.question_equations(record, question + ' altered')
        self.assertEqual(math.question_equations('unregistered', 'ordinary question'), '')

    def test_real_corpus_gets_broad_source_preserving_math_coverage(self):
        from qcb_curriculum import load_catalog
        _, items, _ = load_catalog()
        covered, count = 0, 0
        for item in items.values():
            spans = []
            for field in ('question', 'reference_answer'):
                value = item[field]
                current = math.algebra_spans(value)
                for span in current:
                    self.assertEqual(value[span.start:span.end], span.source)
                    self.assertTrue(math._valid_tex(span.tex))
                spans += current
            covered += bool(spans)
            count += len(spans)
        self.assertGreater(covered / len(items), .9)
        self.assertGreater(count, 4000)

    def test_whole_prose_binding_is_the_exact_utf8_source(self):
        source = 'A†A=I\n\nLiteral condition: x^2.'
        parsed = Parsed(math.render_prose(source))
        self.assertEqual(parsed.tags[0][1]['data-qcb-text-sha256'], hashlib.sha256(source.encode()).hexdigest())


if __name__ == '__main__':
    unittest.main()
