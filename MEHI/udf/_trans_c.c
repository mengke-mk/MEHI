#include <math.h>

void c_trans8(unsigned char* frame, double *U, unsigned char *ret, int m){
    int i, j;
    int x, y;
    for (i = 0; i < m; i++){
        for(j = 0; j < m; j ++){
            x = round(U[0] * i + U[1] * j + U[2]);
            y = round(U[3] * i + U[4] * j + U[5]);
            if(0 <= x && x < m && 0 <= y && y < m)
                ret[x*m+y] = frame[i*m+j];
        } 
    }
    return;
}

void c_trans16(unsigned short* frame, double *U, unsigned short *ret, int m){
    int i, j;
    int x, y;
    for (i = 0; i < m; i++){
        for(j = 0; j < m; j ++){
            x = round(U[0] * i + U[1] * j + U[2]);
            y = round(U[3] * i + U[4] * j + U[5]);
            if(0 <= x && x < m && 0 <= y && y < m)
                ret[x*m+y] = frame[i*m+j];
        } 
    }
    return;
}


