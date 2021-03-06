from sympy import *

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




def findMe():
    for a in xrange(1,30):
        for b in xrange(a):
            t = a**2 - a*b + 3*(b**2)
            if (t) > 0:
                u = factors(t)
                prev = 0
                for i in u:
                    if i != prev:
                        prev = i
                        if i % 5 > 1:
                            print a, b, t, i

        
def Problem3(L):
    g = primRoots(L)[0]
    e = 2
    f = (L-1)/e

    t = [0] * L

    for i in xrange(f):
        t[pow(g,i*e,L)] = 1

    for i in xrange(f):
        t[pow(g,(i*e) + 1,L)] = -1

    res = multCyc(t,t)
    return res[0] - res[1]

def Problem5(L):
    g = primRoots(L)[0]
    e = 2
    f = (L-1)/e

    t = [0] * L

    for i in xrange(f):
        t[pow(g,i*e,L)] = 1

    for i in xrange(f):
        t[pow(g,(i*e) + 1,L)] = 1

    res = multCyc(t,t)
    return res[0] - res[1]


def EE(L):
    g = primRoots(L)[0]
    t0 = [pow(g,2*i,L) for i in xrange((L-1)/2)]
    t1 = [pow(g,2*i + 1,L) for i in xrange((L-1)/2)]

    c = [0,0,0]
    indv = [(i*2) % L for i in t0]

    try:
        b = indv.index(t0[0])
        c[0] += 1
    except ValueError:
        c[1] += 1

    res = []
    for i in xrange(len(t0)-1):
        for j in xrange(i+1,len(t0)):
            res.append((t0[i]+t0[j]) % L)

    print 't0', t0
    print 't1', t1
    print 'indv', indv
    print 'res', res
    
    # count t0, t1 and 0
    a = [t0[0], t1[0], 0]
    
    j = 0

    for i in a:
        s = 0
        while 1:
            try:
                b = res[s:].index(i)
                s += b + 1
                c[j] += 2
            except ValueError:
                break
        j += 1

    print c
    
    return t0, t1, indv, res


def pF(n):
    a = factors(n)

    for i in a:
        print i,

    print 

def generateEtas(L, f, v=False):
    e = (L-1)/f

    # create eta's
    g = primRoots(L)[0]

    eta = [[0] * L for i in xrange(e)]

    for i in xrange(e):
        for j in xrange(f):
            eta[i][pow(g,j*e+i,L)] = 1
        if v == True:
            print u'\u03B7%d =' % (i), eta[i]

    return eta

def generateEtag(L, f, c):
    e = (L-1)/f

    # create eta's
    g = primRoots(L)[c]

    eta = [[0] * L for i in xrange(e)]

    for i in xrange(e):
        for j in xrange(f):
            eta[i][pow(g,j*e+i,L)] = 1

        print u'\u03B7%d =' % (i), eta[i]

    return eta

def findEtaNz(eta):

    e = len(eta)
    L = len(eta[0])

    nz = [0] * e
    
    for i in xrange(e):
        for j in xrange(L):
            if eta[i][j] != 0:
                nz[i] = j
                break

    return nz

# function to print sums of eta's
def printSumEtaRaw(res, nz):
    e = len(nz)
    m = 0
    for j in xrange(e):
        if res[nz[j]] != 0:
            if res[nz[j]] < 0:
                print '-'
            elif m > 0:
                print '+',
            print u'%d*\u03B7%d' % (abs(res[nz[j]]), j),
            m += 1


    if res[0] < 0:
        print '-', abs(res[0])
    elif res[0] > 0:
        print '+', abs(res[0])
    else:
        print

# function to prepare linear algebra matrix
def findCoeff(res, nz, i, u0):
    const = -res[0]
    const -= res[nz[0]]*u0

    e = len(nz)
    coeff = [0]*(e - 1)

    for j in xrange(1,e):
        if res[nz[j]] != 0:
            coeff[j-1] = -res[nz[j]]

    coeff[i - 1] += u0

    return coeff, const


# function to find all u_i for all \eta_i
def findAllUs(L, p):
    f = findOrder(L, p)
    e = (L - 1)/f

    eta = generateEtas(L, f)
    nz = findEtaNz(eta)

    g = primRoots(L)[0]
    min_e = searchMinE(L)

    u0 = 0

    # find u0
    for i in xrange(1, p+1):
        eta[0][0] = -i
        if cycNormFast(f=eta[0], g=g, e=min_e) % p == 0:
            u0 = i
            break

    if e == 1:
        sol = {}
        u = [u0]
    else:
        eta[0][0] = 0
        coeffs = []
        consts = []
        # find the other u's
        for j in xrange(1,e):
            res = multCyc(eta[0], eta[j])

            coeff, const = findCoeff(res, nz, j, u0)
            coeffs.append(coeff)
            consts.append(const)

        # create symbol string tuple
        u = ()
        for i in xrange(1,e):
            u += ('u%d ' % i,)
        
        # create equations string tuple
        eqn = ()
        for i in xrange(0,e-1):
            eqstr = '%+d' % consts[i]
            for j in xrange(len(coeffs[i])):
                eqstr += '%+d*u%d' % (coeffs[i][j], j+1)
            eqn += (eqstr,)

        sol = solve(eqn, u)
        soln = sol.items()

        u = [0] * e
        u[0] = u0

        for i in soln:
            num = i[1].p
            den = i[1].q % p

            if den != 1:
                den = pow(den, p-2, p)
                num = (num * den)

            num = num % p

            u[int(str(i[0])[1:])] = num

    return sol, u


# print out multiplication table for periods
def multTablePeriods(L, f):

    e = (L-1)/f
    eta = generateEtas(L, f)

    # first get non zero index of each eta
    nz = findEtaNz(eta)

    # now build the multiplication table if there are e periods
    # then there are e main terms plus e(e-1)/2 cross terms

    for i in xrange(e):
        res = multCyc(eta[i], eta[i])

        print u'\u03B7%d^2 = ' % (i),
        printSumEtaRaw(res, nz)
        

    # now check for cross terms
    for i in xrange(e-1):
        for j in xrange(i+1,e):
            res = multCyc(eta[i], eta[j])

            print u'\u03B7%d*\u03B7%d = ' % (i, j),
            printSumEtaRaw(res, nz)


# find u_i corresponding to eta_i
def findU(L, p, e):

    if L == 5:
        for i in xrange(1,1000):
            if ((i*(i+1)) % p) == 1:
                u = [i, -(i+1)]
                break
    
    elif L == 13:
        u = [0] * e
        for i in xrange(100):
            if e == 4:
                if ((pow(i,4,p) + pow(i,3,p) + 2*pow(i,2,p) - 4*i + 3) % p) == 0:
                    u[0] = i
                    break
                if ((pow(-i,4,p) + pow(-i,3,p) + 2*pow(-i,2,p) - 4*(-i) + 3) % p) == 0:
                    u[0] = -i
                    break
            elif e == 3:
                if ((pow(i,3,p) + pow(i,2,p) - 4*i + 1) % p) == 0:
                    u[0] = i
                    break
                if ((pow(-i,3,p) + pow(-i,2,p) - 4*(-i) + 1) % p) == 0:
                    u[0] = -i
                    break
            elif e == 2:
                if ((pow(i,2,p) + i -3) % p) == 0:
                    u[0] = i
                    break
                if ((pow(-i,2,p) + (-i) -3) % p) == 0:
                    u[0] = -i
                    break
        print u[0]
        if e == 4:
            # find inverse of 3 mod p
            for i in xrange(1,p):
                if (i*3) % p == 1:
                    i3 = i
                    break
            else:
                i3 = 0
                
            u[2] = (i3 * (3 - 2*u[0] - pow(u[0],3,p))) % p
            u[1] = (pow(u[0],2,p) - 2*u[2]) % p
            u[3] = (-1 -u[0] - u[1] - u[2] ) % p
        elif e == 3:
            u[2] = (pow(u[0],2,p) + u[0] - 3) % p
            u[1] = (-1 - u[0] - u[2]) % p
        elif e == 2:
            u[1] = (-1 - u[0]) % p

    return u

def printEtaFactor(res):
    ln = len(res)

    for j in xrange(ln-1):
        m = 0

        print '(',
        for i in xrange(1,ln):
            if res[i] != 0:
                if res[i] < 0:
                    print '-',
                elif m > 0:
                    print '+',
                print u'%d*\u03B7%d' % (abs(res[i]), ((i-1)+j) % (ln-1)),
                m += 1
            
        if res[0] < 0:
            print '-', abs(res[0]),
        elif res[0] > 0:
            print '+', abs(res[0]),
        print ')',

    print
    

# find factors of prime numbers   
def findPrimeFactors(L, p, C=10):

    # first find order of p mod L
    for i in xrange(1,L):
        if pow(p,i,L) == 1:
            f = i
            break
    else:
        print 'p == L'
        return

    if f == L - 1 :
        print 'f is L - 1'
        return 

    print 'f', f
    e = (L-1)/f

    # create eta's

    eta = generateEtas(L, f)

    # u = findU(L,p,e)

    sol, u = findAllUs(L,p)

    for i in xrange(e):
        print 'u%d: %d,' % (i, u[i]),
    print

    g = primRoots(L)[0]
    min_e = searchMinE(L)
    
    import itertools
    t = [i for i in range(1,e+1)]


    for c in xrange(1,C+1):
        print 'c', c
        for y in xrange(1,e + 1):
            
            l = itertools.combinations(t, y)

            for i in l:
                # create a bitmap for the plus minus
                for k in range(0,2**y):
                    res = [0] * (e+1)
                    for j in range(y):
                        b = pow(-1,(k >> j) & 0x01)
                        if j == 0:
                            b *= c
                        res[i[j]] = b*1
                        res[0] -= b*u[i[j]-1]

                    cd = [0] * L
                    for j in xrange(1,len(res)):
                        et = [res[j] * z for z in eta[j-1]]
                        cd = addCyc(cd, et)
                    cd[0] = res[0]
                    N = cycNormFast(f=cd, g=g, e=min_e)

                    # we actually don't need to calculate the norm
                    # we can straight away do the verification below
                    # but this serves as a double-check

                    if N == pow(p,f):
                        print N, res
                        
                        # check result to see if we need a minus sign
                        tmp = [0] * L
                        tmp[0] = res[0]
                        for j in xrange(1,e + 1):
                            et = [res[j] * w for w in eta[j-1]]
                            tmp = addCyc(tmp, et)

                        tot = [w for w in tmp]
                        for j in xrange(1,e):
                            tmp = cycShift(tmp, g)
                            tot = multCyc(tot, tmp)

                        # check if all elements from index 1 to L-1 are the same
                        for j in xrange(2,L):
                            if tot[j] != tot[j-1]:
                                print 'Tot is not right'
                                break
                        else:
                            print tot[0] - tot[1], '=',

                        # this is just cosmetics but it's worth it
                        printEtaFactor(res)
                        

        
def printOrderList(L, n):

    # first find order of p mod L
    for i in xrange(1,n):
        if isNotPrime(i) == False:
            for j in xrange(1,L):
                if pow(i,j,L) == 1:
                    print 'p', i, 'f', j
                    break

def Page121Problem4(L):

    # first find order of p mod L
    for i in xrange(1,300):
        if isNotPrime(i) == False:
            for j in xrange(1,L):
                if pow(i,j,L) == 1:
                    print 'p', i, 'f', j
                    break

    for u in xrange(1,1000):
        if ((u*(u+1)) % 109) == 1:
            print u
            break


def Page124Problem1(L, f):

    e = (L-1)/f
    g = primRoots(L)[0]

    eta = generateEtas(L, f)
    nz = findEtaNz(eta)

    # build P(X) here X = 13

    P = [0] * L
    P[0] = 13
    P[1] = -1

    p = [i for i in P]

    for i in xrange(1,f):
        tmp = cycShift(p, pow(g,i*e,L))
        print tmp
        P = multCyc(P, tmp)

    print P

    # search for power of 13

    res = [[0] * L for i in xrange(f)]

    # first try to calculate the constant term
    c = P[0] - pow(13, f)
    P[0] -= c
    
    for i in xrange(f,0,-1):
        t = pow(13,i)
        for j in xrange(L):
            if P[j] != 0:
                if P[j] % t == 0:
                    res[i-1][j] = P[j] / t
                    P[j] = 0

    P[0] += c
    res.insert(0,P)

    print res

    print '(%+d)' % res[0][0],
    
    # now see which eta is which
    for i in xrange(1,f):
        print '(',
        for j in xrange(e):
            if res[i][nz[j]] != 0:
                print u'%+d*\u03B7%d' % (res[i][nz[j]],j),
        print ')*X^%d' % i,

    if res[f][0] != 1:
        print 'res[f][0] not one, something wrong'
        
    for j in xrange(1,L):
        if res[f][j] != 0:
            print 'res[f] is not right'
            break
        
    print '(%+d)*X^%d' % (res[f][0], f)



def bbaass():
    for i in xrange(2**6):
        for j in xrange(6):
            print ((i >> j) & 1),
        print



def Page133Problem5(L):

    import itertools
    # we need to get all possible values of e

    for e in xrange(2,L):
        print 'e = %d' % e
        if (L-1) % e == 0:
            f = (L-1)/e
            
            eta = generateEtas(L,f)
            nz = findEtaNz(eta)

            # don't forget to set the minus sign
            for i in xrange(e):
                eta[i] = [-1*j for j in eta[i]]

            t = [i for i in range(0,e)]
    
            for y in xrange(1,e+1):
        
                l = itertools.combinations(t, y)

                tot = [0] * L
                for i in l:
                    # create individual products
                    res = [0] * L
                    res[0] = 1
                    for j in i:
                        res = multCyc(res, eta[j])

                    tot = addCyc(tot, res)

                # check that tot has same elements from [1:end]
                for i in xrange(2,L):
                    if tot[i] != tot[i-1]:
                        print 'Something Wrong'
                else:
                    print '%d*X^%d' % (tot[0] - tot[1], e - y)

    
def findOrder(L, p):
    for i in xrange(1,L):
        if pow(p,i,L) == 1:
            return i

def isZeroModP(f, p):
    L = len(f)
    c = f[0] % p
    for k in xrange(1,L):
        if (f[k] % p) != c:
            return False

    return True

def changeModP(f, p):
    L = len(f)
    for i in xrange(L):
        f[i] = f[i] % p

    return f

def checkMultiplicity(f, Psi, p):
    L = len(f)
    
    res = multCyc(f, Psi)
    mult = 1
    if isZeroModP(res, p) == False:
        return 0
    else:
        for i in xrange(1, 10):
            res = multCyc(res, Psi)
            if isZeroModP(res, pow(p, i + 1)) == False:
                mult = i
                break
        else:
            mult = float('inf')

    return mult

def findPsi(L, p):

    f = findOrder(L, p)
    e = (L - 1)/f

    print 'f =', f
    
    eta = generateEtas(L, f)
    nz = findEtaNz(eta)

    # u is the u in \eta_i \equib u_i
    u = [0] * e

    Psi = [0] * L
    Psi[0] = 1
    
    for v in xrange(p):
        for i in xrange(e):

            t = [1*k for k in eta[i]]
            t[0] -= v
            tmp = [1*k for k in Psi]
            tmp = changeModP(multCyc(tmp, t), p)

            if isZeroModP(tmp, p) == False:
                Psi = [1*k for k in tmp]
            else:
                u[i] = v

    # check consistency and print output
    etj = [i for i in eta]

    # this is the phi from Page 140
    phi = [0] * L    
    g = primRoots(L)[0]
    for k in xrange(e):

        # check consistency
        for i in xrange(e):
            etj[i][0] = -u[(i-k) % e]
            tmp = multCyc(Psi, etj[i])
            if isZeroModP(tmp, p) == False:
                print 'There is something wrong', tmp, k, i

        Psi = cycShift(Psi, g)
        # we don't add Psi itself, only its conjugates
        if k < e-1:
            phi = addCyc(phi, Psi)

    # we now check how many times phi is divisible
    # by this prime factor

    mult = checkMultiplicity(phi, Psi, p)
    
    if mult == 0:
        print u'Something wrong with \u03C6(\u03B7)'
    elif mult != float('inf'):
        print u'\n\u03C6(\u03B7) is divisible %d times\n' % mult
    else:
        print u'is still divisible at 11 multiplicities'
    
        
    # print output
    print u'\u03A8(\u03B7) =',
    printSumEtaRaw(Psi, nz)
    print

    if mult > 1:
        phi[0] += p
    print u'\u03C6(\u03B7) =',
    printSumEtaRaw(phi, nz)
    print

    # something extra check multiplicities of eta_i - u_i
    for i in xrange(e):
        eta[i][0] = -u[i]
        mult = checkMultiplicity(eta[i], Psi, p)
        print u'multiplicity of \u03B7%d - %d is %d' % (i, u[i], mult)
    
    return Psi, phi, u

