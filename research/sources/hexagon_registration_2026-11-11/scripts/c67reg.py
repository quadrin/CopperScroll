import numpy as np, sys, pickle
sys.path.insert(0,'/home/claude/dem')
import auto, reg2
D='/mnt/user-data/uploads/Copper Scroll/08 Working files/corona windows 2026-11-11/'
W={'jer':(D+'DF041d_sep67_jericho_oasis_and_scarp_full_x16500_y1500.jpg',16500,1500,1),
   'pl':(D+'DF041d_sep67_plain_deir_hajla_jordan_full_x20500_y4300.jpg',20500,4300,1),
   'eb':(D+'DF041d_sep67_east_bank_kafrein_full_x25000_y1300.jpg',25000,1300,1)}
def prior(s=2.05,th=5.6,p=(19100,3490),g=(31.857,35.461)):
    t=np.radians(th); E,N=auto.T.transform(g[1],g[0])
    M=np.array([[s*np.cos(t),s*np.sin(t)],[s*np.sin(t),-s*np.cos(t)]])
    c=np.array([E,N])-np.array(p)@M
    return np.vstack([M,c])
bbox=(35.30,31.70,35.80,32.00)
if __name__=='__main__':
    A0=prior()
    best=None
    for az in (100,130,160,190,220,250):
        for name in ('jer','eb'):
            P,G,C=reg2.matches([W[name]],A0,bbox,az,35,80,30,0.3,14)
            sh=np.median(G-P@A0,axis=0) if len(P) else (0,0)
            print(az,name,len(P),'c %.2f'%(C.mean() if len(C) else 0),'shift',np.round(sh), 'spread', np.round((G-P@A0).std(0)) if len(P) else '')
