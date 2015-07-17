import sys
import taxon
import time
import datetime


def timeStamp():
    '''Return time stamp'''
    t = time.time()
    fmt = '[%Y-%m-%d %H:%M:%S]'
    return datetime.datetime.fromtimestamp(t).strftime(fmt)

## run this as a script
if __name__ == "__main__":
    ids=['1211997']
    if len(sys.argv) == 1:
        print "Supply your own id for the tree. Here is an example"
    else:
        ids=sys.argv[1:]

    print "Starting to read: " + timeStamp()
    sys.stdout.flush()
    taxa = taxon.readNodes()
    names,blastname = taxon.readNames()
    divs = taxon.readDivisions()
    print "Finished read: " + timeStamp()
    sys.stdout.flush()
    for i in ids:
        c=0
        if i not in taxa:
            sys.stderr.write("Error: ID " + str(i) + " was not found in the taxonomy filei\n")
            sys.exit(0)
        while taxa[i].parent != '1' and i != '1':
            #print " " * c, taxa[i].taxid, "name:", names[i].name, "rank:", taxa[i].rank, "div:", taxa[i].division, "code:", divs[taxa[i].division].code
            bn=names[i].name
            if i in blastname:
                bn=blastname[i].name
            print taxa[i].taxid, "name:", names[i].name, "blast name", bn, "rank:", taxa[i].rank, "parent: ", taxa[i].parent
            i=taxa[i].parent
            c+=1
        print
    print "Finished: " + timeStamp()
    sys.stdout.flush()

