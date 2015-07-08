import pandas as pd
p = []
columns = ('x', 'y')
ind = []
for i in range(0,20):
    p.append([i,-i])
    ind.append(i*10)
ap = pd.DataFrame([], index=[])
ind = pd.Index(ind, name='l')
p = pd.DataFrame(p, index=ind, columns=columns)
t = p[['x','y']].copy()
for i, row in t.iterrows():
    print i, row['x'],row['y']
print t.loc[120]['x']
print t.index[0]
