
#include <stdlib.h>
#include <stdio.h>

typedef unsigned long long ui;

typedef struct {
    int x1;
    int x2;
    int y1;
    int y2;
    int z1;
    int z2;
    char on;
} Cube;

int comp(const void * a, const void * b) {
    return *(int*)a == *(int*)b ? 0 : (*(int*)a < *(int*)b ? -1 : 1);
}

int abs(int x) {
    return x < 0 ? -x : x;
}

ui integrate(Cube * input, int inputl, int p1) {
    ui result = 0;

    if ( inputl > 1000 ) {
        return 0;
    }

    int * const X = malloc(sizeof(int) * inputl * 2);
    int * const Y = malloc(sizeof(int) * inputl * 2);
    int * const Z = malloc(sizeof(int) * inputl * 2);
    int Xl, Yl, Zl;
    Xl = Yl = Zl = 0;

    for ( int i = 0; i < inputl; i++ ) {
        if ( p1 ) {
            if ( !(( abs(input[i].x1) <= 50 )
                && ( abs(input[i].x2) <= 50 )
                && ( abs(input[i].y1) <= 50 )
                && ( abs(input[i].y2) <= 50 )
                && ( abs(input[i].z1) <= 50 )
                && ( abs(input[i].z2) <= 50 ))
            ) {
                continue;
            }
        }
        X[Xl++] = input[i].x1; X[Xl++] = input[i].x2+1;
        Y[Yl++] = input[i].y1; Y[Yl++] = input[i].y2+1;
        Z[Zl++] = input[i].z1; Z[Zl++] = input[i].z2+1;
    }

    qsort(X, Xl, sizeof(int), *comp);
    qsort(Y, Yl, sizeof(int), *comp);
    qsort(Z, Zl, sizeof(int), *comp);

    printf("%d, %d, %d\n", Xl, Yl, Zl);

    for ( int xi = 0; xi+1 < Xl; xi++ ) {
        printf("%d/%d\n", xi, Xl-2);
        for ( int yi = 0; yi+1 < Yl; yi++ ) {
            for ( int zi = 0; zi+1 < Zl; zi++ ) {
                for ( int ii = 0; ii < inputl; ii++ ) {
                    Cube e = input[inputl-1-ii];
                    if ( e.x1 <= X[xi] && X[xi] <= e.x2 &&
                         e.y1 <= Y[yi] && Y[yi] <= e.y2 &&
                         e.z1 <= Z[zi] && Z[zi] <= e.z2 ) {
                        if ( e.on == 1 ) {
                            result += (ui)(X[xi+1] - X[xi]) * (ui)(Y[yi+1] - Y[yi]) * (ui)(Z[zi+1] - Z[zi]);
                        }
                        break;
                    }
                }
            }
        }
    }

    free(X);
    free(Y);
    free(Z);

    return result;
}

