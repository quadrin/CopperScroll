# Decode Copernicus GLO-30 COG (deflate + floating-point predictor 3) without imagecodecs.
import tifffile,numpy as np,zlib,sys
def read(f):
    with tifffile.TiffFile(f) as t:
        p=t.pages[0]
        H,W=p.shape; tw,tl=p.tilewidth,p.tilelength
        tie=p.tags['ModelTiepointTag'].value; sc=p.tags['ModelPixelScaleTag'].value
        fh=t.filehandle
        out=np.zeros((H,W),np.float32)
        nx=(W+tw-1)//tw; ny=(H+tl-1)//tl
        for i,(off,n) in enumerate(zip(p.dataoffsets,p.databytecounts)):
            ty,tx=divmod(i,nx)
            fh.seek(off); raw=zlib.decompress(fh.read(n))
            b=np.frombuffer(raw,np.uint8).reshape(tl,4*tw)
            b=np.cumsum(b,axis=1,dtype=np.uint8)   # undo byte differencing (mod 256)
            planes=b.reshape(tl,4,tw).transpose(0,2,1)  # MSB plane first
            v=planes.copy().view('>f4').reshape(tl,tw)
            y0,x0=ty*tl,tx*tw
            out[y0:y0+tl,x0:x0+tw]=v[:min(tl,H-y0),:min(tw,W-x0)]
        return out,(tie[3],tie[4],sc[0],sc[1])
if __name__=='__main__':
    a,g=read(sys.argv[1]); print(a.shape,a.min(),a.max(),g)
