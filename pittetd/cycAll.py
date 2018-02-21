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

def sigmaShift(f, g, k):
    L = len(f)
    return cycShift(f, pow(g,k,L))

# compute norm of f(A) using periods
# total e + f multiplications rather than e*f
# but first you must find a primitive root so the total
# time needed might be the same
def cycNormFast(f, g):

    # Find primitive a root
    # Create the \sigma operator \alpha \to \alpha^\gamma
    # Construct G(\alpha)
    # Multiply the G(\alpha)'s

    L = len(f)
    if L <= 1:
        return
    
    #g = primRoots(L)[0]

    # for now set e = 2
    e = 2
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

# calculate prime factor
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
    
    import itertools
    t = [i for i in range(1,L)]
    for u in xrange(2,L):
        
        l = list(itertools.combinations(t, u))

        for i in l:
            # create a bitmap for the plus minus
            for k in range(0,2**u):
                res = [0] * L
                for j in range(u):
                    b = (k >> j) & 0x01
                    if b == 0:
                        b = -1
                    res[i[j]] = b*1
                    res[0] -= b*kp[i[j]]
                N = cycNormFast(res, g)
                if N == p:
                    print N, res, u



    
