"""Exact three-token proof successor. Comments are masked before formal inspection."""
import hashlib
import re

RELATIVE='QuantumBlockEncoding/CubicAmplitudePrimitive.lean'
ORIGINAL_SHA='48c9a4a1c47c925c93493eede21eb7b492d23d2cb7dadf254782e4485c349cb3'
NAMES=('cubicN2Amplitude_abs_le_one','cubicN2ControlIndex_encode','cubicN2EncodeBits_context_eq_iff')
OLD=b'native_decide'
NEW=b'decide +kernel'


def sha(data): return hashlib.sha256(data).hexdigest()


def mask(text):
    out=[]; i=0; depth=0; quoted=False; esc=False; line=False
    while i<len(text):
        c=text[i]; n=text[i:i+2]
        if line:
            if c=='\n': line=False; out.append(c)
            else: out.append(' ')
        elif depth:
            if n=='/-': depth+=1; out.extend('  '); i+=1
            elif n=='-/': depth-=1; out.extend('  '); i+=1
            else: out.append(c if c in '\r\n' else ' ')
        elif quoted:
            out.append(c)
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': quoted=False
        elif c=="'" and (ch:=re.match(r"'(?:\\.|[^'\\])'",text[i:])):
            out.extend(ch[0]); i+=len(ch[0])-1
        elif c=='"': quoted=True; out.append(c)
        elif n=='/-': depth=1; out.extend('  '); i+=1
        elif n=='--': line=True; out.extend('  '); i+=1
        else: out.append(c)
        i+=1
    if depth or quoted: raise ValueError('unterminated lexical boundary')
    return ''.join(out)


def candidate(raw):
    if sha(raw)!=ORIGINAL_SHA: raise ValueError('original source SHA drift')
    text=raw.decode('utf-8'); masked=mask(text)
    matches=list(re.finditer(r'\bnative_decide\b',masked))
    if len(matches)!=3: raise ValueError('not exactly three native proof tokens')
    sites=[]
    for expected,match in zip(NAMES,matches):
        starts=list(re.finditer(r'\b(?:theorem|lemma)\s+([A-Za-z0-9_]+)',masked[:match.start()]))
        if not starts or starts[-1][1]!=expected or not re.match(r'\s+\+revert\b',masked[match.end():]):
            raise ValueError('proof site/boundary drift')
        start=len(text[:match.start()].encode('utf-8')); end=start+len(OLD)
        if raw[start:end]!=OLD: raise ValueError('raw byte coordinate drift')
        sites.append(dict(sourceName='QuantumBlockEncoding.CubicDiagonalOracle.'+expected,
            originalLine=text[:match.start()].count('\n')+1,oldByteStart=start,oldByteEnd=end,
            oldToken=OLD.decode(),newToken=NEW.decode(),
            statementAndBindersUnchanged=True,remainingProofSuffix='+revert'))
    result=raw
    for site in reversed(sites): result=result[:site['oldByteStart']]+NEW+result[site['oldByteEnd']:]
    restore=result
    for i,site in reversed(list(enumerate(sites))):
        pos=site['oldByteStart']+i*(len(NEW)-len(OLD))
        if restore[pos:pos+len(NEW)]!=NEW: raise ValueError('candidate inverse boundary drift')
        restore=restore[:pos]+OLD+restore[pos+len(NEW):]
    if restore!=raw: raise ValueError('non-proof bytes changed')
    return result,sites


def derive_profile(original,new_sha):
    import copy
    result=copy.deepcopy(original)
    modules=[m for m in result['modules'] if m['module']=='QuantumBlockEncoding.CubicAmplitudePrimitive']
    if len(modules)!=1 or modules[0]['rawSHA256']!=ORIGINAL_SHA or result['projectInputs'][RELATIVE]!=ORIGINAL_SHA:
        raise ValueError('original profile binding drift')
    modules[0]['rawSHA256']=new_sha; result['projectInputs'][RELATIVE]=new_sha
    return result


def validate_derivation(original,derived,new_sha):
    if derived!=derive_profile(original,new_sha): raise ValueError('profile changes outside exact target SHA derivation')
    return True
