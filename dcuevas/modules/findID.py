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
    query = ['Escherichia coli']
    if len(sys.argv) == 1:
        print "Supply your own name for the tree. Here is an example"
    else:
        query = sys.argv[1:]

    print "Starting to read: " + timeStamp()
    sys.stdout.flush()
    taxa = parseTaxon.readNodes()
    snames, bnames, ids = parseTaxon.readNames()
    print "Finished read: " + timeStamp()
    sys.stdout.flush()

    for n in query:
        if n not in snames:
            for i, info in ids.items():
                if info.bname == n or info.sname == n:
                    id = i
                    break
            else:
                sys.stderr.write("Error: Name " + str(n) + " was not found in the taxonomy filei\n")
                sys.exit(0)
        else:
            id = snames[n]
        resultIds = []
        resultNames = []
        while taxa[id].parent != "1" and id != "1" and id != "131567":
            currName = ids[id].bname
            if currName is None:
                currName = ids[id].sname
            resultIds.append(id)
            resultNames.append(currName)
            id = taxa[id].parent
        print "|".join(reversed(resultIds)) + "\t" + "|".join(reversed(resultNames))

#    for n in names:
#        c=0
#        if i not in taxa:
#            sys.stderr.write("Error: ID " + str(i) + " was not found in the taxonomy filei\n")
#            sys.exit(0)
#        while taxa[i].parent != '1' and i != '1':
#            bn=names[i].name
#            if i in blastname:
#                bn=blastname[i].name
#            print taxa[i].taxid, "name:", names[i].name, "blast name", bn, "rank:", taxa[i].rank, "parent: ", taxa[i].parent
#            i=taxa[i].parent
#            c+=1
#        print
    print "Finished: " + timeStamp()
    sys.stdout.flush()
