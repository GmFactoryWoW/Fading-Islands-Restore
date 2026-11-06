import sys,math,pickle
sys.path.insert(0,'C:/CoA-Build/boats')
import numpy as np
from scipy.signal import fftconvolve
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw
d=np.load('C:/CoA-Build/boats/obs.npz');X0,X1,Y0,Y1=[int(d[k]) for k in('X0','X1','Y0','Y1')]
land,shal,struct,pier=d['land'],d['shal'],d['struct'],d['pier']
H,W=land.shape
hull=pickle.load(open('C:/CoA-Build/boats/hull.pkl','rb'))
DPIER=distance_transform_edt(~pier);SOL=land|struct;DSOL=distance_transform_edt(~SOL)
KS=61
def kernel(poly_local,theta):
    c,s=math.cos(theta),math.sin(theta)
    img=Image.new('L',(2*KS+1,2*KS+1),0);dr=ImageDraw.Draw(img)
    P=[(KS-(s*lx+c*ly),KS-(c*lx-s*ly)) for lx,ly in poly_local]
    dr.polygon(P,fill=255);return np.array(img)>0
def corr(A,K): return fftconvolve(A.astype(np.float32),K[::-1,::-1].astype(np.float32),mode='same')
def freemap(deg,solclear=3.0,pierclear=1.0):
    th=math.radians(deg)+math.pi
    return corr((DSOL<solclear)|(DPIER<pierclear),kernel(hull,th))<0.5
