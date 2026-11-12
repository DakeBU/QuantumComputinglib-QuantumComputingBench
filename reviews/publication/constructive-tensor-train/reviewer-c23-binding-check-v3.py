"""Independently recompute exact versioned graph successor binding."""
from pathlib import Path
old = Path('reviews/publication/constructive-tensor-train/reviewer-c23-binding-check.py').read_text(encoding='utf-8')
corrected = old.replace("source = read('author-source-row-candidate.json')", "source = read('author-source-row-candidate.json')['source']")
corrected = corrected.replace('publication-candidate.json','publication-candidate-v2.json')
corrected = corrected.replace('121c0c8603b75ccde304783e94fa61abd82159768b0007da675da201f7501c24','9be3c975b10363ad36778d6dc9da4c7a941857f6571f3e2f6072c73d65a51c09')
corrected = corrected.replace("'author-graph-views.json'","'parent-graph-views-v2.json'").replace("'author-source-coverage.json'","'parent-source-coverage-v2.json'")
corrected = corrected.replace('reviewer-c23-binding-receipt.json','reviewer-c23-binding-receipt-v2.json')
exec(compile(corrected, 'reviewer-c23-binding-check-v3.py', 'exec'))
