'''is used for defining the ordering of the priority Queue'''

def CompareValues(a,b): # Comparator definition
    if(a[0] ==None and b[0] != None):
        return True;
    elif(a[0] != None and b[0] == None):
        return False;
    elif(a[0] == None and b[0] == None):
        return a[1] > b[1];
    elif(a[0] == b[0]):
        return a[1] > b[1];
    else:
        return a[0] > b[0];
    # if(a>b):
    #     return True;
    # else:
    #     return False;

def ExchangeValues(l,i,j):
    temp = l[i];
    l[i] = l[j];
    l[j] = temp;

def UpdateValues(timeOfUpdation,x,v,i,T,lastUpdateList):
    # ogTime = collisionDetailsOriginal[0];
    # timeDifference = ogTime - timeOfUpdation;
    # x[i] = collisionDetailsOriginal[2] - v[i]*timeDifference;

    timeDifference = timeOfUpdation - lastUpdateList[i];
    x[i] = x[i] + v[i]*timeDifference;
    lastUpdateList[i] = timeOfUpdation;
    if(v[i+1] != v[i]):
        newTimeToCollide = (x[i]-x[i+1])/(v[i+1]-v[i]);
    else:
        newTimeToCollide = T+1;
    newPosToCollide = x[i] + v[i]*newTimeToCollide;
    if(newTimeToCollide > 0):
        return (timeOfUpdation+newTimeToCollide,i,newPosToCollide);
    else:
        return (T+2,i,newPosToCollide);


class PriorityQueue: #Uses Heap, (min or max depends on the Compare function) #stores tuples
    
    Representation = []; #uses a representation list to store the values of the almost complete binaryTree or Heap
    locationStore = []; #ith element stores the location of the ith particles collision details in the RepresentationList.

    #size = 0;
    def __init__(self,l = []) -> None:
        if(len(l) == 0):
            self.Representation = [];
        else:
            self.BuildHeap(l);
        pass
    def getParentIndex(self,u):
        return (int((u-1)//2));
    def getRightChildIndex(self,u):
        return 2*u+2;
    def getLeftChildIndex(self,u):
        return 2*u+1;
    def getParentValue(self,u):
        return self.Representation[int((u-1)//2)];
    
    def __len__(self):
        return len(self.Representation);
    
    def HeapUp(self,u):
        #so u is the position of this particular node in the Representation List.
        #gotta heapUp.
        if(u == 0):
            return u;
        while(CompareValues(self.getParentValue(u),self.Representation[u])):

            p = self.getParentValue(u); #stores the value of the parent of the element
            cur = self.Representation[u]; #stores the value of the element
            #if the parent p is not <= cur, then we exchange their positions.

            ExchangeValues(self.locationStore,p[1],cur[1]); 

            self.Representation[self.getParentIndex(u)] = cur;
            self.Representation[u] = p;
            u = self.getParentIndex(u); 
            #changed u to correspond to its correct location after exchanging.
            if(u <= 0): #if we reached the top of the Heap, we break.
                return u;
        return u;
    #now that HeapUp is defined, we can make a system to enqueue.
    def Enqueue(self,x):
        #pos = self.size;
        self.Representation.append(x);
        pos = len(self.Representation) - 1; #the position of the appended item(the new element x);
        if(pos > 0):
            self.HeapUp(pos);


    def BuildHeap(self,l):
        n = len(l);
        self.Representation = [0]*n;
        self.locationStore = [0]*n; 
        for i in range(n-1,-1,-1):
            self.Representation[i] = l[i];
            self.locationStore[l[i][1]] = i; #considering the second element of the l[i] to be the index of the particle
            self.HeapDown(i);
            #simple O(n) implementation of Fast BuildHeap using HeapDown.

    def HeapDown(self,u): #a recursive function which heaps down the uth node to its correct location
        c1 = 2*u + 1;
        c2 = 2*u + 2;
        if(len(self.Representation) > c2):
            cmin = c2 if CompareValues(self.Representation[c1],self.Representation[c2]) else c1; #cmin is the index of the minimum child,
            #if both children have equal values, we return c1;
        elif(len(self.Representation) == c2):
            #only one child exists, in this case, we do the same thing    
            cmin = c1;
        else:
            #else, no child exists of the current node, hence we cannot heap it down further, so we return.
            return u;
        if(CompareValues(self.Representation[u],self.Representation[cmin])):# if uth element is greater than its children.
            # temp = self.Representation[u];
            # self.Representation[u] = self.Representation[cmin];
            # self.Representation[cmin] = temp; #exchange values of the child and the parent, so the new parent is smaller than its children
            ExchangeValues(self.locationStore,self.Representation[u][1],self.Representation[cmin][1]); #exchanges values of their location store as well
            ExchangeValues(self.Representation,u,cmin);
            u = cmin;#new location of the current node. Also gotta HeapDown on this one again.
            return self.HeapDown(u); #heaps down again, only if we changed its position in this recursion.
        else:
            return u;
    
    #with HeapDown done, we can define an extract min
    def GetCollisionIndex(self,i):
        return self.locationStore[i];
    def GetRoot(self):
        return self.Representation[0];
    def ExtractRoot(self):
        m = self.Representation[0];
        lastPos = len(self.Representation)-1;
        self.Representation[0] = self.Representation[lastPos]; #brings the last node to the top.
        self.Representation.pop();
        self.HeapDown(0); #then we heap it down to its correct location.

        return m; #then we return the minimum value    


#now making the Actual assignment stuff.
def finalVelocities(v1,v2,m1,m2):
    v1f = (v1*(m1-m2) + 2*m2*v2)/(m1+m2);
    v2f = (v2*(m2-m1) + 2*m1*v1)/(m1+m2);
    return (v1f,v2f); #returns a tuple of the final velocities of both the elastic colliding objects

globalTime = 0;

def listCollisions(M,x,v,m,T):
    n = len(M); #number of colliders, or particles
    L = [];
    lastUpdate = [0]*n;
    for i in range(0,n-1):
        if(v[i+1] == v[i] or (x[i]-x[i+1])/(v[i+1]-v[i]) <= 0):
            timeToCollide = None;
            xpos = None;
        else:
            timeToCollide = (x[i]-x[i+1])/(v[i+1]-v[i]);
            xpos = x[i] + timeToCollide*v[i];
        
        L.append((timeToCollide,i,xpos)); #the last number is the time of its last update
    col = PriorityQueue(L);
    #with that the initial priority queue of the collisions col has been created.
    L = []; #now L is the list that stores the collision details in order
    counter = 0;
    while(counter < m):
        counter += 1;
        top = col.GetRoot();

        if(top[0] == None): #no more further collisions possible.
            break;
        if(top[0] > T):
            break;
        L.append((round(top[0],4),top[1],round(top[2],4))); 
        cur = top[1];
        #we update x and v of the current objects.
        x[cur] = top[2]; x[cur+1] = top[2];
        newVelocities = finalVelocities(v[cur],v[cur+1],M[cur],M[cur+1]);
        v[cur] = newVelocities[0]; v[cur+1] = newVelocities[1];
        lastUpdate[cur] = top[0]; lastUpdate[cur+1] = top[0];

        col.Representation[0] = (None,cur,None); #will update its location in the Priority queue later
        col.HeapUp(col.HeapDown(0));
        #now we need to update the positions of the object at cur+2 and cur-1;
        if(cur >= 1):
            #we need to update location of the cur-1 th particle and then recalculate its collision time.
            x[cur-1] = x[cur-1] + v[cur-1]*(top[0] - lastUpdate[cur-1]); #position successfully updated.
            lastUpdate[cur-1] = top[0];
            #time to collide now becomes.
            if(v[cur-1] == v[cur]):
                newCollisionTime = None;
                newHitPoint = None;
            elif((x[cur] - x[cur-1])/(v[cur-1]-v[cur]) < 0):
                newCollisionTime = None;
                newHitPoint = None;
            else:
                newCollisionTime = (x[cur] - x[cur-1])/(v[cur-1]-v[cur]);
                newHitPoint = x[cur] + newCollisionTime*v[cur];

            #now we update these changes in the priority queue.
            #how do we do that exactly? By using the locationStore ofcourse.
            if(newCollisionTime == None):
                actualCollisionTime = None;
            else:
                actualCollisionTime = top[0] + newCollisionTime;
            prev = col.locationStore[cur-1];
            col.Representation[prev] = (actualCollisionTime,cur-1,newHitPoint); #updated its value.
            col.HeapUp(col.HeapDown(col.locationStore[cur-1]));

        if(cur < n-2):
            #here, we update the position of the cur+2 particle and then recalculate collision of cur+1 and cur+2;
            x[cur+2] = x[cur+2] + v[cur+2]*(top[0] - lastUpdate[cur+2]); #position successfully updated.
            lastUpdate[cur+2] = top[0];
            #time to collide now becomes.
            if(v[cur+2] == v[cur+1]):
                newCollisionTime = None;
                newHitPoint = None;
            elif((x[cur+2] - x[cur+1])/(v[cur+1]-v[cur+2]) < 0):
                newCollisionTime = None;
                newHitPoint = None;
            else:
                newCollisionTime = (x[cur+2] - x[cur+1])/(v[cur+1]-v[cur+2]);
                newHitPoint = x[cur+2] + newCollisionTime*v[cur+2];
            if(newCollisionTime == None):
                actualCollisionTime = None;
            else:
                actualCollisionTime = top[0] + newCollisionTime;
            ahead = col.locationStore[cur+1];
            col.Representation[ahead] = (actualCollisionTime,cur+1,newHitPoint);
            col.HeapUp(col.HeapDown(col.locationStore[cur+1]));
        
        #now we put the 3 of these into their correct positions within the Priority Queue.
        #col.HeapUp(col.HeapDown(0)); #putting the minimum node in its correct position.
        # col.HeapUp(col.HeapDown(col.locationStore[cur-1]));
        # col.HeapUp(col.HeapDown(col.locationStore[cur+1]));

        #then onto the next iteration of the loop.

    return L;
        
        

#testing statements


# a.BuildHeap([4,1,6,2,1,10,39,3,12,5,3,2]);

#c =  listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5)  

# d = listCollisions([940.1440594570123, 342.32941684559046, 686.1000355388383, 520.8309066514597,
# 870.9632698994412, 727.2119773442081], [2.5912045650076445, 3.3979994719550377, 5.247957197003846,
# 5.383388625251065, 5.440818809376985, 6.415333653364417], [99.79672039800879, 94.19054127616612, 
# 25.977729855078213, 25.5959601276192, 31.543951443609476, 25.267596192531126], 8, 4.531827813401554);

# b = listCollisions([1,1,1,1,1],[1,2,3,4,5],[-1,-2,2,4,-1],10,10);
# print(d);
    



