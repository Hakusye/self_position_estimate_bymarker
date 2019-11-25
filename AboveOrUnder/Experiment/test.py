import numpy as np
from pprint import pprint
import math
Predicted = 160.0
xst = math.radians(45.0)
yst = math.radians(30.0)
Xrange = 2 * Predicted * math.tan(xst/2)
Yrange = 2 * Predicted * math.tan(yst/2)
print("X:"+str(Xrange)+"\nY:"+str(Yrange))