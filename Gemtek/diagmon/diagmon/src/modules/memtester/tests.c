/*
 * Very simple but very effective user-space memory tester.
 * Originally by Simon Kirby <sim@stormix.com> <sim@neato.org>
 * Version 2 by Charles Cazabon <charlesc-memtester@pyropus.ca>
 * Version 3 not publicly released.
 * Version 4 rewrite:
 * Copyright (C) 2004-2010 Charles Cazabon <charlesc-memtester@pyropus.ca>
 * Licensed under the terms of the GNU General Public License version 2 (only).
 * See the file COPYING for details.
 *
 * This file contains the functions for the actual tests, called from the
 * main routine in memtester.c.  See other comments in that file.
 *
 */

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#include "types.h"
#include "sizes.h"
#include "memtester.h"
#include "tests.h"
//#include <errUtils.h>

char progress[] = "-\\|/";
#define PROGRESSLEN 4
#define PROGRESSOFTEN 2500
#define ONE 0x00000001L

struct test tests2[] = {
     { "Random Value", test_random_value },
     { "Compare XOR", test_xor_comparison },
     { "Compare SUB", test_sub_comparison },
     { "Compare MUL", test_mul_comparison },
     { "Compare DIV",test_div_comparison },
     { "Compare OR", test_or_comparison },
     { "Compare AND", test_and_comparison },
     { "Sequential Increment", test_seqinc_comparison },
     { "Solid Bits", test_solidbits_comparison },
     { "Block Sequential", test_blockseq_comparison },
     { "Checkerboard", test_checkerboard_comparison },
     { "Bit Spread", test_bitspread_comparison },
     { "Bit Flip", test_bitflip_comparison },
     { "Walking Ones", test_walkbits1_comparison },
     { "Walking Zeroes", test_walkbits0_comparison },
     { "8-bit Writes", test_8bit_wide_random },
     { "16-bit Writes", test_16bit_wide_random },
     { NULL, NULL }
};


/* Function definitions. */

int compare_regions(ulv *bufa, ulv *bufb, size_t count, int x) {
    int r = 0;
    size_t i;
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    off_t physaddr;

//    printf("\b\b\b\b\b\b\b\b\b\b\b");
//    fflush(stdout);
    for (i = 0; i < count; i=i+10000, p1++, p2++) {
        if (*p1 != *p2) {
/*          if (use_phys) {
                physaddr = physaddrbase + (i * sizeof(ul));
                fprintf(stderr, 
                        "FAILURE: 0x%08lx != 0x%08lx at physical address "
                        "0x%08lx.\n", 
                        (ul) *p1, (ul) *p2, physaddr);
            } else {
                fprintf(stderr, 
                        "FAILURE: 0x%08lx != 0x%08lx at offset 0x%08lx.\n", 
                        (ul) *p1, (ul) *p2, (ul) (i * sizeof(ul)));
            }
*/            /* printf("Skipping to next test..."); */
	    physaddr = physaddrbase + (i * sizeof(ul));
            r = -1;
/*	    if(openErrLog()==1) {
                
		printf("\n");
                errLog_setTitle("Fatal error #1 during Memory test %s test", tests2[x].name);
                errLog_setTest("Start Memory test %s test", tests2[x].name);
                errLog_addMsg("Memtory test %s is FAILED", tests2[x].name);
		errLog_addMsg("-FAILURE: physical address at 0x%08lx--", physaddr);
                errLog_endMsg();
		errLog_endTest(1, "Memtory test %s test", tests2[x].name);
                
                closeErrLog();
            }   
*/
/*	    printf("\b\b\b\b\b\b\b\b\b\b\b");
	    printf("Test is FAILED");
	    fflush(stdout);
	    printf("\b\b\b");
	    fflush(stdout);
	    return 0;
*/	}
	else{
	    r = 0;
//	    physaddr = physaddrbase + (i * sizeof(ul));
//	    printf("\b\b\b\b\b\b\b\b\b\b\b\b");
//	    printf("0x%08lx", physaddr);
//	    fflush(stdout);
//	    printf("\b\b\b\b\b\b\b\b\b\b");
//	    fflush(stdout);
	}
	break;
    }
    return r;
}

int test_stuck_address(ulv *bufa, size_t count) {
    ulv *p1 = bufa;
    unsigned int j;
    size_t i;
    off_t physaddr;

    printf("           ");
    fflush(stdout);
    for (j = 0; j < 16; j++) {
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        p1 = (ulv *) bufa;
        printf("setting %3u", j);
        fflush(stdout);
        for (i = 0; i < count; i++) {
            *p1 = ((j + i) % 2) == 0 ? (ul) p1 : ~((ul) p1);
            *p1++;
	}
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        printf("testing %3u", j);
        fflush(stdout);
        p1 = (ulv *) bufa;
        for (i = 0; i < count; i++, p1++) {
            if (*p1 != (((j + i) % 2) == 0 ? (ul) p1 : ~((ul) p1))) {
                if (use_phys) {
                    physaddr = physaddrbase + (i * sizeof(ul));
                    fprintf(stderr, 
                            "FAILURE: possible bad address line at physical "
                            "address 0x%08lx.\n", 
                            physaddr);
                } else {
                    fprintf(stderr,
                            "FAILURE: possible bad address line at offset "
                            "0x%08lx.\n", 
                            (ul) (i * sizeof(ul)));
                }
                printf("Skipping to next test...\n");
                fflush(stdout);
                return -1;
            }
	}
    }
    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
    fflush(stdout);
    return 0;
}

int test_random_value(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    ul j = 0;
    size_t i;
    off_t physaddr;

    printf(" Test is testing ");
    fflush(stdout);
    for (i = 0; i < count; i=i+100000) {
        *p1++ = *p2++ = rand_ul();
/*        if (!(i % PROGRESSOFTEN)) {
            putchar('\b');
            putchar(progress[++j % PROGRESSLEN]);
            fflush(stdout);
        }
*/	physaddr = physaddrbase + (i * sizeof(ul));
        printf("0x%08lx", physaddr);
        printf("\b\b\b\b\b\b\b\b\b\b");
        fflush(stdout);
    }
//    printf("\b \b");
//    fflush(stdout);
    return compare_regions(bufa, bufb, count, 0);
}

int test_xor_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ ^= q;
        *p2++ ^= q;
    }
    return compare_regions(bufa, bufb, count, 1);
}

int test_sub_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ -= q;
        *p2++ -= q;
    }
    return compare_regions(bufa, bufb, count, 2);
}

int test_mul_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ *= q;
        *p2++ *= q;
    }
    return compare_regions(bufa, bufb, count, 3);
}

int test_div_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        if (!q) {
            q++;
        }
        *p1++ /= q;
        *p2++ /= q;
    }
    return compare_regions(bufa, bufb, count, 4);
}

int test_or_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ |= q;
        *p2++ |= q;
    }
    return compare_regions(bufa, bufb, count, 5);
}

int test_and_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ &= q;
        *p2++ &= q;
    }
    return compare_regions(bufa, bufb, count, 6);
}

int test_seqinc_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    size_t i;
    ul q = rand_ul();

    for (i = 0; i < count; i++) {
        *p1++ = *p2++ = (i + q);
    }
    return compare_regions(bufa, bufb, count, 7);
}

int test_solidbits_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    ul q;
    size_t i;

    printf("           ");
    fflush(stdout);
    for (j = 0; j < 64; j++) {
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        q = (j % 2) == 0 ? UL_ONEBITS : 0;
        printf("setting %3u", j);
        fflush(stdout);
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
        for (i = 0; i < count; i++) {
            *p1++ = *p2++ = (i % 2) == 0 ? q : ~q;
        }
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        printf("testing %3u", j);
        fflush(stdout);
        if (compare_regions(bufa, bufb, count, 8)) {
            return -1;
        }
    }
    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
    fflush(stdout);
    return 0;
}

int test_checkerboard_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    ul q;
    size_t i;
    off_t physaddr;

    printf(" Test is testing ");
    fflush(stdout);
    for (j = 0; j < 64; j++) {
//        printf("\b\b\b\b\b\b\b\b\b\b\b");
        q = (j % 2) == 0 ? CHECKERBOARD1 : CHECKERBOARD2;
//        printf("setting %3u", j);
//        fflush(stdout);
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
        for (i = 0; i < count; i=i+100000) {
            *p1++ = *p2++ = (i % 2) == 0 ? q : ~q;
	    physaddr = physaddrbase + (i * sizeof(ul));
            printf("0x%08lx", physaddr);
            printf("\b\b\b\b\b\b\b\b\b\b");
            fflush(stdout);
        }
//        printf("\b\b\b\b\b\b\b\b\b\b\b");
//        printf("testing %3u", j);
//        fflush(stdout);
//        if (compare_regions(bufa, bufb, count, 10)) {
//            return -1;
//        }
    }
    if (compare_regions(bufa, bufb, count, 10)) {
        return -1;
    }

//    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
//    fflush(stdout);
    return 0;
}

int test_blockseq_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    size_t i;

    printf("           ");
    fflush(stdout);
    for (j = 0; j < 256; j++) {
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
        printf("setting %3u", j);
        fflush(stdout);
        for (i = 0; i < count; i++) {
            *p1++ = *p2++ = (ul) UL_BYTE(j);
        }
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        printf("testing %3u", j);
        fflush(stdout);
        if (compare_regions(bufa, bufb, count, 9)) {
            return -1;
        }
    }
    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
    fflush(stdout);
    return 0;
}

int test_walkbits0_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    size_t i;
    off_t physaddr;

    printf(" Test is testing ");
    fflush(stdout);
    for (j = 0; j < UL_LEN * 2; j++) {
//        printf("\b\b\b\b\b\b\b\b\b\b\b");
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
//        printf("setting %3u", j);
//        fflush(stdout);
        for (i = 0; i < count; i=i+100000) {
            if (j < UL_LEN) { /* Walk it up. */
                *p1++ = *p2++ = ONE << j;
            } else { /* Walk it back down. */
                *p1++ = *p2++ = ONE << (UL_LEN * 2 - j - 1);
            }
	    physaddr = physaddrbase + (i * sizeof(ul));
            printf("0x%08lx", physaddr);
            printf("\b\b\b\b\b\b\b\b\b\b");
            fflush(stdout);
        }

//        printf("\b\b\b\b\b\b\b\b\b\b\b");
//        printf("testing %3u", j);
//        fflush(stdout);
//        if (compare_regions(bufa, bufb, count, 14)) {
//            return -1;
//        }
    }
    if (compare_regions(bufa, bufb, count, 14)) {
            return -1;
    }

//    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
//    fflush(stdout);
    return 0;
}

int test_walkbits1_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    size_t i;
    off_t physaddr;

    printf(" Test is testing ");
    fflush(stdout);
    for (j = 0; j < UL_LEN * 2; j++) {
//        printf("\b\b\b\b\b\b\b\b\b\b\b");
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
//        printf("setting %3u", j);
//        fflush(stdout);
        for (i = 0; i < count; i=i+100000) {
            if (j < UL_LEN) { /* Walk it up. */
                *p1++ = *p2++ = UL_ONEBITS ^ (ONE << j);
            } else { /* Walk it back down. */
                *p1++ = *p2++ = UL_ONEBITS ^ (ONE << (UL_LEN * 2 - j - 1));
            }
            physaddr = physaddrbase + (i * sizeof(ul));
            printf("0x%08lx", physaddr);
            printf("\b\b\b\b\b\b\b\b\b\b");
            fflush(stdout);
	}
//        printf("\b\b\b\b\b\b\b\b\b\b\b");
//        printf("testing %3u", j);
//        fflush(stdout);
//        if (compare_regions(bufa, bufb, count, 13)) {
//            return -1;
//        }
    }
    if (compare_regions(bufa, bufb, count, 13)) {
            return -1;
    }

//    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
//    fflush(stdout);
    return 0;
}

int test_bitspread_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j;
    size_t i;

    printf("           ");
    fflush(stdout);
    for (j = 0; j < UL_LEN * 2; j++) {
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        p1 = (ulv *) bufa;
        p2 = (ulv *) bufb;
        printf("setting %3u", j);
        fflush(stdout);
        for (i = 0; i < count; i++) {
            if (j < UL_LEN) { /* Walk it up. */
                *p1++ = *p2++ = (i % 2 == 0)
                    ? (ONE << j) | (ONE << (j + 2))
                    : UL_ONEBITS ^ ((ONE << j)
                                    | (ONE << (j + 2)));
            } else { /* Walk it back down. */
                *p1++ = *p2++ = (i % 2 == 0)
                    ? (ONE << (UL_LEN * 2 - 1 - j)) | (ONE << (UL_LEN * 2 + 1 - j))
                    : UL_ONEBITS ^ (ONE << (UL_LEN * 2 - 1 - j)
                                    | (ONE << (UL_LEN * 2 + 1 - j)));
            }
        }
        printf("\b\b\b\b\b\b\b\b\b\b\b");
        printf("testing %3u", j);
        fflush(stdout);
        if (compare_regions(bufa, bufb, count, 11)) {
            return -1;
        }
    }
    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
    fflush(stdout);
    return 0;
}

int test_bitflip_comparison(ulv *bufa, ulv *bufb, size_t count) {
    ulv *p1 = bufa;
    ulv *p2 = bufb;
    unsigned int j, k;
    ul q;
    size_t i;

    printf("           ");
    fflush(stdout);
    for (k = 0; k < UL_LEN; k++) {
        q = ONE << k;
        for (j = 0; j < 8; j++) {
            printf("\b\b\b\b\b\b\b\b\b\b\b");
            q = ~q;
            printf("setting %3u", k * 8 + j);
            fflush(stdout);
            p1 = (ulv *) bufa;
            p2 = (ulv *) bufb;
            for (i = 0; i < count; i++) {
                *p1++ = *p2++ = (i % 2) == 0 ? q : ~q;
            }
            printf("\b\b\b\b\b\b\b\b\b\b\b");
            printf("testing %3u", k * 8 + j);
            fflush(stdout);
            if (compare_regions(bufa, bufb, count, 12)) {
                return -1;
            }
        }
    }
    printf("\b\b\b\b\b\b\b\b\b\b\b           \b\b\b\b\b\b\b\b\b\b\b");
    fflush(stdout);
    return 0;
}

int test_8bit_wide_random(ulv* bufa, ulv* bufb, size_t count) {
    u8v *p1, *t;
    ulv *p2;
    int attempt;
    unsigned int b, j = 0;
    size_t i;
    off_t physaddr;

//    putchar(' ');
    printf(" Test is testing ");
    fflush(stdout);
    for (attempt = 0; attempt < 2;  attempt++) {
        if (attempt & 1) {
            p1 = (u8v *) bufa;
            p2 = bufb;
        } else {
            p1 = (u8v *) bufb;
            p2 = bufa;
        }
        for (i = 0; i < count; i=i+100000) {
            t = mword8.bytes;
            *p2++ = mword8.val = rand_ul();
            for (b=0; b < UL_LEN/8; b++) {
                *p1++ = *t++;
            }
/*            if (!(i % PROGRESSOFTEN)) {
                putchar('\b');
                putchar(progress[++j % PROGRESSLEN]);
                fflush(stdout);
            }
*/	    physaddr = physaddrbase + (i * sizeof(ul));
            printf("0x%08lx", physaddr);
            printf("\b\b\b\b\b\b\b\b\b\b");
            fflush(stdout);
        }
//        if (compare_regions(bufa, bufb, count, 15)) {
//            return -1;
//        }
    }
    if (compare_regions(bufa, bufb, count, 15)) {
        return -1;
    }

//    printf("\b \b");
//    fflush(stdout);
    return 0;
}

int test_16bit_wide_random(ulv* bufa, ulv* bufb, size_t count) {
    u16v *p1, *t;
    ulv *p2;
    int attempt;
    unsigned int b, j = 0;
    size_t i;

    putchar( ' ' );
    fflush( stdout );
    for (attempt = 0; attempt < 2; attempt++) {
        if (attempt & 1) {
            p1 = (u16v *) bufa;
            p2 = bufb;
        } else {
            p1 = (u16v *) bufb;
            p2 = bufa;
        }
        for (i = 0; i < count; i++) {
            t = mword16.u16s;
            *p2++ = mword16.val = rand_ul();
            for (b = 0; b < UL_LEN/16; b++) {
                *p1++ = *t++;
            }
            if (!(i % PROGRESSOFTEN)) {
                putchar('\b');
                putchar(progress[++j % PROGRESSLEN]);
                fflush(stdout);
            }
        }
        if (compare_regions(bufa, bufb, count, 16)) {
            return -1;
        }
    }
    printf("\b \b");
    fflush(stdout);
    return 0;
}
