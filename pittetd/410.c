#include<stdio.h>
#include<stdlib.h>

int main (void)
{
    unsigned long long ku, kd, w, a;
    
    for (w = 1ULL; w < 10LL; w++)
    {
        ku = (1ULL*w*w)-(5ULL*w)+8ULL;
        kd = 10ULL;
        printf("%lld %lld 30 : %lld\n", (1ULL*w*w) % kd, -((5ULL*w) % kd), ku % kd);
    }
    
    return 0;
    
    
}