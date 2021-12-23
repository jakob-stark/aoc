#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct Game Game;
typedef struct Hash Hash;

typedef unsigned short hash_t;

static inline int imin(int x, int y) {
    return x < y ? x : y;
}

struct Game {
    char hallway[7];
    char rooms[4][4];
};

struct Hash {
    int cost;
    Game entry;
};

static inline hash_t hash(const Game* g, char D) {
    uint32_t result = 314159265;
    for ( unsigned char i = 0; i < 7+4*D; i++ ) {
        result ^= (((unsigned char *)g)[i] & 0x7) << i%10*3;
    }
    result ^= result << 13;
    result ^= result >> 17;
    result ^= result << 5;
    return result & 0x7fff;
}

static const int dist[7][4] = {
    {3,5,7,9},
    {2,4,6,8},
    {2,2,4,6},
    {4,2,2,4},
    {6,4,2,2},
    {8,6,4,2},
    {9,7,5,3}
};

static const int mult[4] = {1,10,100,1000};

static inline char can_move_to(const Game* g, char r, char h) {
    if ( h <= r+1 ) {
        for ( char p = h+1; p <= r+1; p++ ) {
            if ( g->hallway[p] != -1 ) {
                return 0;
            }
        }
    } else {
        for ( char p = h-1; p >= r+2; p-- ) {
            if ( g->hallway[p] != -1 ) {
                return 0;
            }
        }
    }
    return 1;
}

static inline char can_enter(const Game* g, char r, char D) {
    for ( char l = D-1; l >= 0; l-- ) {
        if ( g->rooms[r][l] == -1 ) {
            return l;
        } else if ( g->rooms[r][l] != r ) {
            return -1;
        }
    }
    return -1;
}

static inline char can_leave(const Game*g, char r, char D) {
    for ( char l = D-1; l >= 0; l-- ) {
        if ( g->rooms[r][l] == -1 ) {
            return -1;
        } else if ( g->rooms[r][l] != r ) {
            for ( char t = 0; t <= l; t++ ) {
                if ( g->rooms[r][t] != -1 ) {
                    return t;
                }
            }
        }
    }
    return -1;
}

int ab(const Game* g, int cost, int min_cost, Hash* hashtable, char D) {
    char moved = 0;
    char hw_empty = 1;

    if ( cost >= min_cost ) {
        return min_cost;
    }

    hash_t z = hash(g,D);
    if ( hashtable[z].cost < cost ) {
        if ( memcmp(&hashtable[z].entry, g, 7+4*D) == 0 ) {
            return min_cost;
        }
    }

    for ( char h = 0; h <= 6; h++ ) {
        Game tg = *g;
        const char a = tg.hallway[h];
        if ( a != -1 ) {
            hw_empty = 0;
            char enter = can_enter(&tg, a, D);
            if ( enter >= 0 && can_move_to(&tg, a, h) ) {
                int tcost;
                tcost = cost + mult[a] * (dist[h][a] + enter);
                tcost = tcost;
                tg.rooms[a][enter] = a;
                tg.hallway[h] = -1;
                //printf("enter (%d,%d) from %d\n", a, enter, h);
                moved = 1;
                min_cost = imin(ab(&tg, tcost, min_cost, hashtable, D), min_cost);
            }
        }
    }

    for ( char r = 0; r <= 3; r++ ) {
        char leave = can_leave(g, r, D);
        if ( leave >= 0 ) {
            char a = g->rooms[r][leave];
            for ( char h = r+1; h >= 0; h-- ) {
                Game tg = *g;
                int tcost;
                if ( tg.hallway[h] == -1 ) {
                    tcost = cost + mult[a] * (dist[h][r] + leave);
                    tcost = tcost;
                    tg.rooms[r][leave] = -1;
                    tg.hallway[h] = a;
                    //printf("leave (%d,%d) to %d\n", r, leave, h);
                    moved = 1;
                    min_cost = imin(ab(&tg, tcost, min_cost, hashtable, D), min_cost);
                } else {
                    break;
                }
            }
            for ( char h = r+2; h <= 6; h++ ) {
                Game tg = *g;
                int tcost;
                if ( tg.hallway[h] == -1 ) {
                    tcost = cost + mult[a] * (dist[h][r] + leave);
                    tcost = tcost;
                    tg.rooms[r][leave] = -1;
                    tg.hallway[h] = a;
                    //printf("leave (%d,%d) to %d\n", r, leave, h);
                    moved = 1;
                    min_cost = imin(ab(&tg, tcost, min_cost, hashtable, D), min_cost);
                } else {
                    break;
                }
            }
        }
    }

    if ( !moved ) {
        if ( hw_empty ) {
            return cost;
        } else {
            return min_cost;
        }
    }

    hashtable[z].cost = cost;
    memcpy(&hashtable[z].entry, g, 7+4*D);

    return min_cost;
}

int search(const Game* g, int m, int D) {
    Hash* hashtable = malloc(0x8000 * sizeof(Hash));
    for ( int i = 0; i < 0x8000; i++ ) {
        hashtable[i].cost = m;
    }
    int result = ab(g,0,m,hashtable,D);
    /*
    int hc = 0;
    for (int i = 0; i < 0x8000; i++ ) {
        if ( hashtable[i].cost < m ) {
            hc++;
        }
    }
    printf("Hash usage %f percent\n", (double)hc/(double)0x8000*100);
    */
    free(hashtable);
    return result;
}

