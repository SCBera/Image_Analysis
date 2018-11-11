"""
This code has the functions: get_filelist, get_frames, get_men, get_max
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import sys
import psutil


def get_filelist(dir_, filetype='*.tif'):
    """ This returns lists of files in the directory with given file formate (default is .tif) """
    filelist = glob.glob(dir_+filetype)
    return filelist

def get_frames(file_):
    """This reads a stack of images from a given file and returns dictionary of frames."""
    t_dict_single = {}
    stack = io.imread(file_)
    # print("reading slices...with shape", len(stack.shape))
    if psutil.virtual_memory()[2] > 88: #this to avoid malfuntioning due to memory sortage of the computer
        print(f'Sytem RAM not sufficient! Higher than 88%!')
    elif len(stack.shape) < 3: # this analyzes the stack with shape: (y,x)
        t_dict_single = [stack]
    elif stack.shape[0] > 300: # this analyzes the stack with shape: (y,x,z)
        for slice_t in range(stack.shape[2]):
                t_dict_single[slice_t] = [stack[:, :, slice_t]]
    else: # this analyzes the stack with shape: (z,y,x)
        for slice_t in range(stack.shape[0]):
                t_dict_single[slice_t] = [stack[slice_t]]
    return t_dict_single


def get_mean(imgfile):
    """Returns means of mean of a given image file (stack/frame) """
    meanlist = []
    if len(imgfile) > 1:
        for slice_pos in imgfile:
            slice_ = np.array(imgfile[slice_pos])
            meanlist.append(slice_.mean())
    else:
        meanlist = np.array(imgfile).mean()
    return meanlist

def get_max(imgfile):
    """Returns means of mean of a given image file (stack/frame) """
    maxlist = []
    if len(imgfile) > 1:
        for slice_pos in imgfile:
            slice_ = np.array(imgfile[slice_pos])
            maxlist.append(slice_.max())
    else:
        maxlist = np.array(imgfile).max()
    return maxlist

if __name__ == "__main__":

    pass