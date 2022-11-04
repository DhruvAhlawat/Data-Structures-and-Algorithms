from pdb import pm
import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	#so let number of primes that divide f(p') - f(p) be k.
	#then clearly k <= log2(f(p') - f(p)), according to the formula given.
	#also we know that f(p') - f(p) <= 26^m - 1
	#therefore, k <= m*log2(26)
	#also, if q was chosen to be any of these k primes, only then will there be an erroneus matching
	#therefore probability = k/pi(N) <= m*log2(26)/pi(N), combining this with pi(N) >= N/log2(N),
	#we get N/log2(N) >= 2mlog2(26)/epsilon
	# Just gotta solve this via an approximation or some inequality
	#so let the rhs be c.

	#then its obvious that any constant multiple of c would not work for N, as log(N) would grow beyong this multiple
	#at a particular N. But we also know that space complexity must be of O(log(m/eps)) so O(log(c))
	#therefore a good slower growing inequality, we can find an N such that
	#N = t*log(t), where t is a linear function of c (the right hand side)
	
	#we get that t*log(t)/(log(t)+loglog(t)) >= c.
	#now using the graphing software Desmos, 
	#I found that loglog(t) <= 0.54*log(t) for all values of t greater than 1, when the base of all logs is 2
	#although for safety, I will take a multiple of 0.6 instead of 0.54

	#then we have that the LHS, t*log(t)/(log(t) + loglog(t)) >= t*log(t)/(log(t) + 0.6*log(t)) >= t/1.6
	#therefore we have N >= t/1.6, and if we just set t/1.6 >= c, we get t as 1.6*c.

	#therefore 1.6*c*log(1.6*c) >= c, where c is 2*m*log(26)/eps
	right = 2*m*math.log2(26)/eps;
	N = math.ceil(1.6*right*math.log2(1.6*right));
	#and hence we get a good approximation for N, with the error's upper bound less than eps
	#also the space complexity of N is still O(m/eps) so thats fine
	return N;
def intValue(a):
	return ord(a)-ord('a'); #returns the integer equivalent of the character
def binaryExponentiation(n,mod,a=26):
	if(n == 0):
		return 1;
	if(n%2 == 0):
		k = binaryExponentiation(n//2,mod,a)%mod;
		return (k*k)%mod;
	else:
		return a*binaryExponentiation(n-1,mod,a)%mod;
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	n = len(x); m = len(p); #uses log(n) + log(m) memory
	#calculate the modular value of the 26-ary number
	if(m > n):
		return [];
	curMod = 0; pMod = 0;
	pow26 = 1;
	for i in range(m-1,-1,-1): #the pMod value stores the value of the hash for the pattern
		pMod += (pow26*(intValue(p[i])%q))%q;
		pMod %= q;
		pow26 = (pow26*(26%q))%q; #calculates the next power

	pow26 = 1;
	for i in range(m-1,-1,-1): 
		curMod += (pow26*(intValue(x[i])%q))%q;
		curMod %= q;
		pow26 = (pow26*(26%q))%q; #calculates the next power
		
	#now we have the current value of the hash starting at the index i = 0, ending at index m-1
	#and we can shift this around by simply subtracting the top value*26^(m-1) and multiplying by 26 and adding the next value
	L = [];

	storedPow = binaryExponentiation(m-1,q); #storing this value as we will need it repeatedly
	#stores (26^(m-1))%q
	for i in range(0,n-m+1):
		if(curMod%q == pMod):
			L.append(i);
		#now we update curMod
		if(i+m == n):
			break;
		curMod -= (intValue(x[i])*storedPow)%q; #the first digit has been removed
		curMod %= q;
		curMod = (curMod*26)%q;
		curMod += intValue(x[i+m]);
		curMod %= q; #now the next hash has been formed
	
	return L;

#print(modPatternMatch(1000000007, "DE", "ABCDEDE"));

# Return sorted list of starting indices where p matches x
#I believe the below implementation is also correct,
#where I have skipped the '?' character and therefore only matched m-1 characters, 
#using powers of 26 only uptill m-2, instead of m-1 like before.
#I commented this part out because unlike what the assignment mentions that we must figure out a
#definition for f ourselves, the autograder is marking things deterministically, like
#theres only one correct implementation of f, which is probably wrong.

def modPatternMatchWildcard(q,p,x):
	n = len(x); m = len(p);
	L = []; #the list to store the indices
	if(m > n):
		return L; #obviously
	if(m == 1):
		#that means only one character is present and it must be "?".
		for i in range (0,n):
			L.append(i);
		return L; #since all positions should return a match
	
	currentPow = 1;
	curMod = 0; pMod = 0; #similar to the one in modPatternMatch

	i = m-1; wildCardPos = 0;
	while(i >= 0):
		if(p[i] == '?'):
			wildCardPos = i;
			currentPow = (currentPow*26)%q;
			i-=1;
			continue; #skips the wildcard element from adding to the pMod, but does increment the power
		#else we add it to the pMod like normal
		pMod += (intValue(p[i])*currentPow)%q; #the hash of the current character
		pMod %= q; 
		currentPow = (currentPow*26)%q; #the power for the next digit
		i-=1; 
	#now pMod has been created and it shall be constant 

	#creating the starting hash
	i = m-1; #reseting i
	currentPow = 1; #reset
	while(i >= 0):
		if(wildCardPos == i):
			currentPow = (currentPow*26)%q; 
			i-=1; 
			continue; 
		
		curMod += (intValue(x[i])*currentPow)%q; 
		curMod %= q; #so the value stays below q
		currentPow = (currentPow*26)%q; 
		i-=1; 
	#now curMod has been made for the string starting from x[0] and ending at x[m-1]
	#then we shift this match one by one and calculate the hash

	# if(pMod == curMod):
	# 	L.append(0);
	
	i = 0; #resetting 0 again
	pow26mMinus2 = binaryExponentiation(m-2,q); #default power is 26
	pow26mMinus1 = (pow26mMinus2*26)%q;
	if(wildCardPos == 0):
		#special case 1
		while(i < n):
			if(pMod == curMod):
				L.append(i); #hash matches
			if(i+m == n):
				break; #reached the end
			#then we shift the current matching to now start from i+1 
			#must delete the i+1th element, as it will become the next wildCard position
			curMod -= (pow26mMinus2*intValue(x[i+1]))%q
			curMod = (curMod*26)%q; #increasing the 26 power of each digit by 1
			curMod += intValue(x[i+m]); #the next character is inserted
			
			curMod %= q; #resetting curMod to a value between 0 and q.
			#now the hash for substring starting at x[i+1] has been generated
			i += 1; #incrementing
	elif(wildCardPos == m-1):
		#special case 2
		while(i < n):
			if(pMod == curMod):
				L.append(i);
			if(i+m == n):
				break; #reached the end
			
			curMod -= (pow26mMinus1*intValue(x[i]))%q; #removing the ith character
			curMod = (curMod*26)%q; #multiplying with 26 to increase each digit's power
			curMod += (26*intValue(x[i+m-1]))%q; #adding the now second last element, which was the wildCard before, NOT adding x[i+m] as that is the new wildCard Position
			
			curMod %= q;
			i += 1; 
	else:
		#general case where wildCard is somewhere between 0 and m-1
		wildCardPowMinus1 = binaryExponentiation(m-wildCardPos-2,q);
		wildCardPow = (wildCardPowMinus1*26)%q;
		while(i < n):
			if(pMod == curMod%q):
				L.append(i);
			if(i+m == n):
				break; #reached the end
			#now we know that wildCard isn't at the start or at the end
			#finding the next hash of substring starting at i+1

			curMod -= (pow26mMinus1*intValue(x[i]))%q; #removes the ith character
			#also the x[i+wildCard] was the current wildCard, and therefore we should add it back
			# as now its position will become wildCard -1 for the substr starting at i+1
			curMod += ((intValue(x[i+wildCardPos]))*wildCardPow)%q;
			curMod -= ((intValue(x[i+wildCardPos+1]))*wildCardPowMinus1)%q;
			curMod %= q;
			curMod = (curMod*26)%q;
			#now add the last new position
			curMod += (intValue(x[i+m]));

			curMod %= q; #reModuloing i t
			i+=1;
	
	#then we shift


	#function assumes
	return L;

print(findN(0.01,20));
