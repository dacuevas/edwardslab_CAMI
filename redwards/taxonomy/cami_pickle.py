"""

Create a pickle file that has the taxonomy information and the rank
information

"""


import pickle
import os
import sys



def save_pickle(data, f='taxonomy.p'):
    ''' pickle the data'''
    pickle.dump(data, open(f, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(f='taxonomy.p'):
    return pickle.load(open(f, 'rb'))



def load_rank(f):
    """Load a simple hash with the ranks in it"""
    rank = {}
    with open(f, 'r') as fin:
        for l in fin:
            p=l.strip().split("\t")
            rank[p[0]] = p[1]
    return rank

def load_taxonomy(f):
    """ Load the taxonomy output that we will use. This is tab separated
    and the first column is the id, and the rest is everything else."""
    tax = {}
    with open(f, 'r') as fin:
        for l in fin:
            p=l.strip().split("\t")
            tax[p[0]]=p
    return tax





if __name__ == '__main__':
    try:
        taxonomyF = sys.argv[1]
        ranksF = sys.argv[2]
    except:
        sys.exit(sys.argv[0] + " <taxonomy file> <rank file>")

    data={}
    data['rank']  = load_rank(ranksF)
    data['taxonomy'] = load_taxonomy(taxonomyF)

    save_pickle(data)

