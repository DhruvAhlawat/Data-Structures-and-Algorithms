#first we make an AVL tree
from typing import List
import math

from django.http import QueryDict

def comparision(a,b): #returns if a > b
    return a._value > b._value;
def FindHeight(a):
    if(a == None):
        return 0;
    else:
        return a._height;
#simply we can sort the data first
class Node(): #essentially is a binary subtree rooted at self
    _value = (0,0);
    _left = None;
    _right = None;
    _height = 0;
    _parent = None;
    def __init__(self,a:tuple) -> None:
        self._value = a;
        self._height = 1;

    def __UpdateHeight(self):
        l:Node = self._left;
        r:Node = self._right;
        # if(l == None and r == None):
        #     self._height = 1;
        # elif(l == None):
        #     self._height = 1 + r._height;
        # elif(r == None):
        #     self._height = 1 + l._height;
        # else:
        #     self._height = max(1+l._height,1+r._height);
        self._height = max(1+FindHeight(l),1+FindHeight(r));

    #Function to Update the heights of all the parents of the current node
    def __UpdateAllParentsHeights(self):
        a:Node = self;
        while(a != None):
            a.__UpdateHeight();
            a = a._parent;
        
        

    def setLeft(self,l): #set left child of node, it can even be None to signify no left child
        prevLeft = self._left;
        if(prevLeft is not None):
            if(prevLeft._parent == self):
                prevLeft._parent = None;
        self._left = l;
        if(l == None):
            if(self._right == None):
                self._height = 1;
            else:
                self._height = 1 + self._right._height;
            self.__UpdateAllParentsHeights();
            return prevLeft;
        #else if l is not None but an actual Node
        self._height = max(self._height,1+l._height);
        l._parent = self;
        self.__UpdateAllParentsHeights();
        return prevLeft;


    def setRight(self,r): #set right child of node
        prevRight = self._right;
        if(prevRight is not None):
            if(prevRight._parent == self):
                prevRight._parent = None;
        self._right = r;
        if(r == None):
            if(self._left == None):
                self._height = 1;
                
            else:
                self._height = self._left._height + 1;
            self.__UpdateAllParentsHeights();
            return prevRight;
        #else if r is not None but an actual Node
        #self._height = max(self._height,1+r._height);

        r._parent = self;
        self.__UpdateAllParentsHeights();
        return prevRight;
    
    def inorder(self,l):
        if(self._left is not None):
            l.extend(self._left.inorder([]));
        l.append(self._value);
        if(self._right is not None):
            l.extend(self._right.inorder([]));
        return l;
    
    def modifiedPreorder(self,l):
        l.append(self._value);
        if(self._left is not None):
            l.extend(self._left.modifiedPreorder([]));
        else:
            l.append(-1);
        if(self._right is not None):
            l.extend(self._right.modifiedPreorder([]));
        else:
            l.append(-1);
        return l;
    #checks if the subtree is balanced at this node, can instead keep a boolean and update it too
    def isBalanced(self):
        return abs(FindHeight(self._left) - FindHeight(self._right)) <= 1;
    
    def RightRotate(self):
        #We right rotate about self
        parent = self._parent;
        leftOfSelf = self._left;
        #rightOfSelf = self._right;
        rightOfLeftOfSelf = leftOfSelf._right;
        if(parent == None): #if the node is the root node (head), then it has no parent
            self.setLeft(rightOfLeftOfSelf);
            leftOfSelf.setRight(self);
            return leftOfSelf; #returns the new root node 
            print("rotation around root detected");
        elif(parent._left == self):
            parent.setLeft(leftOfSelf);
            self.setLeft(rightOfLeftOfSelf);
            leftOfSelf.setRight(self);
        elif(parent._right == self):
            parent.setRight(leftOfSelf);
            self.setLeft(rightOfLeftOfSelf);
            leftOfSelf.setRight(self);


    def LeftRotate(self):
        parent = self._parent;
        rightChild = self._right;
        leftOfRightChild = rightChild._left;
        if(parent == None):
            self.setRight(leftOfRightChild);
            rightChild.setLeft(self);
            return rightChild; #the new root node;
        elif(parent._left == self):
            parent.setLeft(rightChild);
            self.setRight(leftOfRightChild);
            rightChild.setLeft(self);
        elif(parent._right == self):
            parent.setRight(rightChild);
            self.setRight(leftOfRightChild);
            rightChild.setLeft(self);

    def ReBalance(self):
        #gotta return the new header node too if it is Head
        #then we simply rebalance the node
        if(FindHeight(self._left) > FindHeight(self._right) + 1):
            l = self._left._left;
            r = self._left._right;
            if(FindHeight(l) >= FindHeight(r)):
                #Then we simply right rotate at the, which is self
                newRoot = self._left;
                self.RightRotate(); #Hopefully this return works in sending the new Root
                return newRoot; 
            else:
                self._left.LeftRotate(); #left rotating the left side of the root first
                newRoot = self._left;
                self.RightRotate();
                return newRoot;
        elif(FindHeight(self._right) > FindHeight(self._left)+1):
            l = self._right._left;
            r = self._right._right;
            if(FindHeight(l) <= FindHeight(r)):
                newRoot = self._right;
                self.LeftRotate();
                return newRoot;
            else:
                self._right.RightRotate();
                newRoot = self._right;
                self.LeftRotate();
                return newRoot;        

    def leafInorder(self):
        if(self._height == 1):
            return [self._value];
        l = [];
        if(self._left != None):
            l.extend(self._left.leafInorder());
        if(self._right != None):
            l.extend(self._right.leafInorder());
        return l;

class bst:
    _root = None;
    def __init__(self,l:List) -> None:
        l.sort();
        self._root = self.BuildTree(l);
    def GetHeight(self):
        return self._root._height;
    def BuildTree(self,s:List):
        #asusme the list is sorted
        #first we sort the list, then we make it into a binary search tree using recursion
        if(len(s) == 1):
            return Node(s[0]);
        x = math.floor((len(s)+1)/2)-1;
        #x is the position of the median
        l = s[0:x+1];
        r = s[x+1:];
        a = Node(s[x]); #node which has 2 children
        a.setLeft(self.BuildTree(l));
        a.setRight(self.BuildTree(r));
        return a;
    def findLesser(self,x2,curNode:Node):
        l = [];
        #if it is a leaf node
        if(curNode._height == 1): 
            if(curNode._value <= x2):
                return [curNode._value];
            else:
                return [];
        if(curNode._value <= x2):
            l.extend(curNode._left.leafInorder());
            #and then check the right side
            l.extend(self.findLesser(x2,curNode._right)); 
            return l; #done
        else:
            #then all values to its right would be greater than x2, hence no point checking there
            l.extend(self.findLesser(x2,curNode._left));
            return l;
    
    def findGreater(self,x1,curNode:Node):
        l = [];
        #if it is a leaf node
        if(curNode._height == 1): 
            if(curNode._value >= x1):
                return [curNode._value];
            else:
                return [];
        if(curNode._value >= x1):
            l.extend(curNode._right.leafInorder()); #all nodes on its right would be greater than it afterall
            #and then check the right side
            l.extend(self.findGreater(x1,curNode._left)); 
            return l; #done
        else:
            #then all values to its right would be greater than x2, hence no point checking there
            l.extend(self.findGreater(x1,curNode._right));
            return l;

    def __Query(self,x1,x2,curNode:Node):
        #find and return points lying within range x1 <= x <= x2
        #then we find and return 
        #we find the first point where the search for x1 and x2 split up, let it be called v
        if(curNode._value >= x1 and curNode._value >= x2):
            curNode = curNode._left;
            return self.__Query(x1,x2,curNode);
        if(curNode._value < x1 and curNode._value < x2):
            curNode = curNode._right;
            return self.__Query(x1,x2,curNode);
        #if neither of above cases hold, then it must be the splitting point for the search
        l = [];
        l.extend(self.findGreater(x1,curNode._left));
        l.extend(self.findLesser(x2,curNode._right));
        return l;
    def Query(self,x1,x2):
        return self.__Query(x1,x2,self._root);



l = [];  
for i in range(1,30):
    l.append(i);
a = bst(l); 
#print(a._root.modifiedPreorder([]));
print(a.GetHeight());
k = 10;
print(a.findLesser(k,a._root));
print(a.findGreater(k,a._root));
print(a.Query(1,23));