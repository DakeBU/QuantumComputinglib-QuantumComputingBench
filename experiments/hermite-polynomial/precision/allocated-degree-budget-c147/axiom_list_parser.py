"""Parse Lean's printed axiom-name list without accepting unknown names."""
import re

def parse_axiom_list(text):
    if not text.strip():return []
    pattern=re.compile(r'\s*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)(?:\.\{[A-Za-z0-9_, .+()]+\})?\s*(,|$)')
    names=[];pos=0
    while pos<len(text):
        match=pattern.match(text,pos)
        if not match:raise ValueError('Malformed printed axiom list')
        names.append(match[1]);pos=match.end()
        if not match[2]:
            if pos!=len(text):raise ValueError('Unparsed axiom suffix')
            break
        if not text[pos:].strip():raise ValueError('Trailing axiom separator')
    return names

def ordinary_only(names):
    return set(names)<={'propext','Classical.choice','Quot.sound'}
