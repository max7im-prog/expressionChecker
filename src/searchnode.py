from typing import List
from my_parser import MyParser
from copy import deepcopy
from lark import Tree, Token
from equiv import Equiv
from copy import deepcopy
from normalize import NormalizeTree


class SearchNode:
    def __repr__(self):
        return SearchNode.equationRepr(self.tree)
    
    def __str__(self):
        return SearchNode.equationRepr(self.tree)
    
    @staticmethod
    def equationRepr(tree: Tree):
        arr = []
        ans = ""
        for ch in tree.children:
            if isinstance(ch,Tree):
                arr.append(ch)
        if(tree.data == "sum"):
            ans = ans + "("
            ans = ans + SearchNode.equationRepr(arr[0])
            for ch in arr[1::]:
                ans = ans + "+" + SearchNode.equationRepr(ch)
            ans = ans + ")"
        elif(tree.data == "mul"):
            ans = ans + "("
            ans = ans + SearchNode.equationRepr(arr[0])
            for ch in arr[1::]:
                ans = ans + "*" + SearchNode.equationRepr(ch)
            ans = ans + ")"
        elif(tree.data == "fraq"):
            ans = ans + "("
            ans = ans + SearchNode.equationRepr(arr[0])
            for ch in arr[1::]:
                ans = ans + "/" + SearchNode.equationRepr(ch)
            ans = ans + ")"
        elif(tree.data == "sub"):
            ans = ans + "("
            ans = ans + SearchNode.equationRepr(arr[0])
            for ch in arr[1::]:
                ans = ans + "-" + SearchNode.equationRepr(ch)
            ans = ans + ")"
        elif(tree.data == "pow"):
            ans = ans + "("
            ans = ans + SearchNode.equationRepr(arr[0])
            for ch in arr[1::]:
                ans = ans + "**" + SearchNode.equationRepr(ch)
            ans = ans + ")"
        elif(tree.data == "var"):
            ans = tree.children[0]
        elif(tree.data == "num"):
            ans = tree.children[0]
        else:
            ans = "???"
                
        
        return ans
        
        
    
    def __init__(self, equation_or_ancestor):
        parser: MyParser = MyParser()
        if isinstance(equation_or_ancestor, str):
            self.tree: Tree = parser.parse(equation_or_ancestor).children[0]
        elif isinstance(equation_or_ancestor, SearchNode):
            self.tree: Tree = deepcopy(equation_or_ancestor.tree)
        elif isinstance(equation_or_ancestor, Tree):
            self.tree: Tree = deepcopy(equation_or_ancestor)  
        else:
            raise TypeError("Expected a string or a Tree")
        self.normalize()
        self.elemRefs: List[Tree] = self.getElementsReferences(self.tree)
        self.elemEquivs: List[Tree] = self.getAllElemEquivalents(self.elemRefs)
        self.childNodes: List[SearchNode] = []
        self.ancestorNode = None
        

    def getAllElemEquivalents(self, arr: List[Tree]) -> List[Tree]:
        ret: List[Tree] = []
        for ref in self.elemRefs:
            ret.append(Equiv.getEquiv(ref))

        return ret

    def getElementsReferences(self, curTree: Tree) -> List[Tree]:
        arr = []
        arr = arr + [curTree]
        if isinstance(curTree, Tree):
            for child in curTree.children:
                arr = arr + self.getElementsReferences(child)
        return arr

    def getChildNodes(self) -> List:
        """computes all possible equivalents of a tree and returns them in a list.
        DOES NOT ADD them to childNodes of a node"""
        ret: List[SearchNode] = []
        for numRef in range(len(self.elemRefs)):
            for numEq in range(len(self.elemEquivs[numRef])):
                nextChild: SearchNode = SearchNode(self)
                nextChild.elemRefs[numRef].data = nextChild.elemEquivs[numRef][numEq].data
                nextChild.elemRefs[numRef].children = deepcopy(
                    self.elemEquivs[numRef][numEq].children
                )
                ret.append(nextChild)
        for i in ret:
            i.normalize()
            i.recalculateEquivalents()
        return ret

    def findChildNodes(self) -> None:
        "computes all possible equivalents of a tree. adds them to childNodes of a node"
        
        self.childNodes = self.getChildNodes()
        for node in self.childNodes:
            node.setAncestor(self)

    def setAncestor(self, ancestor:'SearchNode'):
        if not isinstance(ancestor, SearchNode):
            raise TypeError("Expected SearchNode")
        self.ancestorNode = ancestor

    def normalize(self):
        normalizer: NormalizeTree = NormalizeTree()
        self.tree = normalizer.transform(self.tree)
        
    def recalculateEquivalents(self):
        self.elemRefs = self.getElementsReferences(self.tree)
        self.elemEquivs = self.getAllElemEquivalents(self.elemRefs)
        
        
    def forestPretty(self,depth:int = 3,curDepth:int = 0) -> str:
        ret = "\t"*curDepth + self.__str__() + "\n"
        if curDepth < depth:
            for ch in self.childNodes:
                ret += ch.forestPretty(depth,curDepth+1)
        elif len(self.childNodes) != 0:
            ret += "\t"*(curDepth+1) + "..." + "\n"
        
        
        return ret
        
        
        
