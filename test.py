import bz2
import json
import codecs
import os
import re

DATA = "jstest.json"
OUT_FILE = "rec.json"

with open(DATA, mode='rt') as f:
    temp = ''
    first = True
    with open(OUT_FILE, mode='w') as nf:
        nf.write('[\n')
        for line in f:
            if line.startswith('{'):
                temp = line
            elif line.startswith('}'):
                # Add extra conditions for humans before storing
                temp = temp+'}'
                temp3 = json.loads(temp)
                # print(temp3['claims']['P31'], end='\n\n')
                if first:
                    # Only write the required data in a different format, we don't need the complicated json structure
                    nf.write(temp)
                    first = False
                else:
                    nf.write(',\n\n'+temp)
            else:
                temp = temp+line
        nf.write('\n]')

test = []
with open(OUT_FILE) as js:
    test = json.load(js)
print(test)
