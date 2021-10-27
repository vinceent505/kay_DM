import csv
import os
import pandas as pd
from collections import Counter
from datamining_utils import *

path = os.path.join(os.path.dirname(__file__),'GroceryStoreDataSet.csv')

# df store data
TDB = pd.read_csv(path,names = ['items'], sep = ',')
print(TDB.head(5))
#itemset1 store items
itemset1 = set()

# 1 itemset
for i in range(len(TDB)):
    itemrow=TDB.loc[i,'items']
    #print(itemrow)
    setcur=set()
    setcur=set(itemrow.split(','))
    #print(setcur)
    itemset1=(itemset1|setcur)
#print(itemset1)

#dictionary
freq1 = {}
globfreqset = {}

for item in itemset1:
    freq1[item]=0
    
# C1->freq dict1
for i in range(len(TDB)):
    setcur=set()
    itemrow=TDB.loc[i,'items']
    setcur=set(itemrow.split(','))
    #print(setcur)
    for cur_item in setcur:
        #print(cur_item)
        freq1[cur_item]+=1
#print(freq1)

#support
minsup = 0.3
L1 = set()
for item, supCount in freq1.items():
    if supCount/len(TDB) >= minsup:
        L1.add(item)

cur_L = list(L1)
k=2
print(cur_L) #['BREAD', 'COFFEE', 'BISCUIT', 'SUGER', 'CORNFLAKES', 'TEA']
while cur_L:

    #store freq item set
    globfreqset[k-2]=cur_L 
    # self Ck=join(Lk*Lk) {A*B | |A&B|= k } 
    candidatelst = getUnion(cur_L,k) # DataFrame
#    df = pd.DataFrame(frozenset(candidatelst[i]) for i in range(len(candidatelst)),columns=[i for i in range(len(candidatelst))])
#    print(df)
    # Perform subset testing and remove pruned supersets
    # d = dict()
    Ci = pruning(candidatelst, cur_L, k) #(list,list)
    
    # Scanning itemSet for counting support
    minsup = 0.1
    cur_L = getminsup(Ci ,TDB, minsup)
    print(cur_L)
    print('-------------')
    k+=1
    
