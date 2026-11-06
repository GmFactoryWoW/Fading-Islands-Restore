import sys
sys.path.insert(0,'C:/CoA-Build/boats')
from shoot import *
bx,by,deg=953,-3604,141
r=search(bx,by,deg,False,n=60000,seed=7)
print('APPROACH',len(r));[print(x) for x in r[:4]]
