A = 149
line = 2
r = 12
# we don't really need this, we can just set K = -5/k
s = -5
k = 1
K = s/k

# This is for Problem 6, since I'm already writing a script
# let's use it instead of multiplying matrices
kK = [k, K]
P = [1,12]
Q = [0, 1]

while K <> 1:    
    # min_s is to hold the current possible minimum of s
    # has to be reset everytime we search for the next K
    min_s = float('inf')
    # next_R is a dummy variable to contain possible R
    next_R = r
    while True:

        # make sure next_R is different from r
        next_R += 1
        # this loop is here to find R such that r + R is divisible by K
        while next_R % abs(K) <> 0:
            next_R += 1

        R = next_R - r
        next_s = R**2 - A

        # using the Indian cyclic method we want R that minimizes
        # abs(s), so I created this min_s to hold the current min for s
        # produced by the current R (next_R)

        # they way I know that I've got the minimum s is if the next s
        # is bigger than the previous one, this way I need to keep the previous s
        # and previous R

        if abs(next_s) < min_s:
            min_s = abs(next_s)
            prev_s = next_s
            prev_r = R
        else:
            # Calculate next P and Q
            n = (r + prev_r)/abs(K)
            sgn = kK[0]*kK[1]/(abs(kK[0])*abs(kK[1]))
            
            new_P = n*P[1] - sgn*P[0]
            new_Q = n*Q[1] - sgn*Q[0]

            # now update these values to the new ones
            r = prev_r
            K = prev_s/K
            s = prev_s

            kK[0] = kK[1]
            kK[1] = K
            P[0] = P[1]
            P[1] = new_P
            Q[0] = Q[1]
            Q[1] = new_Q
            
            line += 1
            print "line:{0:3d} r:{1:3d} s:{2:4d} K:{3:3d} P:{4:<12d} Q:{5:<11d}".format(line, r, s, K, new_P, new_Q)
            break

