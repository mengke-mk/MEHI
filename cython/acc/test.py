import numpy as np
from hello import say_hello_to
a = [1,2,3,4]
a = np.array(a, dtype=np.uint16)
print a.dtype
a.astype(np.uint8)
print a.dtype
a = a.astype(np.uint8)
print a.dtype
say_hello_to('mengke')
