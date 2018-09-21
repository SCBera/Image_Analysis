"""
This code reads ".tif" files/stacks from given directory (excluding the first file).
Extracts slices from stacks and make a MAX projection of the slices.
Save it in a separate folder inside destination folder.


Inputs requires during run:
script -a for automatic mode then files derectory

script -(anything) for manual mode then files derectory that must end with '\' and
position of the slice/stack need be extracted, number of files to be read.

The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (64bit), scikit image, numpy
Author: Subhas Ch Bera
Last updated: September 2018
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import sys

#files = glob.glob(Dir+filetype)
#print(files)
# This gets the lists of files in the directory given with first file name removed
def get_filelist(Dir, filetype='*.tif'):
    files = glob.glob(Dir+filetype)
    del files[0] # deletes first file form the list
    files_mod = files
    return files_mod

# This function gives out of the MAX projection of all the individual slices
# from all the files in the above list of files
def get_max_all(filelists):
    img = io.imread(filelists[0])
    #print('image_shape:', img.shape[0])
    if len(img.shape) < 3:
        print('\nImage is not a stack! Please choose a stack of images.')
        result = img
        return result
    else:
        stack = np.zeros((len(filelists), img.shape[1], img.shape[2]), img.dtype)
        for slice in range(0, img.shape[0]):
            for n in range(0, len(filelists)):
                img = io.imread(filelists[n])
                new_img = (img[int(slice)]) #counting starts from 0 in python
                print(f"reading file no.{n+1}")
                stack[n, :, :] = new_img
            im_max= np.max(stack, axis=0)
            os.makedirs(Dir+'Processed/', exist_ok=True)
            io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice-{slice+1}_from_{len(filelists)}-files.tif", im_max)
            #io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice_{slice}_{len(filelists)}_files.tif", stack)

        return im_max

# This function gives out of the MAX projection of selective slices
# from selective/all the files in the above list of files
def get_max_limited(filelists, slice_pos, nfiles):
    img = io.imread(filelists[0])
    #print('image_shape:', img.shape)
    if len(img.shape) < 3:
        print('\nImage is not a stack! Please choose a stack of images.')
        result = img
        return result
    else:
        stack = np.zeros((len(filelists), img.shape[1], img.shape[2]), img.dtype)
        if slice_pos.lower() != 'all' and nfiles.lower() == 'all':
            for n in range(0, len(filelists)):
                img = io.imread(filelists[n])
                new_img = (img[int(slice_pos)-1]) #counting starts from 0 in python
                print(f"reading file no.{n+1}")
                stack[n, :, :] = new_img
            im_max= np.max(stack, axis=0)
            os.makedirs(Dir+'Processed/', exist_ok=True)
            #io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice_{slice_pos}_{len(filelists)}_files.tif", stack)
            io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice-{slice_pos}_from_{len(filelists)}-files.tif", im_max)

        elif slice_pos.lower() != 'all' and nfiles.lower() != 'all':
            for n in range(0, int(nfiles)):
                img = io.imread(filelists[n])
                new_img = (img[int(slice_pos)-1]) #counting starts from 0 in python
                print(f"reading file no.{n+1}")
                stack[n, :, :] = new_img
            im_max= np.max(stack, axis=0)
            os.makedirs(Dir+'Processed/', exist_ok=True)
            io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice-{slice_pos}_from_{nfiles}-files.tif", im_max)
            #io.imsave(f"{Dir+'Processed/'}Max_stack_of_slice_{slice_pos}_{nfiles}_files.tif", stack)

    return im_max

# This will run if no argument is prodived or the argument is not '-a'
if len(sys.argv) < 2 or sys.argv[1] != '-a':
    Dir = (input('Directory>') + '\\')
#    Dir = dir.replace('\\', '/')
    filelists = get_filelist(Dir)
    slice_pos = input('slice_position>')
    nfiles = input('How many files to read>')
    result = get_max_limited(filelists, slice_pos, nfiles)
#    plt.imshow(result, cmap='gray')
#    plt.show()
elif sys.argv[1] == '-a':
    Dir = (input('Directory>') + '\\')
#    Dir = dir.replace('\\', '/')
    filelists = get_filelist(Dir)
    result = get_max_all(filelists)
#    plt.imshow(result, cmap='gray')
#    plt.show()
#else: # if the argument is not '-a'
#    dir = (input('Directory>') + '\\')
#    Dir = dir.replace('\\', '/')
#    filelists = get_filelist(Dir)
#    slice_pos = input('slice_position>')
#    nfiles = input('How many files to read>')
#    result = get_max_limited(filelists, slice_pos, nfiles)
#    plt.imshow(result, cmap='gray')
#    plt.show()

#img = io.imread(filelists[0])
#print('dtype:', img.dtype)
#print('image_shape:', img.shape)
