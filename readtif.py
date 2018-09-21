"""
This code extracts corresponding slices from a series of images stacks and make a
separate stack from it.
Inputs requires:
files derectory that must end with '\', position of the slice/stack need
be extracted, number of files to be read.
The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (64bit), scikit image, numpy
Author: Subhas Ch Bera
Year: September 2018
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os

#import glob

#files = glob.glob("*.tif")
# print(files)


#im = io.imread(Dir + FileName + '.tif')
#img = io.imread('D:/Codes/test_1.tif')
#img = io.imread('D:/Codes/test_stack1.tif')
img = (io.imread('D:/Academics/Codes/test_stack1.tif')[0])
#img = io.imread('D:/Codes/sample_stack1.tif')
print(type(img))
print(img.shape)  # prints the z, y, x dimention of the image file
print(img.min(), img.max(), img.mean(), img.std())
# print(im_new.shape) # prints the z, y, x dimention of the image file
# print(im.shape[0]) # shape[i] where i=0 for Z, i=1 for y and i=2 for x

# io.imshow(im_new) # shows the image
#io.imsave(f"{Dir} {listfiles[1]}_slice_{stack_pos}.tif", im_new)
#io.imsave(f"{Dir} {FileName}_slice_{stack_pos}_stack.tif", new_stack)
#

#
#plt.imshow(im_new, cmap='gray')
# plt.show()  # And window will appear
##plt.savefig(dir + 'output.tif')
