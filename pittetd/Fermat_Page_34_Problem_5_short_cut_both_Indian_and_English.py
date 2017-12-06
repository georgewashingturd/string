# it builds solution starting from line 1
def SolvePell(A=149, English=False, Shortcut=True):

    # cosmetics only
    output_string = "line:{0:3d} r:{1:3d} s:{2:4d} K:{3:3d} P:{4:<17d} Q:{5:<11d}"

    # try to start from line 1
    line = 1
    r = 0
    K = 1**2 - A*0

    # This is for Problem 6, since I'm already writing a script
    # let's use it instead of multiplying matrices
    kK = [0, K]
    P = [0, 1]
    Q = [0, 0]

    # print line 1, the loop below will generate line 2 and above
    # here r and s doesn't make sense since we had nowhere to come from
    print output_string.format(line, r, 0, K, 1, 0)
    
    while kK[0] == 0 or K <> 1:
        
        # min_s is to hold the current possible minimum of s
        # has to be reset everytime we search for the next K,
        # this is only for the Indian method
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

            # for the English method we want to make R as large as possible
            # while maintaining next_s to be negative, thus we stop once we get
            # a positive or zero next_s

            if English == True:
                if next_s < 0:
                    prev_s = next_s
                    prev_r = R
                    continue
            else:               
                if abs(next_s) < min_s:
                    min_s = abs(next_s)
                    prev_s = next_s
                    prev_r = R
                    continue

            # Calculate next P and Q, for the first line we cannot use the matrix method
            # since there is only one line the matrix method requires two
            if line >= 2:
                n = (r + prev_r)/abs(K)
                sgn = kK[0]*kK[1]/(abs(kK[0])*abs(kK[1]))
            
                new_P = n*P[1] - sgn*P[0]
                new_Q = n*Q[1] - sgn*Q[0]
            else:
                new_P = prev_r
                new_Q = 1
                
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

            # This is the short cut defined in Problem 7, if two consecutive
            # k's are the same magnitude we can multiply the results together
            # and divide the new P and Q by k^2 to get p^2 - Aq^2 = \pm 1
            # if it's minus one we need to multiply it again to get the final result

            if Shortcut == True and abs(kK[1]) == abs(kK[0]):
                # but before preceding, show the twin k's to user first :)
                print output_string.format(line, r, s, K, new_P, new_Q)
                
                new_P = P[0]*P[1] + A*Q[0]*Q[1]
                new_Q = Q[0]*P[1] + P[0]*Q[1]
                new_K = new_P**2 - A*(new_Q**2)
                new_K = new_K/(abs(kK[1])**2)

                if new_K == -1:
                    new_P, new_Q = (new_P*new_P + A*new_Q*new_Q)/(abs(kK[1])**2), (2*new_P*new_Q)/(abs(kK[1])**2)
                    new_K = new_P**2 - A*(new_Q**2)

                # make sure the outer loop stop
                K = new_K
                
                print "Final line: K:{0:3d} P:{1:<12d} Q:{2:<11d}".format(K, new_P, new_Q)
                break
                    
            
            print output_string.format(line, r, s, K, new_P, new_Q)
            break

SolvePell(149,False,True)
