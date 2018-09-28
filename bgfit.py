

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
# from lmfit import Model
import glob
import os

def get_dir(dir_in):
    """This checks the path of the files provided."""

    if os.path.isdir(dir_in) == True:
        dir_ = dir_in + "\\"
        return dir_
    else:
        # raise IOError(f"No such directory found: {dir_in}")
        print(f"No such directory found: {dir_in}")
        exit()

def make_dir_out(dir_in):
    """This makes a new directory '_out' inside the given path."""
    try:
        os.makedirs(dir_ + '_out\\', exist_ok=True)
        dir_out = (dir_ + '_out\\')
        return dir_out
    except:
        raise IOError(f"Unable to make new directory: {dir_in}")

def get_filelist(dir_, filetype='*.tif'):
    """This gets the lists of files in the directory given (excluding the first file)
    """
    files = glob.glob(dir_ + filetype)
    return files[1:]


def func(x, a, b, c):
    return a*x*x + b*x + c

def get_row(frame):

    X = range(frame1.shape[1])
    n = 0
    fit_data = []

    for row in frame:
        Y = row
        params = curve_fit(func, X, Y)
        [a,b,c] = params[0]
        fit_data.append(func(X, a, b, c))
        #fit_data = np.array([list(X), func(X, a, b, c)])
        #
    return np.array(fit_data)


#        n += 1
#        print(f"row-{n}:", row)


def save_csv(dir_out, result):
    """This will save resultant values in the output folder as a '.csv' format"""
    try:
        # np.savetxt(f"{dir_out}_results_from_{len(list_of_files)}-files.csv",
        #            result.T, delimiter=",", header='Time(h), Avrg_int, SD, SE, Sum_int, Max_int')
        np.savetxt(f"{dir_out}bg_fit_data.csv", result.T, delimiter=",", header='X, fit_data')
    except:
        print("Existing csv file is not accessible!")
        exit()


def save_tif(dir_out, result):
    """This will save resultant frame or stack in the output folder as '.tif' format"""
    try:
        path = f"{dir_out}_bg-file.tif"
        io.imsave(path, result)
    except:
        # raise error here.
        print("Existing image file is not accessible!")
        exit()



dir_ = get_dir(input('Dir>'))
list_of_files = get_filelist(dir_)
dir_out = make_dir_out(dir_)


#stack = io.imread('test_stack1.tif')
stack = io.imread(list_of_files[0])


frame1 = stack[0]
#print(frame1)
#get_row(frame1)
frame_row = frame1[100]
X = range(frame1.shape[1])
Y = frame_row

params = curve_fit(func, X, Y)
[a,b,c] = params[0]


#io.imshow(frame1)
#print(params)
plt.plot(X, Y, label='BG')
plt.plot(X, func(X, a, b, c),
         label='Fitted function')

plt.show()

bg_img = get_row(frame1)

print(bg_img.shape)

#io.imread(bg_img)
save_tif(dir_out, bg_img)
io.imshow(bg_img, cmap='gray')

#fit_data = func(X, a, b, c)
##fit_data = np.array([list(X), func(X, a, b, c)])
##
#print(len(fit_data))
#
#save_csv(dir_out, fit_data)
##print(list(X), func(X, a, b, c))
#
##print(np.array([list(X)], func(X, a, b, c)))




















