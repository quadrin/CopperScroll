import sys; sys.path.insert(0, sys.argv[1])
from tfmini import *
T = sys.argv[2]
print(load_otype(T))
