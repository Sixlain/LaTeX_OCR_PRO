import json
from sympy import*
import tree_Method as tm
'''
with open('result.json','r') as f:
    totalList=json.load(f)
good=0
bad=0
myobj=sympify(totalList[1][1])
'''
def ptFun(node):
    if node['sym']!=None:
        return node['sym']
    else:
        return node['fun']

x,y,z=symbols('x y z')
myobj=2*sin(x**z+y)*sin(y+z)+2*sin(x**z+y)*sin(x+z)
#myobj=x+y+z
#myobj=logcombine(myobj)

print(str(myobj.args[1].func))
l=[]
obj=tm.StandardFormula(myobj)
print(latex(obj.expr))
tree=tm.Xtree(obj.expr)
t=tree.良序树()
tree.前序打印机(t,l,ptFun)
print(l)
'''
for item in totalList:
    temp=item[1]
    try:
        myobj=sympify(temp)
    except:
        bad+=1
    else:
        good+=1
print(bad,good)
print(len(totalList))
'''
