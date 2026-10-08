import math
Z=16; X0=39213; Y0=26634
def ll2px(lat, lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n
    return (x-X0)*256, (y-Y0)*256
def px2ll(px, py):
    n=2**Z; x=px/256+X0; y=py/256+Y0
    return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))), x/n*360-180
def m_per_px(lat):
    return 156543.03392*math.cos(math.radians(lat))/2**Z
