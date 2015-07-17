"""

Check the output of the taxonomy results

"""

import os
import sys

try:
    of = sys.argv[1]
except:
    sys.exit(sys.argv[0] + " <focus docker output file>")


with open(of, 'r') as rin:
    count = {}
    for l in rin:
        # ignore comments
        if l.startswith('@'):
            continue
        if l.startswith('#'):
            continue
        if not (l.strip()):
            continue

        p = l.strip().split("\t")
        if (len(p) < 2):
            sys.stderr.write("WARNING: Skipped line |" + l.strip() + "|\n")

        count[p[1]] = count.get(p[1], 0) + float(p[-1])
        
        # test that there are the same number of | in columns 

        if p[2].count('|') != p[3].count('|'):
            sys.stderr.write("FATAL: There are a different number of | in "  + p[2] + " and " + p[3] + "\n") 



for c in count:
    if count[c] > 100:
        sys.stderr.write("WARNING: There are more than 100 of " + c + " total: " + str(count[c]) + "\n")
