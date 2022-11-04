a = input();
b = input();
 
 
def kmp(a,b):
    #a is the string, and b is the pattern
    #returns the list of starting indices where the pattern b matches with a
    #the utility function of the string b(can be made using kmp(b,$+b[1:]))
    utilityFunction = ComputeUtility(b) 
    m = len(b); n = len(a);
    #assuming we are not finding the utility function rn and its already made
    #we check for the string at
    answer = []; 
    i = 0; j = 0; 
    # while(i < n-m+1):
    #     if(a[i] == b[j]):
    #         i+=1; j+=1; #added 1 to both
    #         if(j == len(b)):
    #             answer.append(i-len(b));
    #             j -= (m - utilityFunction[m-1]);
    #             i+=1;
    #         continue; 
    #     else:
    #         if(j == 0):
    #             i+=1; j+=1; 
    #             continue; 
    #         #we shift the current string, by how much?, by the length of b - utlity[j]
    #         #we accomplish this shift by shifting the value of j, while keeping i constant
    #         j -= m - utilityFunction[j-1] + 1;
    #         #the utilityfunction[j] stores the length of the longest proper suffix of b[0:j+1]
    #         #that is a prefix of b, hence we must restore j to utilityFunction[j]+1;
 
    #i is the current position in a to be checked, and j is current position in b to be compared to
    while(i < n):
        #print(i,j, a[i] == b[j]);
        if(a[i] == b[j]):
            i+=1; 
            j+=1;
            #print("a[i] = a[j] at ",i,j);
            if(j == m):
                answer.append(i-m); #the location of the correct match
                j = utilityFunction[m-1]; 
                #relocates j to the position to be checked with
        else:
            if(j == 0):
                i+=1; #j += 1; 
                continue; 
        #we shift the current string by the length of b - utility[j-1];
        #we can do this by simply changing j and i
            j = utilityFunction[j-1]; #simple case
        #i should remain same by simple argumen, we must always increase i by only 1
    return answer;
 
def generateUtilityFunction(b):
    #a = b;
    a = '$' + b[1:];
    m = len(b); n = len(a);
    #assuming we are not finding the utility function rn and its already made
    #we check for the string at
    answer = []; 
    utilityFunction = [0]*m;
    i = 0; j = 0; 
    # while(i < n-m+1):
    #     if(a[i] == b[j]):
    #         i+=1; j+=1; #added 1 to both
    #         if(j == len(b)):
    #             answer.append(i-len(b));
    #             j -= (m - utilityFunction[m-1]);
    #             i+=1;
    #         continue; 
    #     else:
    #         if(j == 0):
    #             i+=1; j+=1; 
    #             continue; 
    #         #we shift the current string, by how much?, by the length of b - utlity[j]
    #         #we accomplish this shift by shifting the value of j, while keeping i constant
    #         j -= m - utilityFunction[j-1] + 1;
    #         #the utilityfunction[j] stores the length of the longest proper suffix of b[0:j+1]
    #         #that is a prefix of b, hence we must restore j to utilityFunction[j]+1;
 
    #i is the current position in a to be checked, and j is current position in b to be compared to
    i = 1;
    while(i < n):
        #print(i,j, a[i] == b[j]);
        if(a[i] == b[j]):
            i+=1; 
            j+=1;
            if(i != n):
                utilityFunction[i] = utilityFunction[i-1] + 1;
            #print("a[i] = a[j] at ",i,j);
            if(j == m):
                answer.append(i-m); #the location of the correct match
                j = utilityFunction[m-1]; 
                #relocates j to the position to be checked with
            
                
        else:
            if(j == 0):
                i+=1; #j += 1;
                #utilityFunction[i] += 99;
                utilityFunction[i] = 1;
                print(i,j);
                continue; 
        #we shift the current string by the length of b - utility[j-1];
        #we can do this by simply changing j and i
            j = utilityFunction[j-1]; #simple case
            while(a[i] != a[j]):
                j = utilityFunction[j-1];
                if(j == 0):
                    break;
            utilityFunction[i+1] = j; 
            
        #i should remain same by simple argumen, we must always increase i by only 1
    print(a);
    print(b);
    return utilityFunction;
 
def ComputeUtility(b):
    m = len(b);
    h = [0]*m;
    a = '$' + b[1:];
    #now we try to match these
    i = 1; j = 0; #i is pointer to a's location, b is pointer to b's location
    #for the ith one, assume we know h(0),h(1)....h(i-1);
    #therefore we know that at i-1, h(i-1) characters have been matched, therefore
    while(i < m):
        if(a[i] == b[j]):
            if(i != 0):
                h[i] = h[i-1]+1; #simply assigned the value then go to the next i
            i+=1; j+=1;
            continue; #computed this value so we go to the next iteration
        else:
            #now if we do not have a match, then we must shift the pattern by m-h(i-1)
            #so currently a[i] != b[j];
            #next shift needs to be by m-h[i-1], therefore j would become h[i-1];
            if(j == 0):
                h[i] = 0;
                i+=1;
                continue;
            while(a[i] != b[j]  and j != 0):
                j = h[j-1];
            #now either j = 0, or a[i] = b[j];
            if(j == 0):
                if(a[i] != b[j]):
                    h[i] = 0; 
                else:
                    h[i] = 1;
                    j+=1;
                i+=1;
                continue;
            #if j not 0;
            else:
                h[i] = h[j-1]+1;
                i+=1;
            #now we check for the pattern matching again, which is done in the next iteration
            #but we might encounter a loop for the starting character of a, since it does not match
            #
            # if(a[i] == b[j]):
            #     #if it matches, then nice, we just make it equal to
            #     h[i] =  
    return h;
 
# l = kmp("abaababaabacabaababaab","abaaba");
# k = kmp("saippuakauppias","pp")
# #print(l); print(len("abaababaabacabaababaaba"));
# #print(generateUtilityFunction("abaaba"));
# print(l,k);
print(len(kmp(a,b)));