from roadgeometry import RoadLine, RoadArc
import matplotlib.pyplot as plt
import math

road1 = RoadLine(0, 7.0710678120487289e+00, 7.0710678117015151e+00, 3.9269908169686372e+00, 4.8660000002387466e-01)
road5 = RoadLine(1.6031224248136859e+01, -6.7269902520731444e+00, 6.7269896521996131e+00, 2.3561944901771223e+00, 4.8660000002378739e-01)

road3 = RoadArc(3.6612031746270493e+00,
                4.3409250448908985e+00,
                4.6416930097877751e+00,
                3.7254287106480075e+00,
                9.1954178989066371e+00,
                -1.2698412698412698e-01)

# roada = RoadArc(0, 0, 1, math.pi, 28, -1.2698412698412698e-01)

road1.graph()
road5.graph()
road3.graph()

plt.xlim(-10, 10)
plt.ylim(0, 20)
plt.show()
