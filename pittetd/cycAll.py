# shifts f(A) to f(A^k), k > 0
def cycShift(f, k):

    if (k <= 0) or len(f) <= 0:
        return
    if (k == 1):
        return f

    L = len(f)
    g = [0] * L

    for i in xrange(L):
        g[(i*k) % L] += f[i]

    return g
    

# multiplies two f's
def multCyc(f, g):

    if len(f) != len(g):
        return

    L = len(f)
    res = [0] * L

    for i in xrange(L):
        for j in xrange(L):
            res[(i+j) %L] += (g[i] * f[j])

    return res

# add two f's
def addCyc(f, g):
    
    if len(f) != len(g):
        return

    L = len(f)
    res = [0] * L

    for i in xrange(L):
        res[i] = g[i] + f[i]

    return res

# compute norm of f(A)
def cycNorm(f):

    L = len(f)

    if L <= 1:
        return
    
    res = [i for i in f] # deep copy of f

    # create f(A^k)
    for k in xrange(2,L):
        fk = cycShift(f, k)
        res = multCyc(res, fk)

    for k in xrange(3,L):
        if res[k] != res[k-1]:
            return

    return res[0] - res[1]

import sys

# the following two functions are used to generate primitive roots
# translated to Python from http://www.bluetulip.org/2014/programs/primitive.js
# (some rights may remain with the author of the above javascript code)

def isNotPrime(possible):
    i = 2
    while i <= possible**0.5:
        if (possible % i) == 0:
            return True
        i = i + 1
    return False

def primRoots(theNum):
    if isNotPrime(theNum):
        raise ValueError("Sorry, the number must be prime.")
    o = 1
    roots = []
    r = 2
    while r < theNum:
        k = pow(r, o, theNum)
        while (k > 1):
            o = o + 1
            k = (k * r) % theNum
        if o == (theNum - 1):
            roots.append(r)
        o = 1
        r = r + 1
    return roots
    min_tot = 2 + (L-1)/2
    min_e = 2

# search a factor e of L-1 such that e+f is minimized

def searchMinE(L):
    # we know we are searching a parabola and sqrt(L-1)
    # is the minimum point thus we break once we find the closest
    # integer factor but we search backwards and forwards

    if L <= 1:
        return L

    min_tot = 2 + (L-1)/2
    min_e = 2
    
    s = int(sqrt(L-1))
    for i in xrange(s,L):
        if ((L-1)% i) == 0:
            if (i + (L-1)/i) < min_tot:
                min_e = i
                min_tot = i + (L-1)/i
            break

    for i in xrange(s,0,-1):
        if ((L-1)% i) == 0:
            if (i + (L-1)/i) < min_tot:
                min_e = i
                min_tot = i + (L-1)/i
            break

    return min_e

# funtion to do sigma conjugation
def sigmaShift(f, g, k):
    L = len(f)
    return cycShift(f, pow(g,k,L))

# compute norm of f(A) using periods
# total e + f multiplications rather than e*f
# but first you must find a primitive root so the total
# time needed might be the same
def cycNormFast(f, g, e=2):

    # Find primitive a root
    # Create the \sigma operator \alpha \to \alpha^\gamma
    # Construct G(\alpha)
    # Multiply the G(\alpha)'s

    L = len(f)
    if L <= 1:
        return
    
    #g = primRoots(L)[0]

    # for now set e = 2
    # e = 2
    F = (L-1)/e

    # now construct G
    G = [i for i in f] # deep copy of f

    for k in xrange(1,F):
        fk = sigmaShift(f, g, k*e)
        G = multCyc(G, fk)

    # now construct G
    res = [i for i in G] # deep copy of f

    for k in xrange(1,e):
        Gk = sigmaShift(G, g, k)
        res = multCyc(res, Gk)

    #print res

    for k in xrange(3,L):
        if res[k] != res[k-1]:
            return

    return res[0] - res[1]


# do division f/h
def divCyc(f, h):

    if len(f) != len(h):
        return

    L = len(f)

    if L == 1:
        return [f[0]/h[0]]

    Nh = cycNorm(h)

    res = [i for i in f] # deep copy of f
    for k in xrange(2,L):
        hk = cycShift(h, k)
        res = multCyc(res, hk)

    # check if every coefficient is the same modulo Nh
    for k in xrange(1,L):
        if (res[k] % Nh) != (res[k-1] % Nh):
            return

    # now subtract the higest coefficient from each coefficient and divide by Nh
    for k in xrange(L):
        res[k] = (res[k] - res[-1])/Nh

    return res

# find factors of a number to be used for generating periods
from math import sqrt
def factors(n):    # (cf. https://stackoverflow.com/a/15703327/849891)
    j = 2
    while n > 1:
        for i in xrange(j, int(sqrt(n+0.05)) + 1):
            if n % i == 0:
                n /= i ; j = i
                yield i
                break
        else:
            if n > 1:
                yield n; break
        
# calculate prime factor for primes that divide a binomial
def binPrimeFactor(L, p):
    if (p-1) % L != 0:
        return

    w = (p-1) / L
    k = pow(2, w, p)

    # calculate all powers of k
    kp = [pow(k, i, p) for i in xrange(L)]

    # calculate all g(\alpha) made of two powers of k
    # there are four possibilities with plus minus for each

    # prepare things for cycNormFast
    g = primRoots(L)[0]

    # this part is to find e and f that minimizes e + f
    # so that we minimize the number of multiplication
    # in the cycNormFast function
    
    min_e = searchMinE(L)
    print min_e

    # now we generate all combos for powers of k
    import itertools
    t = [i for i in range(1,L)]
    for u in xrange(2,L):
        
        l = itertools.combinations(t, u)

        for i in l:
            # create a bitmap for the plus minus
            for k in range(0,2**u):
                res = [0] * L
                for j in range(u):
                    b = pow(-1,(k >> j) & 0x01)
                    res[i[j]] = b*1
                    res[0] -= b*kp[i[j]]
                N = cycNormFast(f=res, g=g, e=min_e)
                if N == p:
                    print N, res, u

def findSquarePrime(L, a, p):
    
    hl = (((L-1)/2) + 1)
    kp = [1] * hl
    for i in xrange(1,hl):
        kp[i] = (pow(a,i,p) + pow(a,L-i,p)) % p

    print kp

    g = primRoots(L)[0]
    min_e = searchMinE(L)
    
    import itertools
    t = [i for i in range(1,hl)]
    
    for u in xrange(2,hl):
        
        l = itertools.combinations(t, u)

        for i in l:
            # create a bitmap for the plus minus
            for k in range(0,2**u):
                res = [0] * L
                for j in range(u):
                    b = pow(-1,(k >> j) & 0x01)
                    res[i[j]] = b*1
                    res[L-i[j]] = b*1
                    res[0] -= 2*b*kp[i[j]]
                N = cycNormFast(f=res, g=g, e=min_e)
                if N == p**2:
                    print N, res, u



# calcule f(k) mod p given f(\alpha)
def calcFK(f, k, p):
    L = len(f)

    res = 0
    for i in range(L):
        res += f[i]*pow(k,i,p)

    return res % p

# find if a conjugate of f(\alpha) satisfies f(k) \equiv 0 \pmod{p}
def findConjWithCorrectK(f, k, p):

    L = len(f)
    for i in xrange(1, L):
        if calcFK(cycShift(f, i), k, p) == 0:
            print i






        
