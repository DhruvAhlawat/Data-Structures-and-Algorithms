#first we make an AVL tree
def comparision(a,b): #returns if a > b
    return a._value > b._value;
def FindHeight(a):
    if(a == None):
        return 0;
    else:
        return a._height;
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
#A BST that has height proportional to log(n); Doesn't support deletions yet
class avlBST():
    _head = None;

    def __init__(self,l) -> None:
        #l is a list of tuples to be converted into an avl BST
        for i in l:
            self.insert(Node(i));
        pass


    def height(self):
        return FindHeight(self._head);
    def insert(self,a:Node):

        #a is a node
        #we want to insert a in its right position in the avl tree;
        #we start at the head then traverse to its correct location
        cur = self._head;
        if(cur == None):
            self._head = a;
            return self._head;
        while(cur._height != 0):
            #since cur is not a leaf, we can check its right and left subtrees
            if(comparision(cur,a)):
                #if cur > a
                if(cur._left == None):
                    break; #arrived at the location to insert the new node
                cur = cur._left; 
            else:
                if(cur._right == None):
                    break; #we have arrived at the location to insert the new node
                cur = cur._right;
            
        #now we compare values with cur again, and set it at the appropriate place
        if(comparision(cur,a)):
            cur.setLeft(a);
        else:
            cur.setRight(a);

        #now we check if each of its parents are balanced or not
        b = a;
        a = a._parent;
        while(a is not None):
            if(a.isBalanced() == False):
                if(a == self._head):
                    self._head = a.ReBalance();
                    #print("needs rebalancing at root ",a._value,b._value);
                    #this case needs extra attention because its annoyingly not working
                    #with the original simple ReBalance method
                    # if(FindHeight(a._left) > FindHeight(a._right)+1):
                    #     newRoot = a._left;
                    #     l = newRoot._left;
                    #     r = newRoot._right;
                    #     if(FindHeight(l) >= FindHeight(r)):
                    #         #then we simply right rotate at root;
                    #         pass 
                    pass
                else:
                    a.ReBalance();
                    #print("needs rebalancing at ",a._value,b._value);
                break;
            a = a._parent;
                    



    def inorder(self):
        return self._head.inorder([]);



t = [];
for i in range(45,0,-1):
    t.append(i);
l = avlBST(t);
print(l.height());
print(l.inorder());
