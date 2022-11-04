from typing import List;

class Stack:
    
    topPos = -1; #holds the index of the top of the stack
    a = []; #the elements are stored in a Python List
    def __init__(self,initialValues:List = []) -> None: #stack defined with default initial state as empty
        self.a = initialValues;
        self.topPos = len(initialValues)-1; #assigns the topPos value as
    
    def __len__(self):
        return (self.topPos+1);
    def isEmpty(self):
        return (self.topPos == -1);
    def pop(self):
        if(self.topPos != -1): 
            self.topPos -= 1;#decrements topPos so it is now the index of the just previous element in the stack, and we are calling it the topmost positinon now
                                #so effectively, the previous value at topPos has been removed from the stack.
            return self.a[self.topPos+1]; #also returns the element that was popped 

    def push(self, value):
        if(self.topPos == len(self.a)-1):
        #if the topPos is already at the top of the Python list, we should double its size.
            if(len(self.a) > 0):
                b = [None]*(2*len(self.a)); #creates a new list b with a size of twice the original list used to store the stack
            else:
                b = [None]; #creates a list of size 1 if initital size was 0
            for i in range(0,self.topPos+1):
                b[i] = self.a[i];   #copying the elements from a to b
            self.a = b; #assigning b to a;
            self.topPos += 1; 
            self.a[self.topPos] = value; #finally, we push this new value onto the stack.
        else:
            self.topPos += 1; #if list to store is big enough, simply increment topPos then add this value at that index, so it becomes the new top of the stack
            self.a[self.topPos] = value;
    
    def top(self):
        ba = self.a[self.topPos]; #returns the current top element
        return ba;
    
    def size(self):
        return int(self.topPos + 1); #returns the size of the stack (NOT the size of the list used to hold the stack)
