#include<stdio.h>
#include<stdlib.h>

int main (int argc, char * argv[])
{
    unsigned long long y, m, ku, kd, w, max, max2, z, zc;
    
    m = (unsigned long long)atoll(argv[1]);
    
    for (y = 1ULL; y <= m; y++)
    {    
        ku = 24ULL*y + 20ULL;
        
        max = 0ULL;
        max2 = 0ULL;
        z = 0ULL;
        zc = 0ULL;
        
        for (w = 1ULL; w < ku; w+=1ULL)
        {
            kd = (w*w) % ku;
            
            if (max <= ku - kd && ku - kd < ku)
                max = ku - kd;
            
            if (max2 <= ku - kd && ku - kd < max)
            {
                max2 = ku - kd;
                z = w;
            }
            
            if (kd == 0ULL && z == 0ULL)
                z = w;
            
            if (kd == 0ULL)
                zc++;
            
            
        }
        
        printf("max : %lld, max2 : %lld, max-max2 : %lld, max2 w : %lld\n", max, max2, max - max2, z);
    }
    return 0;
    
    
}