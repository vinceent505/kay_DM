from collections import defaultdict
import pandas as pd
from itertools import chain, combinations

def getminsup(Ci , TDB ,minsup):
    #support
    L=[]
    # #df = pd.DataFrame(columns=[i for i in range(len(candidatelst))])
    # df = pd.DataFrame(frozenset(candidatelst),columns=[i for i in range(len(candidatelst))])
    # print(df)
    freq_dict = dict()
    #frozen_set = set()
    theset =set()
    for items in Ci:
        theset.add(items)
    #     frozen_set.add(frozenset(items))
    for f_set in theset:#frozen_set:
        freq_dict[f_set]=0

    for i in range(len(TDB)):
        itemrow=TDB.loc[i,'items']
        setcur=set(itemrow.split(','))
        print('---------')
        print(setcur)
        print('---------')
        
    
        for f_set in theset:#frozen_set:
            if ((f_set|setcur)==setcur and (f_set.intersection(setcur)==f_set)):#frozenset.union(setcur,f_set))==setcur and (frozenset.intersection(setcur,f_set))==f_set:
                freq_dict[f_set]+=1
        print(i,freq_dict)
        for f_set,cnt in freq_dict.items():
            support = float(cnt/len(TDB))
            #print(f_set,support)
            if support >= minsup and set(list(f_set)) not in L:
                L.append(set(list(f_set)))
    return L
           
   
    #return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
def getUnion(itemlist, length):
    lst = []
    len = 0
    for item in itemlist:
        s = set()
        s.add(set(item))
        for item2 in itemlist:
            s.add(set(item2))
            if (len(s))==length:
                lst.append(s)
            else:
                s.remove(frozenset(item2))
                s.add(frozenset(item))
    #print(lst)
    unique_lst = []
    for x in lst:
        if x not in unique_lst:
            unique_lst.append(x)
    print('after union:',unique_lst)
    return unique_lst

def pruning(candidatelst,prevFreqlist,length): #
    for setitem in candidatelst:
        if setitem not in prevFreqlist:
            candidatelst.remove(setitem)
            break
    print('After pruning:',candidatelst)
    return candidatelst
    # for i, row in Ci.iterrows():
    #     print('row',row)
    
        # subsets = combinations(item, length)
        # for subset in subsets:
        #     # if the subset is not in previous K-frequent get, then remove the set
        #     if(frozenset(subset) not in prevFreqSet):
        #         Ci.remove(item)
        #         break
    #return Ci


