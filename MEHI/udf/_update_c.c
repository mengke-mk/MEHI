#include <math.h>
#include <string.h>

double c_update(unsigned char* imgA, unsigned char* imgB, double *U, int n){
    double H[256][256];
    int i,j;
    double x,y;
    for (i = 0; i < 256; i++)
        for(j = 0; j < 256; j++)
            H[i][j] = 0;
    for (i = 0; i < n*n; i++){
        H[imgA[i]][imgB[i]] += 1;
    }
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++){
            x = U[0] * i + U[1] * j + U[2];
            y = U[3] * i + U[4] * j + U[5];
            double dx = x - floor(x);
            double dy = y - floor(y);
            if (x <= 0 || x >= n-1 || y <= 0 || y >= n-1){
                H[imgA[0]][imgA[0]] +=1;
            }else{
                H[imgA[(int)(floor(x)*n+floor(y))]][imgB[i*n+j]] += (1-dx)*(1-dy);
                H[imgA[(int)(floor(x)*n+ceil(y))]][imgB[i*n+j]] += dx*(1-dy);
                H[imgA[(int)(ceil(x)*n+floor(y))]][imgB[i*n+j]] += (1-dx)*dy;
                H[imgA[(int)(ceil(x)*n+ceil(y))]][imgB[i*n+j]] += dx*dy;
            }
        }
    double tot = 0;
    for(i = 0; i < 256; i++)
        for( j = 0 ; j < 256; j++)
            tot += H[i][j];
    double A[256],B[256];
    double HAB = 0,HA = 0,HB = 0;
    memset(A,0,sizeof(A));
    memset(B,0,sizeof(B));
    for(i = 0 ; i < 256; i++)
        for(j = 0; j < 256; j++){
            H[i][j] /= tot;
            A[i] += H[i][j];
            B[j] += H[i][j];
            if (H[i][j] > 1e-7)
                HAB += -H[i][j]*(log(H[i][j])/log(2));
            else
                HAB += 0;
        }
    for(i = 0; i < 256; i++){
        if(A[i] > 1e-7)
            HA += -A[i]*(log(A[i])/log(2));
        else
            HA += 0;
        if(B[i] > 1e-7)
            HB += -B[i]*(log(B[i])/log(2));
        else
            HB += 0;
    }
    return HAB-HA-HB;
}
