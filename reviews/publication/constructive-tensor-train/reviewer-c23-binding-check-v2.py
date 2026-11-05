"""Versioned retry; preserves v1 program and its schema-access failure."""
from pathlib import Path
old = Path('reviews/publication/constructive-tensor-train/reviewer-c23-binding-check.py').read_text(encoding='utf-8')
corrected = old.replace("source = read('author-source-row-candidate.json')", "source = read('author-source-row-candidate.json')['source']")
exec(compile(corrected, 'reviewer-c23-binding-check-v2.py', 'exec'))
