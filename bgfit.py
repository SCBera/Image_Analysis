

from skimage import io
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
# from lmfit import Model
import glob


def func(x, a, b):
    return a*x + b



stack = io.imread('test_stack1.tif')

frame1 = stack[4]

frame_row = frame1[400]
X = range(frame1.shape[1])
Y = frame_row

params = curve_fit(func, X, Y)
[a,b] = params[0]


#io.imshow(frame1)
print(params)
plt.plot(X, Y, label='BG')
plt.plot(X, func(X, a, b),
         label='Fitted function')

plt.show()