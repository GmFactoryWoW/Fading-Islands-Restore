import sys
sys.path.insert(0,'C:/CoA-Build/boats')
import wmo_geo as g
from PIL import Image,ImageDraw
BS=chr(92)
t=g.load(BS.join(['world','wmo','kalimdor','lostisles','goblin_riverboat.wmo']))
S=28
def view(ax,ay,flipy,out):
    vs=[v for x in t for v in x]
    mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
    W=int((mx[ax]-mn[ax])*S)+20;H=int((mx[ay]-mn[ay])*S)+20
    img=Image.new('RGB',(W,H),(15,15,20));d=ImageDraw.Draw(img)
    P=lambda v:((v[ax]-mn[ax])*S+10,(mx[ay]-v[ay])*S+10)
    for tr in t: d.polygon([P(v) for v in tr],outline=(120,170,230))
    d.text((4,2),'axes %d(right) %d(up)  min %s'%(ax,ay,[round(m,1) for m in mn]),fill=(255,255,255))
    img.save(out)
view(0,1,0,'C:/CoA-Build/boats/rb_top2.png')   # X right, Y up
view(1,2,0,'C:/CoA-Build/boats/rb_side2.png')  # Y right, Z up
