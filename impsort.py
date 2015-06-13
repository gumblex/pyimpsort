#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tokenize
from io import BytesIO

PY2 = (sys.version_info[0] == 2)
gentok = tokenize.generate_tokens if PY2 else tokenize.tokenize


def taketokline(iterable):
    for x in iterable:
        yield x
        if x[0] in (tokenize.NEWLINE, tokenize.NL, tokenize.DEDENT):
            break


def impsortkey(token):
    sumlen = 0 if token[0][1] == 'import' else 10000
    for n in token:
        if n[0] != tokenize.COMMENT:
            sumlen += 1 + len(n[1])
    return sumlen


def correctimpsort(imps):
    lo = imps[0][0][2][0]
    imps.sort(key=impsortkey)
    for k, line in enumerate(imps, lo):
        for i in range(len(line)):
            ol = line[i]
            line[i] = (ol[0], ol[1], (k, ol[2][1]), (k, ol[3][1]), ol[4])


def dosort(iterable):
    imps = []
    tokline = list(taketokline(iterable))
    while tokline:
        if tokline[-1][0] == tokenize.NL:
            if imps:
                correctimpsort(imps)
                for l in imps:
                    for tok in l:
                        yield tok
                imps = []
            for tok in tokline:
                yield tok
        elif tokline[0][1] in ('import', 'from'):
            imps.append(tokline)
        else:
            if imps:
                correctimpsort(imps)
                for l in imps:
                    for tok in l:
                        yield tok
                imps = []
            for tok in tokline:
                yield tok
        tokline = list(taketokline(iterable))


def impsortrl(readline):
    return tokenize.untokenize(dosort(gentok(readline)))


def impsort(s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    return tokenize.untokenize(dosort(gentok(BytesIO(s).readline)))


if __name__ == '__main__':
    stdin = sys.stdin if PY2 else sys.stdin.buffer
    stdout = sys.stdout if PY2 else sys.stdout.buffer
    if len(sys.argv) > 1:
        stdout.write(impsortrl(open(sys.argv[1], 'rb').readline))
    else:
        stdout.write(impsortrl(stdin.readline))

