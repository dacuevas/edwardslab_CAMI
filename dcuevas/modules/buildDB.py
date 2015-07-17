import sys
import parseTaxon
import time
import datetime


def timeStamp():
    '''Return time stamp'''
    t = time.time()
    fmt = '[%Y-%m-%d %H:%M:%S]'
    return datetime.datetime.fromtimestamp(t).strftime(fmt)

## run this as a script
if __name__ == "__main__":
    f = open("err.txt", "w")
    rankfile = open("rank.txt", "w")
    print >> sys.stderr, timeStamp() + "   Parsing taxonomy files"
    sys.stderr.flush()
    taxa = parseTaxon.readNodes()
    snames, bnames, ids = parseTaxon.readNames()
    focusdb = []
    with open(sys.argv[1]) as fdb:
        first = True
        for l in fdb:
            if first:
                first = False
                continue
            l = l.rstrip("\n")
            ll = l.split("\t")
            focusdb.append(ll[0])

    print >> sys.stderr, timeStamp() + "   Finished parsing files"
    sys.stderr.flush()

    # Build taxonomy order
    torder = {"superkingdom":1, "phylum":2, "class":3, "order":4, "family":5, "genus":6, "species":7}
    cnt = 0
    numSp = str(len(focusdb))
    idranks = []  # ID ranks to avoid duplicates
    for id in focusdb:
        try:
            t = taxa[id]
        except KeyError:
            f.write(timeStamp() + "   Cannot find " + id + " in the taxa file\n")
            cnt += 1
            continue
        cnt += 1
        print >> sys.stderr, timeStamp() + "   Finding organism " + str(cnt) + " out of " + numSp
        sys.stderr.flush()
        resultIds = []  # Result ids to print out
        resultNames = []  # Result names to print out
        first = True
        rankToPrint = t.rank
        prevRank = None
        currRank = None
        while t.parent != "1" and id != "131567":
            # Check if this is the rank we want
            if first or t.rank in torder:
                if t.rank not in torder and first:
                    currRank = 8
                    prevRank = 9
                elif t.rank in torder and first:
                    currRank = torder[t.rank]
                    prevRank = currRank - 1
                elif t.rank in torder and not first:
                    prevRank = currRank
                    currRank = torder[t.rank]

                first = False
                # "No rank" can be strain
                #if t.rank == "no rank" and taxa[t.parent].rank not in ["species", "subspecies"]:
                #    id = t.parent
                #    t = taxa[id]
                #    continue
                #elif t.rank == "no rank":
                #    t.rank = "strain"

                # Add ID to list to avoid printing duplicates
                if id not in idranks:
                    idranks.append(id)
                    rankfile.write(id + "\t" + t.rank + "\n")

                currName = ids[id].sname

                # Append blanks for missing ranks
                diff = prevRank - currRank - 1
                while diff > 0:
                    resultIds.append("")
                    resultNames.append("")
                    diff -= 1
                resultIds.append(id)
                resultNames.append(currName)
            # Iterate to parent taxon
            id = t.parent
            t = taxa[id]
        # Check that there are 8 levels
        if len(resultIds) != len(resultNames):
            f.write(timeStamp() + "   Mismatch in number of ids and names")
        if len(resultIds) != 8:
            f.write(timeStamp() + "   Warning: there are " + str(len(resultIds)) + " ids here\n")
        print resultIds[0] + "\t" + rankToPrint + "\t" + "|".join(reversed(resultIds)) + "\t" + "|".join(reversed(resultNames))

    print >> sys.stderr, "Finished: " + timeStamp()
    f.close()
    rankfile.close()
