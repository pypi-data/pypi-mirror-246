#ifndef RANDOM_H
 #define RANDOM_H

#include <stdlib.h>
#include "mt.h"

// from mt.h
#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfUL
#define UPPER_MASK 0x80000000UL
#define LOWER_MASK 0x7fffffffUL
//

#ifndef RANDOM
 #define RANDOM(m, n) (MT_genrand_int32(m) % (n))
#endif
#ifndef RANDOM0
// #define RANDOM0(n) (genrand_int32() % (n))
 #define RANDOM0(n) (MT_genrand_int32(mt0) % (n))
#endif

#ifndef NEWA
 #define NEWA(p,t,n) {p = (t*)malloc((n)*sizeof(*p));if ((p)==NULL) {printf("not enough memory\n"); exit(1);};}
#endif

#ifndef NEWT
 #define NEWT(t, p) \
  t p; \
  p = (t)malloc(sizeof(*p)); \
  if ((p)==NULL) {printf("not enough memory\n"); exit(1);}
#endif


typedef struct mt {
  unsigned long mt[N];
  int mti;
  long count;
}* MT;

//extern MT mt0, mt1[NC], mt2[NC], mts[NC];

extern MT mt0, mt1[NC], mt2[NC], mts[NC];
#ifndef _MTVAR
 #define _MTVAR
 MT mt0 = NULL;
 MT mt1[NC], mt2[NC], mts[NC], mt3[NC];
 unsigned long MT_init[4][5] = {
  {0x123, 0x234, 0x345, 0x456, 0x789},
  {0x123, 0x234, 0x345, 0x456, 0x789},
  {0x123, 0x234, 0x345, 0x456, 0x789},
  {0x123, 0x234, 0x345, 0x456, 0x789}
 };
#endif

/****************************************************
 * mt1 はパーティー 0 と 1 で共有する乱数
 * mt2 はパーティー 0 と 2 で共有する乱数
 * (パーティー 1, 2 では mts という名前で使う)
 * mt0 は共有しない乱数
****************************************************/


// from mt.h
void _init_genrand(unsigned long s, unsigned long mt[N], int *mti_)
{
  int mti;
    mt[0]= s & 0xffffffffUL;
    for (mti=1; mti<N; mti++) {
        mt[mti] = 
	    (1812433253UL * (mt[mti-1] ^ (mt[mti-1] >> 30)) + mti); 
        /* See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier. */
        /* In the previous versions, MSBs of the seed affect   */
        /* only MSBs of the array mt[].                        */
        /* 2002/01/09 modified by Makoto Matsumoto             */
        mt[mti] &= 0xffffffffUL;
        /* for >32 bit machines */
    }
  *mti_ = mti;
}

void _init_by_array(unsigned long init_key[], int key_length, unsigned long mt[N])
{
    int i, j, k;
    init_genrand(19650218UL);
    i=1; j=0;
    k = (N>key_length ? N : key_length);
    for (; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525UL))
          + init_key[j] + j; /* non linear */
        mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
        i++; j++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
        if (j>=key_length) j=0;
    }
    for (k=N-1; k; k--) {
        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941UL))
          - i; /* non linear */
        mt[i] &= 0xffffffffUL; /* for WORDSIZE > 32 machines */
        i++;
        if (i>=N) { mt[0] = mt[N-1]; i=1; }
    }

    mt[0] = 0x80000000UL; /* MSB is 1; assuring non-zero initial array */ 
}

unsigned long _genrand_int32(unsigned long mt[N], int *mti_)
{
    int mti = *mti_;
    unsigned long y;
    static unsigned long mag01[2]={0x0UL, MATRIX_A};
    /* mag01[x] = x * MATRIX_A  for x=0,1 */

    if (mti >= N) { /* generate N words at one time */
        int kk;

        if (mti == N+1)   /* if init_genrand() has not been called, */
            _init_genrand(5489UL, mt, &mti); /* a default initial seed is used */

        for (kk=0;kk<N-M;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        for (;kk<N-1;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1UL];
        }
        y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1UL];

        mti = 0;
    }
  
    y = mt[mti++];

    /* Tempering */
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);

    *mti_ = mti;
    return y;
}
//

MT MT_init_by_array(unsigned long init[], int len)
{
  NEWT(MT, m);
  _init_by_array(init, len, m->mt);
//  for (int i=0; i<N; i++) m->mt[i] = mt[i];
  m->mti = N+1;
  m->count = 0;
  return m;
}


unsigned long MT_genrand_int32(MT m)
{
  unsigned long y;
  if (m->mti >= N) {
#if 0
    for (int i=0; i<N; i++) mt[i] = m->mt[i];
    mti = m->mti;
    y = genrand_int32();
    for (int i=0; i<N; i++) m->mt[i] = mt[i];
    m->mti = mti;
#else
    y = _genrand_int32(m->mt, &m->mti);
#endif
  } else {
// from mt.h
    y = m->mt[m->mti++];

    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680UL;
    y ^= (y << 15) & 0xefc60000UL;
    y ^= (y >> 18);
//
  }
  m->count++;
  return y;
}

void MT_free(MT m)
{
  free(m);
}

#undef N
#undef M

#endif

#ifdef MT_MAIN
int main(void) {
  unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};

  init_by_array(init, 5);
  for (int i=0; i<1000; i++) {
    genrand_int32();
  }
  for (int i=0; i<10; i++) {
    printf("%lx ", genrand_int32());
  }
  printf("\n");

  init[4] = 1;
  init_by_array(init, 5);
  for (int i=0; i<1000; i++) {
    genrand_int32();
  }
  for (int i=0; i<10; i++) {
    printf("%lx ", genrand_int32());
  }
  printf("\n");

  init[4] = 0;
  MT m1 = MT_init_by_array(init, 5);
  init[4] = 1;
  MT m2 = MT_init_by_array(init, 5);
  for (int i=0; i<1000; i++) {
    MT_genrand_int32(m1);
    MT_genrand_int32(m2);
  }
  for (int i=0; i<10; i++) {
    printf("%lx ", MT_genrand_int32(m1));
    printf("%lx ", MT_genrand_int32(m2));
  }
  printf("\n");


  return 0;
}

#endif
