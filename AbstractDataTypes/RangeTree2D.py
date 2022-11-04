#first we make an AVL tree
from typing import List
import math

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
    yTree = None;
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
            #print("rotation around root detected");
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

    #returns a list of 'Nodes' in the sorted order order based on their values
    def leafInorder(self):
        if(self._height == 1):
            return [self._value];
        l = [];
        if(self._left != None):
            l.extend(self._left.leafInorder());
        if(self._right != None):
            l.extend(self._right.leafInorder());
        return l;

def mergeLists(a:List,b:List):
    #a and b are lists of nodes that are sorted based on their y coordinates
    #so we just merge them in sorted order of their Y coordinates
    l = []; #initializes the new list
    i=0;j=0; 
    while(i < len(a) and j <len(b)):
        if(a[i][1] <= b[j][1]): #only works if the values are tuples
            l.append(a[i]);
            i+= 1;
            continue
        else:
            l.append(b[j]); 
            j+=1;
            continue
    #if the loop ended, either i = len(a) or j = len(b);
    while(i < len(a)):
        l.append(a[i]);
        i+=1;
    while(j < len(b)):
        l.append(b[j]);
        j+=1;
    return l;
        

    

    pass

#returns the index of the number equal to or just greater than a, if all numbers are smaller then
#returns the size of the list
def binarySearchJustGreater(a,b):
    #b is sorted, a is a tuple where the second element is the Y coordinate
    l = 0; r = len(b)-1;
    mid = math.floor((l+r)/2)
    while(l <= r):
        mid = math.floor((l+r)/2);
        if(b[mid][1] == a):
            break;
        if(l==r):
            if(b[mid][1] < a):
                mid+=1;
            break;
        if(b[mid][1] < a):
            l = mid+1;
        elif(b[mid][1] > a):
            r = mid;
    return mid;

def binarySearchJustLesser(a,b):
    #b is sorted, a is a tuple where the second element is the Y coordinate
    l = 0; r = len(b)-1;
    mid = math.floor((l+r)/2)
    while(l <= r):
        mid = math.floor((l+r)/2);
        if(b[mid][1] == a):
            break;
        if(l==r):
            if(b[mid][1] > a):
                mid-=1;
            break;
        if(b[mid][1] < a):
            l = mid+1;
        elif(b[mid][1] > a):
            r = mid;
    return mid;

class PointDatabase:
    _root = None;
    def __init__(self,pointlist):
        pointlist.sort(); #nlogn
        self._root = self.BuildTreeSortedX(pointlist);      

    def GetHeight(self):
        return self._root._height;
    def CombineLists(self,a,b):
        #now we gotta merge both of these trees somehow, so that they remain in the PointDatabase form
        #algorithm merges 2 range trees of the y component
        
        #uses the fact that both these nodes must already have sorted range trees with the Y component
        #aList = a.leafInorder(); 
        #bList = b.leafInorder(); #both of these takes O(n) time,
        
        #also, its important to consider them as ysorted, because xsorted has similar stuff and confusion 
        #would lead to errors
        return mergeLists(a,b); #takes O(n) again
        
        #then after merging we can simply build a tree on this in O(n) time as it is sorted
        return self.BuildTreeY(l);
        pass

    '''def BuildTreeY(self,s:list):
        #a similar algorithm as for the X part, but it has no Ytree
        if(len(s) == 1):
            cur = Node(s[0]);
            return cur;
        y = math.floor((len(s)+1)/2)-1; #position of median
        l = s[0:y+1];
        r = s[y+1:];
        a = Node(s[y]);
        a.setLeft(self.BuildTreeY(l));
        a.setRight(self.BuildTreeY(r));
        return a;'''

    def BuildTreeSortedX(self,s:List):
        #asusme the list is sorted, since it is sorted, I can find the median in O(1);
        #first we sort the list, then we make it into a binary search tree using recursion
        if(len(s) == 1):
            cur = Node(s[0]);
            cur.yTree = [s[0]]; #another node having the same value
            return cur;
        if(len(s) == 0):
            return None;
        x = math.floor((len(s)+1)/2)-1;
        #x is the position of the median
        l = s[0:x+1]; 
        r = s[x+1:]; 
        a = Node(s[x]); #node which has 2 children
        a.setLeft(self.BuildTreeSortedX(l)); 
        a.setRight(self.BuildTreeSortedX(r)); #works in O(n)
        a.yTree = self.CombineLists(a._left.yTree,a._right.yTree);
        return a;

    def searchNearby(self,q,d):
        return self.QueryRangeX(q[0]-d,q[0]+d,q[1]-d,q[1]+d,self._root);
        pass
    
    def QueryRangeY(self,y1,y2,l):
        # l = curNode.yTree; #the sorted list of the y points
        #binary search for y1, or a the least point larger than y1 in this list,
        #basically a lowerbound
        b = binarySearchJustLesser(y2,l);
        a = binarySearchJustGreater(y1,l);
        #from index a to be, we should include all of these.
        if(a >= len(l) or b <= -1): #then range doesn't lie here
            return [];
        return l[a:b+1]; #returns the correct list of the points
        pass


    def QueryRangeX(self,x1,x2,y1,y2,curNode:Node):
        #x1 is the start of x, x2 is the end of x
        #y1 is the start of y, y2 is the end of y
        while(curNode._value[0] > x2):
            #then its value is greater than both, a[0] and a[1], hence we go to its left
            curNode = curNode._left;
        while(curNode._value[0] < x1):
            #then its smaller than both of them, so we go to the right
            curNode = curNode._right;
        #after both of these while loops, we arrive at a place where 
        # a[0] <= curNode._value[0] <= a[1]
        #hence from here
        l = self.findLesser(x2,y1,y2,curNode._right);
        l.extend(self.findGreater(x1,y1,y2,curNode._left));
        return l;
        pass
    
    def findGreater(self,x1,y1,y2,curNode:Node):
        l = [];
        #if it is a leaf node
        if(curNode._height == 1): 
            if(curNode._value[0] >= x1 and curNode._value[1] >= y1 and curNode._value[1] <= y2):
                return [curNode._value];
            else:
                return [];
        if(curNode._value[0] >= x1):
            l.extend(self.QueryRangeY(y1,y2,curNode._right.yTree)); #all nodes on its right would be greater than it afterall
            #and then check the right side
            l.extend(self.findGreater(x1,y1,y2,curNode._left)); 
            return l; #done
        else:
            #then all values to its left would be lesser than x1, hence no point checking there
            l.extend(self.findGreater(x1,y1,y2,curNode._right));
            return l;

    def findLesser(self,x2,y1,y2,curNode:Node):
        l = [];
        #if it is a leaf node
        if(curNode._height == 1): 
            if(curNode._value[0] <= x2 and curNode._value[1] >= y1 and curNode._value[1] <= y2):
                return [curNode._value];
            else:
                return [];
        if(curNode._value[0] <= x2):
            l.extend(self.QueryRangeY(y1,y2,curNode._left.yTree));
            #and then check the right side
            l.extend(self.findLesser(x2,y1,y2,curNode._right)); 
            return l; #done
        else:
            #then all values to its right would be greater than x2, hence no point checking there
            l.extend(self.findLesser(x2,y1,y2,curNode._left));
            return l;

        #wrote functions below for 1D query trees as practice, although 2d has similar
    '''def findLesser(self,x2,curNode:Node):
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
        return self.__Query(x1,x2,self._root);'''

# l = [(3,2),(4,5),(5,9),(9,13),(2,15),(2,17)];  

a = PointDatabase([]); 
# # print(a._root.yTree);
# # print(a._root.leafInorder());
# # b = [(3,2),(4,5)];
# # c = [(4,3),(9,10)];
# # k = mergeLists(c,b);
# # for j in k:
# #     print(j); #MergeLists is working
# c = a.QueryRangeX(1,10,1,14,a._root);
# print(c);
