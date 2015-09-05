#include <math.h>
#include <string.h>
#include <stdio.h>

double max(double x, double y){
    return x > y ? x:y;
}

double min(double x, double y){
    return x < y ? x:y;
}

void c_phansalkar(double* frame, int wsize, int size, unsigned char* ret){
    int i,j,m,n;
    double mean, sdv;
    double k=0.25,r=0.5,p=2,q=10;
    double pixel, th, sum, sum2, num;
    double Max=65537, Min=-1;
    memset(ret, 0, sizeof(ret));
    for (i = 0; i < size; i++)
        for (j = 0; j < size; j++){
            Min = min(Min, frame[i*size+j]);
            Max = max(Max, frame[i*size+j]);
            ret[i*size+j]=0;
        }
            
    for (i = 0; i < size; i++)
        for (j = 0; j < size; j++)
            frame[i*size+j] = (frame[i*size+j] - Min) / (Max - Min);

    for (i = wsize; i < size-wsize; i ++)
        for (j = wsize; j < size-wsize; j ++){

            pixel = frame[i*size+j]; th = 0;
            sum = 0; sum2 = 0;
             
            for(m = i-wsize; m <= i+wsize ; m++)
                for(n = j-wsize; n <= j+wsize ; n++){
                    sum += frame[m*size+n];    
                    sum2 += frame[m*size+n]*frame[m*size+n];
                }
            num = (2*wsize+1)*(2*wsize+1);
            mean = sum/num;
            sdv = sqrt((sum2 - sum*mean)/num);
            th = mean * (1 + p*exp(-q*mean) + k*(sdv/r - 1));
            if (pixel > th)
                ret[i*size+j] = 1;
            else 
                ret[i*size+j] = 0;
        }
}


