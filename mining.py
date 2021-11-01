from FP_Growth import*
import time
import pandas as pd
from itertools import chain, combinations
import os
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
import sys

#TDB = [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
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
    # print("dict: ", d)
    labelencoder = LabelEncoder()
    myset = labelencoder.fit_transform(list(myset))
    # print('myset',myset)
    
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
    #print(return_dict)
    return return_dict, {v : k for k, v in d.items()}

def import_data_test():
    path = os.path.join(os.path.dirname(__file__),'ibm-2021.txt')
    database = open(path,'r')
    list_dict = {}
    list_dict = defaultdict(list)
    for i in database:
        list_dict[int(i.split()[1])].append(int(i.split()[2]))
    return list_dict

# 递归回溯，找到给定节点往上回溯到根节点的路径，并把路径存到列表中
def ascendFPtree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendFPtree(leafNode.parent, prefixPath)

# 找到给定元素名称的条件模式基，以字典格式存贮
def findPrefixPath(basePat, myHeaderTab):
    treeNode = myHeaderTab[basePat][1]  # basePat在FP树中的第一个结点
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendFPtree(treeNode, prefixPath)  # prefixPath是倒过来的，从treeNode开始到根
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count  # 关联treeNode的计数
        treeNode = treeNode.nodeLink  # 下一个basePat结点
    return condPats


def mineFPtree(inTree, headerTable, minSup, preFix, freqItemList):
    # 最开始的频繁项集是headerTable中的各元素
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # 根据频繁项的总频次排序

    #print("bigL: ",bigL)
    for basePat in bigL:  # 对每一个频繁项
        
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #print('x',newFreqSet)
        freqItemList.append(newFreqSet)

        condPattBases = findPrefixPath(basePat, headerTable)  # 当前频繁项集的条件模式基
        #print(condPattBases)
        myCondTree, myHead = createFPtree(condPattBases, minSup)  # 构造当前频繁项的条件FP树
        if myHead != None:
            mineFPtree(myCondTree, myHead, minSup, newFreqSet, freqItemList)  # 递归挖掘条件FP树

def powerset(s):
    if(str(type(s).__name__))=="int":
        # print('here')
        return [[],s]
    else:     
        return chain.from_iterable(combinations(s, r) for r in range(0, len(s)+1))


def rule_gen(freqItems,simDat , minConf,length): #freqItems = golbal_L   freq = global_freq
    freq = []
    ans = []
    D = dict()
    f = {}
    for i in freqItems:
        count = 0
        for j in simDat.values():
            if i.issubset(frozenset(j)):
                count += 1
        f[tuple(i)] = count


    for i,item in enumerate(f):
        if(str(type(item).__name__))=="int":
            D[item] = f[i]    
        else:
            D[tuple(sorted(item))] = f[item]
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
                confidence = float(D[item]/D[(s[0],)])
                support = float(D[item]/length)
            else:
                try:
                    if(str(type(s).__name__))=="int":
                        confidence = float(D[item]/D[s[0]])
                        support = float(D[item]/length)
                    else:
                        confidence = float(D[item]/D[tuple(sorted(s))])
                        support = float(D[item]/length)
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
    
    
        
    # print("Relation rules: {",i[0],'->',i[1],'}')
    # print('Support',i[3])
    # print('confidence',i[2])
    
    
    #return ans

if __name__ == '__main__':
    
    if str(sys.argv[1]) == "ibm-2021":
        simDat = import_data_test()
    elif str(sys.argv[1]) == "groceries":
        simDat, label_d = import_data()
    time_dict = defaultdict()
    #for minsup in range(50,200,150):
    minsup = 50
    minConf = 0.3
    start = time.time()
    initSet = createInitSet(simDat)
    myFPtree, myHeaderTab = createFPtree(initSet, minsup)
    freqItems = []
    f = {}
    f = defaultdict(list)
    # global_freq = []
    # print(myHeaderTab)

    mineFPtree(myFPtree, myHeaderTab, minsup, set([]), freqItems)
    length= len(simDat)
    ans = rule_gen(freqItems, simDat, minConf,length)

    
    if str(sys.argv[1]) == "ibm-2021":
        for i in ans:
            if len(i[1])!=0:
                print("Relation rules: {",i[0],'->',i[1],'}')
                print("support: ", i[2])
                print("confidence: ", i[3])
    elif str(sys.argv[1]) == "groceries":
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
            print("Relation rules: { {", ', '.join(i[0]), '} -> { ', ', '.join(i[1]), '} }')
            print('Support',i[3][0])
            print('confidence',i[2][0])
            print(' ')

        print("Total Time: ", time.time()-start, " sec")
        print(" ")

    
