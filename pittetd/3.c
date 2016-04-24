#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h> // for memset
#include<time.h>
#include <stdint.h>

// This lists the orders of different numbers in Z/p^nZ where p is a prime

typedef unsigned long long uint64;
typedef signed long long int64;

//typedef unsigned int myU128 __attribute__((mode(TI)));
/*
typedef int __int128 __attribute__ ((__mode__ (TI)));
typedef unsigned int __uint128 __attribute__ ((__mode__ (TI)));

typedef unsigned __int128 uint128_t;
typedef signed __int128 int128_t;
*/

// Globals

uint64 * pf = NULL; // Prime Factors
uint64 * pn = NULL; // Powers of each prime factor
uint64 max; // max number of factors

// Functions

uint64 Varphi(void)
{
    uint64 i, v=1ULL;
    
    for (i = 0ULL; i < max; i++)
    {
        if (pn[i] > 0ULL)
        {
            v *= pf[i]-1ULL;
            while (pn[i] > 1ULL)
            {
                v *= pf[i];
                pn[i]--;
            }
        }
    }
    
    return v;
}



void PrintPrimeFactors(void)
{
    uint64 i;

    for (i = 0ULL; i < max; i++)
    {
        if (pf[i] != 0ULL)
        {
            printf("{%lld, %lld} ", pf[i], pn[i]);
        }
        else
        {
            printf("\n");
            return;
        }
    }
}

void InsertPrime(uint64 n)
{
    uint64 i;

    if (pf[0] == 0ULL)
    {
        pf[0] = n;
        pn[0]++;
        return;
    }
    
    for (i = 0ULL; i < max; i++)
    {
        if (pf[i] == n)
        {
            pn[i]++;
            return;
        }
        if (pf[i] == 0)
        {
            pf[i] = n;
            pn[i]++;
            return;
        }
    }
}

// returns the number of factors of n, if it is 1 then it is a prime number
uint64 PrimeFactors(uint64 n) 
{    
    uint64 count = 0ULL;
    
    if (n == 0)
    {
        return 0ULL;
    }
    
    if (n == 1)
    {
        return 1ULL;
    }
    else
    {
        max = sqrtl(n);
        
        if (pf != NULL)
            free(pf);
        if (pn != NULL)
            free(pn);
        
        pf = (uint64 *)malloc(sizeof(uint64) * max);
        pn = (uint64 *)malloc(sizeof(uint64) * max);
        
        memset(pf, 0, sizeof(uint64) * max);
        memset(pn, 0, sizeof(uint64) * max);
        
        // Print the number of 2s that divide n
        while (n%2 == 0)
        {         
            InsertPrime(2ULL);
            count++;
            n = n/2;
        }       
        
        // n must be odd at this point.  So we can skip one element (Note i = i +2)
        for (uint64 i = 3; i <= sqrtl(n); i = i+2)
        {         
            // While i divides n, print i and divide n         
            while (n%i == 0)         
            {             
                InsertPrime(i);
                count++;
                n = n/i;
            }
        }       
        // This condition is to handle the case when n is a prime number     
        // greater than 2     
        if (n > 2)
        {
            InsertPrime(n);
            count++;
        }
    }
    
    return count;
}

uint64 FindGcd(uint64 m, uint64 n)
{
    uint64 a=m,b=n,r;
    
    while(1)
    {
        r = a % b;
        
        if (r == 1ULL)
            return 1ULL;
        if (r == 0ULL)
            return b;
        
        a=b;
        b=r;
    }
    
    return 0;
}

uint64 Power(uint64 p, uint64 n)
{
    uint64 pn = 1ULL;
    
    while(n > 0)
    {
        pn = pn*p;
        n--;
    }
    
    return pn;
}

// q must not be 0
uint64 FindOrder(uint64 mod, uint64 q)
{
    uint64 i = q, j = 1ULL;
    
    if (FindGcd(mod, q) != 1ULL || mod == 1ULL)
        return 0ULL;
    
    while (q % mod != 1ULL)
    {
        q = (q*i) % mod;
        j++;
    }
    
    return j;
}

void ListOrderPowerOfPrime(uint64 p, uint64 n)
{
    uint64 pn = 1ULL, i;
    
    if (PrimeFactors(p) != 1ULL || p <= 1ULL)
    {
        printf("ERROR, p is NOT prime!\n\n");
        return;
    }

    if (n == 0ULL)
    {
        printf("ERROR, n must be greater than 0!\n\n");
        return;
    }
    
    pn = Power(p, n);
    
    for (i = 1; i <= pn; i++)
    {
        if (i % p != 0)
        {
            printf("%lld:\t%lld\n", i, FindOrder(pn,i));
        }
    }
}

void FindPrimitiveRoots (uint64 q)
{
    uint64 i, j, x, v;
    
    PrimeFactors(q);
    v = Varphi();
    
    printf("\nvarphi: %lld\n\n", v);

    for (i = 1+1; i <= q; i++)
    {
        if (FindGcd(q,i) == 1ULL)
        {
            j = FindOrder(q, i);
            
            if (j == v)
            {
                printf("%lld:\t%lld *****\n", i, j);
            }
        }
    }
}

void FindPrimesWith_n_AsSmallestPrimitiveRoot(uint64 start, uint64 end, uint64 n)
{
    uint64 j, v, q;
    
    for (q = start; q <= end; q++)
    {
        if (PrimeFactors(q) == 1)
        {
            j = FindOrder(q, n);

            if (j != 0ULL && j == q-1)
            {
                for (v = n-1; v > 1ULL; v--)
                {
                    j = FindOrder(q, v);
                    
                    if (j == q-1)
                    {
                        break;
                    }
                }
                
                if (v == 1ULL)
                    printf("%lld\n", q);
            }
                
        }
    }    
}

void FindFractionOfPrimesWith2AsPrimitiveRoot (uint64 start, uint64 end)
{
    uint64 j, v = 0ULL, y = 0ULL;
    
    uint64 q;
    
    for (q = start; q < end; q++)
    {
        if (PrimeFactors(q) == 1)
        {
            y++;
            j = FindOrder(q, 2ULL);
            
            if (j != 0ULL && j == q-1)
            {
                printf("%lld\n", q);
                v++;
            }
        }
    }
    
    printf("%lld out of %lld = %2.2f%%\n",v, y, ((double)v*100)/((double)y));
}


uint64 PowerModQ(uint64 n, uint64 x, uint64 q)
{
    /*
    uint64 res = 1ULL;
    uint64 ord;
    
    ord = FindOrder(q, x);
    
    n = n % ord;
    
    while(n > 0ULL)
    {
        res = (res*x) % q;
        n--;
        
        printf("n:%lld\n", n);
    }
    
    return res;
    */
    
    uint64 a[64];
    uint64 i, temp = 1ULL;
    
    a[0] = x % q;
    if (n & 0x1ULL)
        temp = a[0];
    
    for (i = 1ULL; i < 64ULL; i++)
    {
        a[i] = (a[i-1]*a[i-1]) % q;
        if ((n >> i) & 0x1ULL)
        {
            temp = (temp * a[i]) % q;
        }
    }
    
    return (temp % q);

}

uint64 LogModQ(uint64 y, uint64 x, uint64 q)
{
    uint64 res = x % q, n = 1ULL;
    
    y = y % q;
    while(res != y)
    {
        res = (res*x) % q;
        n++;
    }
    
    return n;
}

uint64 CrackRSAFermatMethod(uint64 n)
{
    uint64 t, s, s2, ds2, i = 0;    
    
    t = (uint64)ceill(sqrtl(n));
    //printf("t:%lld %lld\n", t, n);
    //return;
    
    while (t < n)
    {
        s2 = (t*t) - n;
        s = sqrtl(s2);
        
        //printf("::%lld %lld %lld %lld %c\n",s*s, s2, t+s, t-s, 13);
        //return;
        if (s2 == s*s)
        {
            printf("p: %lld, q: %lld\n", (t+s), (t-s));
            return i;
        }
        t++;
        i++;
        
        //if (i > 10)
        //    return;
    }
    
    return i;
}

uint64 Xgcd(uint64 * a, uint64 * b, uint64 * x, uint64 * y)
{
    int64 r = 0ULL, s = 1ULL, so, ro;
    int64 g, temp, q, c, ao = *a, bo = *b;
    
    *x = 1ULL;
    *y = 0ULL;
    
    if (*a < *b)
    {
        temp = *a;
        *a = *b;
        *b = temp;
        ao = *a;
        bo = *b;
    }    
    
    while (*b != 0ULL)
    {
        q = (*a) / (*b);
        c = (*a) % (*b);
        
        *a = *b;
        *b = c;
        so = s; ro = r;
        r = (*x) - q*ro;
        s = (*y) - q*so;
        *x = ro;
        *y = so;
    }
    
    g = *a;
    
    *a = ao;
    *b = bo;

    return g;
}

#define MA 1ULL
void CrackRSAKnowingDMethod(uint64 d, uint64 e, uint64 n)
{
    uint64 m = e*d - 1, j;
    uint64 a[MA], r, g;
    
    printf("%lld\n", m);
    
    j = 0ULL;
    for (uint64 i = 1000ULL; i < 2000ULL && j < MA; i++)
    {
        g = rand();
        if (FindGcd(g, n) == 1ULL)
        {
            a[j] = g;
            j++;
        }
    }
    
    a[0] = 2ULL;
    
    printf("j:%lld\n", j);
    
    while (m % 2 == 0ULL && m > 0ULL)
    {
        m = m/2ULL;
        
        printf("m: %lld\n", m);
        for (uint64 i = 0ULL; i < MA; i++)
        {
            r = PowerModQ(m, a[i], n);
            printf("3 %lld\n", r);
            
            if (r != 1ULL)
            {
                g = FindGcd(r - 1ULL, n);
                printf("g: %lld\n", g);
                if (g > 1ULL && g < n)
                {
                    printf("p: %lld, q: %lld\n", g, n/g);
                    return;
                }
            }
            //printf("%lld\n", i);
        }
    }    
}

int main (int argc, char * argv[])
{
    clock_t begin, end;
    double time_spent;
    
    uint64 i;
    

    /*
    ListOrderPowerOfPrime((uint64) atoi(argv[1]), (uint64) atoi(argv[2]));
    
    FindPrimitiveRoots(Power((uint64) atoi(argv[1]), (uint64) atoi(argv[2])));
    
    FindPrimesWith_n_AsSmallestPrimitiveRoot(10000ULL, 90000ULL, 37ULL);
    
    FindFractionOfPrimesWith2AsPrimitiveRoot(1ULL, 1000ULL);
    */
    //printf("%lld\n", PowerModQ((uint64) atoi(argv[1]), (uint64) atoi(argv[2]), (uint64) atoi(argv[3])));
    //printf("%lld\n", LogModQ((uint64) atoi(argv[1]), (uint64) atoi(argv[2]), (uint64) atoi(argv[3])));

    /*
    begin = clock();
    PrimeFactors((uint64) atoll(argv[1]));
    end = clock();
    time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%f\n", time_spent);

    PrintPrimeFactors();
    
    begin = clock();
    i = CrackRSAFermatMethod((uint64) atoll(argv[1]));
    end = clock();
    time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%lld %f\n", i, time_spent);
    */

    /*
    uint64 a = (uint64) atoll(argv[1]), b = (uint64) atoll(argv[2]), x, y;
    printf("%lld\n", Xgcd(&a, &b, &x, &y));
    printf("%lld %lld %lld %lld\n", a, b, x, y);
    */

    CrackRSAKnowingDMethod((uint64) atoll(argv[1]), (uint64) atoll(argv[1]), (uint64) atoll(argv[1]));
    
    //printf("%lld\n", PowerModQ((uint64) atoll(argv[1]), (uint64) atoll(argv[2]), (uint64) atoll(argv[3])));
    
    return 0;
}