from sympy import*

from functools import cmp_to_key
class StandardFormula():
    def __init__(self,expr):#自动根据类型导入表达式，支持字符串/sympy对象两种形式。请不要输入除这两种格式外其他格式！
        if type(expr) != type("str"):
            self.expr=expr
        else:
            try:
                temp=sympify(expr)
            except:
                return ImportError
            else:
                self.expr=temp
        if (self.expr.is_Equality):
            self.__eqlProcess()#如果是等式，使用内部函数进行特别处理
        self.__std()



    def __eqlProcess(self):#处理形如a=b的等式
        expr=self.expr
        self.expr=[]#以一个list的形式构造函数族
        minus=expr.args[0] - expr.args[1] #a-b构造法
        minus=factor(minus)#通分
        if expr.is_Mul:
            for item in minus.args:
                if item.is_Number:
                    continue #常数不要管
                elif item.is_Pow and item.exp.is_Number and item.exp < 0:#python 表达式从左到右，支持短路，故不会出问题
                    continue #分母不要管
                else:
                    self.expr.append(item)
        else:
            self.expr.append(expr)#即便是等式，还是用一个List来加以区分

    def __stdSingle(self,expr):#标准化操作(单个表达式)
        funList=[expand]
        #1:2选1启动
        #funList.extend([expand_log,expand_power_exp，expand_func])
        #2:
        #funList.extend([logcombine,powsimp])
        temp=expr#注入表达式
        for fun in funList:
            temp=fun(temp)
            #print(latex(temp))测试输出用
        return temp

    def __std(self):#标准化函数
        if type(self.expr)==type([]):#多个标准化
            output=[]
            for item in self.expr:
                output.append(self.__stdSingle(item))
        else:
            self.expr=self.__stdSingle(self.expr)

class Xtree():#神秘的X树控制器
    #我们不构成X树，我们只是X树的控制器
    def __init__(self,expr):
        self.expr=expr #树的表达式
        self.__construtTree()


    def __XdictBuilder(self,node,childrenList=[],father=None):#X树的节点（字典）构造器，被你发现啦！没有递归功能哦~
        dict={}
        dict['children']=childrenList
        dict['fun']=node.func
        #dict.setdefault('father',father)   #和C++保持一致，也留个上级节点吧（虽然不知道有什么用）
        #为了避免循环引用，砍掉了这个功能
        if node.is_Atom:  # 当前节点的sym对象(若为叶子，记录symbol本体）
            dict['sym']=node
        else:
            dict['sym']=None
        return dict
    def __nameRebuild(self,name):
        #重新构建函数名，让它好看一点
        head=name.rfind('.')
        tail=name.rfind('\'')
        if head>0 and tail>0:
            return name[head+1:tail]
        else:
            return name
    def __SdictBuilder(self,node,childrenList=[]):#纯字符串的Xs树
        dict = {}
        dict['children']= childrenList
        dict['fun']= self.__nameRebuild(str(node.func))#把函数名搞好看点
        # dict.setdefault('father',father)   #和C++保持一致，也留个上级节点吧（虽然不知道有什么用）
        # 为了避免循环引用，砍掉了这个功能
        if node.is_Atom:  # 当前节点的sym对象(若为叶子，记录symbol本体）
            if node.is_Symbol:
                dict['sym']= node.name
            else:
                dict['fun']='NUM'
                dict['sym']=None
                dict['num']=(node.p,node.q)
        else:
            dict['sym']= None
        return dict

    def __construtTree(self):#构建语法树，并编号
        self.tree=self.__前序递归构造(self.expr)

    def __前序递归构造(self,node,father=None):#只是通用的递归器而已
        if (len(node.args) == 0):  # 是叶子
            return self.__SdictBuilder(node)
        else:
            chList=[]#完成childrenList
            for item in node.args:
                chList.append(self.__前序递归构造(item))#纯粹是把孩子放进去，本体还没有放
            return self.__SdictBuilder(node,chList)




    def __交换律检查(self,item):
        set={'Pow'}
        if item['fun'] in set:
            return False
        else:
            return True
    def __等价检查(self,a,b):
        #检查是否等价
        alist=[]
        blist=[]
        self.前序打印机(a, alist, self.__叶子打印机)#打印参数表
        self.前序打印机(b, blist, self.__叶子打印机)
        n=len(alist)
        for i in range(n):
            for j in range(i+1,n):
                if((alist[i]==alist[j])!=(blist[i]==blist[j])):
                    return False
        return True
    def __等价检查(self,a,b):
        #检查是否等价。如果不等价，不同的排前面，相同的排后面
        alist=[]
        blist=[]
        self.前序打印机(a, alist, self.__叶子打印机)#打印参数表
        self.前序打印机(b, blist, self.__叶子打印机)
        n=len(alist)
        for i in range(n):
            for j in range(i+1,n):
                if((alist[i]==alist[j])!=(blist[i]==blist[j])):
                    if(alist[i]==alist[j]):
                        return -1
                    else:
                        return 1
        return 0


    def __叶子打印机(self,node):
        if len(node['children'])==0:
            return node['sym']
        else:
            return None

    def 良序树(self):
        self.递归次数=0
        sorted(self.tree['children'], key=cmp_to_key(self.__节点递归比较))
        print(self.递归次数)
        return self.tree

    def 前序打印机(self,node,paper,printFun):#连续打印在一张小抄上
        temp=printFun(node)
        if temp!=None:
            paper.append(temp)#接在后面打印
        for item in node['children']:#递归打印
            self.前序打印机(item,paper,printFun)
    def __numCmp(self,a,b):#比较两个数字的函数。因为两个有理数不好比较
        return a[0]*b[1]-a[1]*b[0]

    def __节点递归比较(self,a,b):#正数a>b,0则a=b，负数a<b
        self.递归次数+=1
        la=len(a['children'])
        lb=len(b['children'])
        if(la==lb):
            if(a['fun']==b['fun']):
                if la==0:#没有孩子，那就是两个符号进行比较，那就是相同的。这个没必要做完备性检查
                    if a['fun']=='NUM':
                        return self.__numCmp(a['num'],b['num'])
                    else:
                        return 0
                else:
                    if self.__交换律检查(a):
                        sorted(a['children'], key=cmp_to_key(self.__节点递归比较))
                    if self.__交换律检查(b):
                        sorted(b['children'], key=cmp_to_key(self.__节点递归比较))
                    n = len(a['children'])  # n重比较
                    for i in range(n):
                        temp = self.__节点递归比较(a['children'][i], b['children'][i])
                        if (temp != 0):
                            return temp
                    return self.__等价检查(a,b)
                    '''原来的问题用一个trick搁置了。理论上还需要证明trick是有效的
                    if self.__等价检查(a,b):
                        return 0#每个孩子都相同，通过检查,辣是真的相同了\
                    else:
                        print('Theory Warning')#理论错误
                        return 0'''
            elif(a['fun']>b['fun']):
                return 1
            else:
                return -1
        else:
            return la-lb















