import numpy as np
import matplotlib.pyplot as plt

n,bins,patches=plt.hist(x,500,normed=1,facecolor='r',alpha=0.75)
plt.xLabel('z')
plt.yLabel('number')
plt.title('Hist of dist')
plt.axis([0,500,0,100])
plt.grid(True)
