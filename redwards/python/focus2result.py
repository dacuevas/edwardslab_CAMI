
"""
Convert the focus output to a result output for CAMI. 

We don't care about the output order as we will let unix sort 
sort it out for us!

"""

import os
import sys
from cami_pickle import load_pickle


try:
    fof = sys.argv[1]
    version = sys.argv[2]
    sampleid = sys.argv[3]
except:
    sys.exit(sys.argv[0] + " <focus output file that ONLY has taxon [tab] percent> <version (any string)> <sampleid (any string)>")


# read FOCUS results
count={}
with open(fof, 'r') as gin:
    for l in gin:
        p=l.strip().split("\t")
        count[p[0].strip()]=float(p[1])

# read our pickled data 
data = load_pickle("/home/taxonomy.p")

# now we need to go through all levels and sum the results

levels = {}
parent_tax = {}


# print the header information
#

print("#CAMI Submission for Taxonomic Profiling")
print("@Version:" + version)
print("@SampleID:"+ sampleid)
print("@Ranks:superkingdom|phylum|class|order|family|genus|species|strain\n")

print("@@TAXID\tRANK\tTAXPATH\tTAXPATHSN\tPERCENTAGE")

valid_taxonomy = {'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain'}

for tid in count:
    if tid not in data['taxonomy']:
        sys.exit("NO |" + tid + "| found in the taxonomy")
    taxlist =  data['taxonomy'][tid][2].split("|")
    taxlistdef = data['taxonomy'][tid][3].split("|")

    if len(taxlist) != len(taxlistdef):
        sys.stderr.exit(data['taxonomy'][tid][2] + " and " + data['taxonomy'][tid][3] + " are not the same length")

    # delete the lowest entries, as we don't want to repeat them
    taxlist.pop()
    taxlistdef.pop()

    while (taxlist and taxlistdef):
        # remember what this string should be for below
        tls = "|".join(taxlist)
        tld = "|".join(taxlistdef)

        # what is my current id
        current = taxlist.pop()
        currentdf = taxlistdef.pop()

        if current == "":
            continue
        if current not in parent_tax:
            crank = data['rank'][current]
            if crank not in valid_taxonomy:
                crank = ""
            parent_tax[current] = [current, crank, tls, tld]
        levels[current]=levels.get(current, 0) + count[tid]

    # check that it has 6 or less significant digits
    if data['taxonomy'][tid][1] not in valid_taxonomy:
        data['taxonomy'][tid][1] = ""
    t = "\t".join(data['taxonomy'][tid])
    print("%s\t%0.6f" % (t, count[tid]))

for l in levels:
    t = "\t".join(parent_tax[l])
    print("%s\t%0.6f" % (t, levels[l]))





