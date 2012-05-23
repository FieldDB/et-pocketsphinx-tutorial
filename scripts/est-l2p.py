#!/usr/bin/python
# -*- coding: latin-1 -*-

'''
Created on Feb 18, 2011

@author: tanel
'''

import sys
import re
import locale
import codecs

# Default settings based on the user's environment.
#locale.setlocale(locale.LC_ALL, '') 

l2p_rules = r"""

s~  S
z~  S

q   k

tt   T
kk   K
pp   P

ph    f

x   ks
sch S
^ch([aeiou])    tS\1
cz    tS
([aeiou])ch    \1hh
([aeiou])ck    \1K
^c(?=[i])   s
c   k
y   i
z   s
w   v



([aeiou]|^)sh(?=($|[aeiou]))    \1S

([aeiou����mnlrv])k(?=($|([[lrmnvjaeiou����]))) \1K
([aeiou����mnlrv])p(?=($|([[lrmnvjaeiou����]))) \1P
([aeiou����mnlrv])t(?=($|([[lrmnvjaeiou����]))) \1T

d   t
g   k
b   p


([^aeiou����])i([aeou����]) \1j\2

([aeiou����])i([aeou����]) \1ij\2

[\+-\?=~]    

"""

word_variants = u"""

k�mmend kend
tegelikult  tegelt
siis    sis
ja     jaa
seal    sel
need    ned
vel     vel
praegu  pr��gu
vaata   vata
kuidagi kudagi
m�ttes  m�ts
lihtsalt lissalt
lihtsalt lissat
kindlasti   kinlasti
kaheksa kaeksa
�heksa    �eksa
�heksa    �eksa

selle(.*)   sele\1
(.*[aeiou����])nud$ \1nd


"""

phon2phon = u"""
S    sh
�    ou
�    ae
�    oe
�    ue
K    kk
P    pp
T    tt
"""

phones = u"a ae e f h i j k kk l m n o oe ou p pp r s sh t tt u ue v".split()

def is_phone(phone):
    return phone in phones


if __name__ == '__main__':
    rules = []
    for l in l2p_rules.splitlines():
        ss = l.split()
        if len(ss) > 0:
            if len(ss) == 1:
                rules.append((ss[0], ""))
            else:
                rules.append((ss[0], ss[1]))
    variant_rules = []
    for l in word_variants.splitlines():
        ss = l.split()
        if len(ss) > 1:
            variant_rules.append((ss[0], ss[1]))
    phon2phon_map = {}
    for l in phon2phon.splitlines():
        ss = l.split()
        if len(ss) > 1:
            phon2phon_map[ss[0]] = ss[1]
    
    encoding = locale.getdefaultlocale()[1]
    print >> sys.stderr, "Using", encoding , "for input and output"
    
    sys.stdout = codecs.getwriter(encoding)(sys.stdout);
        
    for l in codecs.getreader(encoding)(sys.stdin):        
        ss = l.split()
        
        
        if len(ss) > 0:
            word = ss[0]
            word = re.sub(r".*\[(.*)\]", r"\1", word)
            word = word.lower()
            words = [word]        
            for (fr, to) in variant_rules:
                new_word = re.sub(r"^" + fr + r"$", to, words[0])
                if new_word != words[0]:
                    words.append(new_word)
            
            for i in xrange(len(words)):
                word = words[i]
                phon = word
                for (fr, to) in rules:
                    phon = re.sub(fr, to, phon)
                
                if i > 0:
                    print "%s(%d)" % (ss[0], (i+1)),
                else:
                    print ss[0],
                print " ".join(filter(is_phone, [phon2phon_map.get(p, p) for p  in phon]))
                sys.stdout.flush()
         
        
