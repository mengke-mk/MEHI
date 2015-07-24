#include <cstring>
#include <cstdio>
namespace prepocess{
    class Image{
        public:
        int* data;
        int H,W;
        Image(int* frame, int W, int H){
            this->H = H;
            this->W = W;
            this->data = new int[W*H];
            memcpy(this->data, frame, 4*W*H);
        }
        Image(int W, int H){
            this->W = W;
            this->H = H;
            this->data = new int[W*H];
        }
        int getHeight(){
            return H;
        }
        int getWidth(){
            return W;
        }
        int* getPixels(){
            return data;
        }
        int getPixel(int h, int w){
            if (w < 0) w = 0;
            if (h < 0) h = 0;
            if (w >= this-> W) w = this->W-1;
            if (h >= this-> H) h = this->H-1;
            return this->data[h*W+w];
        }
        void putPixel(int h, int w, int val){
            this->data[h*this->W+w] = val;
        }
        Image copy(){
            Image *ret = new Image(this->W, this->H);
            memcpy(ret->data, this->data, 4*this->W*this->H);
            return *ret;
        }

        void smooth(){
            int *smoothed = new int[this->W * this->H];
            for (int i = 0; i < H; i++)
                for(int j = 0; j < W; j++){
                    smoothed[i*H + j] = this->getPixel(i-1, j-1) + this->getPixel(i-1, j) + this->getPixel(i-1, j+1)
                        + this->getPixel(i, j-1) + this->getPixel(i, j) + this->getPixel(i, j+1)
                        + this->getPixel(i+1, j-1) + this->getPixel(i+1, j) + this->getPixel(i+1, j+1);
                    smoothed[i*H + j] /= 9;
                }
            this->data = smoothed;
        }
    };

    class RollingBall{
        public:
        RollingBall(int radius);
        unsigned char *data;
        int patchwidth;
        int shrinkfactor;
        void buildRollingBall(int ballradius, int arcTrimPer);
    };

    class Rolling_Ball_Background{
        public:
        int radius;
        Image rollBall(RollingBall ball, Image image, Image smallImage);
        Image shrinkImage(Image ip, int shrinkfactor);
        void interpolateBackground(Image background, RollingBall ball);
        void extrapolateBackground(Image background, RollingBall ball);
        Image subtractBackround(Image ip, int ballRadius);
        void run(Image ip, int rd, int* ret);
    };

    class Rolling_Ball_Background_8{
        public:
        int radius;
        Image rollBall(RollingBall ball, Image image, Image smallImage);
        Image shrinkImage(Image ip, int shrinkfactor);
        void interpolateBackground(Image background, RollingBall ball);
        void extrapolateBackground(Image background, RollingBall ball);
        Image subtractBackround(Image ip, int ballRadius);
        void run(Image ip, int rd, int* ret);
    };

}
