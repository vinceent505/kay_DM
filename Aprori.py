from typing import final
import pandas as pd
from itertools import chain, combinations
import os
import sys
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
import time


# TDB = [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
global_L=[]
global_freq = []

def import_data_test():
    path = os.path.join(os.path.dirname(__file__),'ibm-2021.txt')
    database = open(path,'r')
    list_dict = {}
    list_dict = defaultdict(list)
    for i in database:
        list_dict[int(i.split()[1])].append(int(i.split()[2]))
    return list_dict

def import_data1():
    path = os.path.join(os.path.dirname(__file__),'Groceries_dataset.csv')

    # df store data
    database = pd.read_csv(path, sep = ',')
    
    list_dict = {}
    list_dict = defaultdict(list)
    labelencoder = LabelEncoder()
    database["itemDescription"] = labelencoder.fit_transform(database["itemDescription"])
    for i in database.iloc:
        list_dict[i["Member_number"]].append(i["itemDescription"])
    #print('list_dict',list_dict)
    
    return list_dict

def import_data():
    path = os.path.join(os.path.dirname(__file__),'groceries - groceries.csv')
    database = pd.read_csv(path, sep = ',')
    #print(database)
    myset = set()
    
    for i in database:
        if i=="Item(s)":
            continue
        for j in database[i]:
            if pd.isnull(j):
                continue
            else:
                myset.add(j)
                #print('j',j) # item name
    d = {}
    d = defaultdict(str)
    for i , j in enumerate(myset):
        d[j] = i
    print("d: ", d)
    labelencoder = LabelEncoder()
    myset = labelencoder.fit_transform(list(myset))
    
    itemlist = []
    for i in range(len(database)): # 0->9834
        sub_itemlist = []
        for j in database: # Item1 -> Item 32
            # print(i,j,type(j), database[j][i])
            if pd.isnull(database[j][i]):
                continue
            elif pd.api.types.is_integer_dtype(type(database[j][i])):
                continue
            else:
                sub_itemlist.append(d[database[j][i]])
                #print(database[j][i])   
        itemlist.append(sub_itemlist) 

    return_dict = {}
    for num, item in enumerate(itemlist):
        return_dict[num] = item
    return return_dict, {v : k for k, v in d.items()}

def itemlist1(TDB):   #C1
    unique_list = []
    for i in range(len(TDB)):
        row = set(TDB[i])
        
        for item in row:
            if item not in unique_list:
                unique_list.append(item)
    unique_list.sort()
    #print('unique_list:',unique_list)
    # unique_list = np.transpose(unique_list)
    # length = len(unique_list)
    #unique_list = unique_list.reshape((length,1))
    #print('1',unique_list)
    #ul = list(unique_list)#.tolist -> [array([1]), array([2]), array([3]), array([4]), array([5])] (n,1)的array
    # ul = ul.sort()
    #print('2',unique_list)
    
    return unique_list


def get_L(itemsetlst,TDB,k, min_sup): #[2,3,5]
    
    #print('here',itemsetlst) 
    freq1 = []
    #print('length of itemsetlst:',len(itemsetlst))
    for i in range(len(itemsetlst)):
        freq1.append(0)   
    for i in range(len(TDB)):
        row=TDB[i]
        row_set=set(row) #{1,3,4}
        #print('row_set: ',row_set)
        if k==1 :
            for i in range(len(itemsetlst)):
                for item2 in row_set:
                    if itemsetlst[i] == item2:
                        freq1[i]+=1
        else:
            #print('------',itemsetlst) # [[1, 2], [1, 3], [1, 5], [2, 3], [2, 5], [3, 5]]
            for j in range(len(itemsetlst)):#[{1,2},{3,4}]
                if (row_set.union(set(itemsetlst[j])))==row_set:
                    if (row_set.intersection(set(itemsetlst[j])))==set(itemsetlst[j]):
                        freq1[j]+=1
    out = []
    freq = []
    for cnt in range(len(freq1)):
        support = freq1[cnt]
        if support >= min_sup :
            # print(support)
            # print(min_sup)
            out.append(itemsetlst[cnt])
            freq.append(freq1[cnt])
    
    return out,freq

def get_C2(L,length):
    out = []
    ls = []
    if length == 1 or length == 2: 
        for i in combinations(L,length):
            
            out.append(i)
        
        return out
    else:
        #a=[{1,2}, {1, 3}, {1, 5}, {2, 3}, {2, 5}, {3, 5}] 
        
        for i in combinations(L,length):
            out = []
            st = set()

            for item in list(i):
                st=st.union(set(item)) #[[1, 3], [2, 3], [2, 5], [3, 5]]
            # print("st: ", st) #{1, 2, 3} -> {1,2,5} -> ...
            # print(length)
            if len(st)==length:  
                for s in st:
                    # print("s: ", s)
                    out.append(s)   
            if len(out):
                # print("out: ", out)
                ls.append(tuple(out))
            
        # print("ls: ", ls)
        return ls

def powerset(s):
    if(str(type(s).__name__))=="int":
        # print('here')
        return [[],s]
    else:     
        return chain.from_iterable(combinations(s, r) for r in range(0, len(s)+1))

def rule_gen(global_L,global_freq,TDB,minConf=0.1):
    D = dict()
    ans = []
    for i,item in enumerate(global_L):
        if(str(type(item).__name__))=="int":
            D[item] = global_freq[i]    
        else:
            try:
                D[tuple(sorted(item))] = global_freq[i]
            except:
                print("error item: ", item)
                print(type(item))
                exit()
    # print(global_L,global_freq)
    # print("D: ", D)
    for item in D:
        l = []
        if(str(type(item).__name__))=="int":
            l.append(item)
        elif not item:
            pass
        else:
            try:
                l = list(item)
            except:
                print("error: ", item)
                exit()
        subset = powerset(l)

        # print("L: ", l)
        # print("i: ", item)
        for s in subset:
            # print(len(s))
            if not len(s):
                continue
            if len(s)==1:
                confidence = float(D[item]/D[s[0]])
                support = float(D[item]/len(TDB))
            else:
                try:
                    if(str(type(s).__name__))=="int":
                        confidence = float(D[item]/D[s])
                        support = float(D[item]/len(TDB))
                    else:
                        confidence = float(D[item]/D[tuple(sorted(s))])
                        support = float(D[item]/len(TDB))
                except Exception as e:
                    print(item)
                    print(s)
                    print(e)
                    exit()
            # print("con: ", confidence)
            if(confidence > minConf):
                st = set()
                st = st.union(s)
                ans.append([st, set(set(l).difference(st)), confidence, support])
    
    return ans
        
if __name__ == "__main__":
    if str(sys.argv[1]) == "ibm-2021":
        TDB = import_data_test()
    elif str(sys.argv[1]) == "groceries":
        TDB, label_d = import_data()
        print(label_d)
    TDB = list(TDB.values())
    time_dict = defaultdict()
    #for minsup in [60,100,200]:#70,80,90,100,200, 400, 600]:
    #    m = [0.1,0.2,0.3,0.4,0.5]
    #for minConf in m:
    minsup=100
    minConf=0.3
    global_L = []
    global_freq = []
    count = 0
    start = time.time()
    itemsetlst = itemlist1(TDB) #C1 = [1,2,3,4,5]
    k = 1
    L,freqlist=get_L(itemsetlst,TDB,k,minsup)  #L=[1,2,3,5] ,freq1 = [2,3,3,1,3]->[2,3,3,3]
    
    cur_L=L
    
    #print(TDB)
    for item in L:
        global_L.append(item)
    for freq in freqlist:
        global_freq.append(freq)

    k+=1
    cur_L = []
    
    while True:
        # print(k)
        C2=get_C2(L,k) #[[1, 2], [1, 3], [1, 5], [2, 3], [2, 5], [3, 5]]
        # print('C2: ', C2) #[2,3,5]
        L, freqlist = get_L(C2,TDB,k,minsup)
        
        if not len(L):
            break
        
        for item in L:
        #    print('append',item)
            global_L.append(item)
        # print(global_L)
        for freq in freqlist:
            global_freq.append(freq)
        k+=1
        cur_L = L
    # print("global freq: ", global_freq)
    ans = rule_gen(global_L,global_freq,TDB,0.3)
    # print("ans: ", ans)  
    
    if str(sys.argv[1]) == "groceries":
        final_ans = {}
        final_ans = defaultdict(list)
        for i, j in enumerate(ans):
            if len(j[1]):
                final_ans[i].append([])
                final_ans[i].append([])
                final_ans[i].append([])
                final_ans[i].append([])
                for k in j[0]:
                    final_ans[i][0].append(label_d[k])
                    pass
                for k in j[1]:
                    final_ans[i][1].append(label_d[k])
                    pass
                final_ans[i][2].append(j[2])
                    
                final_ans[i][3].append(j[3])

        print(final_ans)
        for num, i in enumerate(final_ans.values()):
            count+=1
            print("Relation rules: { {", ', '.join(i[0]), '} -> { ', ', '.join(i[1]), '} }')
            print('Support',i[3][0])
            print('confidence',i[2][0])
            print(' ')

        print("Total Time: ", time.time()-start, " sec")

        # print('minsup',minsup)
        # print('minconf',minConf)
        # print("num: ", count)
        time_dict[minsup] = time.time()-start
        print(" ")
    elif str(sys.argv[1]) == "ibm-2021":
        
        for i in ans:
            if len(i[1]):
                count+=1
                print("Relation rules: {",i[0],'->',i[1],'}')
                print('Support',i[3])
                print('confidence',i[2])
                print(' ')

        print("Total Time: ", time.time()-start, " sec")

        # print('minsup',minsup)
        # print('minconf',minConf)
        # print("num: ", count)
        time_dict[minsup] = time.time()-start
        print(" ")
    print(str(sys.argv[0]))
#print(time_dict)
