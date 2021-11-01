from mining import*

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink= None
        self.parent = parentNode
        self.children = {}
    def inc(self, numOccur):
        self.count += numOccur
    def disp(self, ind=1):
        print (' ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)

# 当出现两个或两个以上的类似项时，找到最后一个类似项的实例，让该实例的self.nodeLink属性保存新出现的类似项
# 效果如同是在一条链的最后一个节点后再接入一个节点，这些链就是self.nodeLink
def updateHeader(node, targetNode):
    while node.nodeLink != None:
        node = node.nodeLink
    node.nodeLink = targetNode

# 接收处理好的事务列表，画出FP树
def updateFPtree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 判断items的第一个结点是否已做为子结点
        inTree.children[items[0]].inc(count)
    else:
        # 建立新的分支
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新相应频繁项集的链表，日后添加
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    # 递归
    if len(items) > 1:
        updateFPtree(items[1::], inTree.children[items[0]], headerTable, count)

# 输入字典格式的事务和最小支持度，返回FP树和项头表
def createFPtree(dataSet, minSup=1):
    headerTable = {}
    # 當每筆新的transection進來 更新headerTable
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 不滿足min sup 的 item刪除        
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del (headerTable[k])  
    freqItemSet = set(headerTable.keys())  # 知足最小支持度的频繁项集
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # element: [count, node]
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:  # 过滤，只取该样本中知足最小支持度的频繁项
                localD[item] = headerTable[item][0]  # element : count
                
        if len(localD) > 0:
            # 根据全局频数从大到小对单样本排序
            #orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            #print(localD.items())
            
            orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], -p[0]),reverse=True)] #key=lambda p: (p[1], -ord(p[0])),reverse=True)]
            #print('orderItems=', orderedItem)
            # 用过滤且排序后的样本更新树
            updateFPtree(orderedItem, retTree, headerTable, count)
        # for item in headerTable:
        #     print(item)
    return retTree, headerTable

# 构形成 element : count 的形式，以字典形式输出
def createInitSet(dataSet):
    retDict = {}
    Trans = []
    for trans in dataSet:
        # print(trans)
        # for item in trans:
        #     Trans.append(item)
        # trans = "".join(trans)
        key = frozenset(Trans)
        if key in retDict:
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
        #print(retDict)
    return retDict


if __name__ == '__main__':
    
    Dat = import_data()
    Dat = list(Dat.values())
    print(Dat)
    initSet = createInitSet(Dat)
    print('hi',Dat,initSet)
    myFPtree, myHeaderTab = createFPtree(initSet, 1)
    
    #print(myFPtree.disp())