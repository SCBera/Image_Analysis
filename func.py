"""
This code has the functions: get_filelist, extract_frames
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

def extract_frames(file_):
    """This reads a stack of images from a file and returns dictionary of frames."""
    t_dict_single = {}
    stack = io.imread(file_)
    # print("reading slices...")
    if psutil.virtual_memory()[2] > 88: #this to avoid malfuntioning due to memory sortage of the computer
        print(f'Sytem RAM not sufficient! Higher than 88%!')
    elif stack.shape[0] > 300: # this analyzes the stack with shape: (y,x,z)
        for slice_t in range(stack.shape[2]):
                t_dict_single[slice_t] = [stack[:, :, slice_t]]
    else: # this analyzes the stack with shape: (z,y,x)
        for slice_t in range(stack.shape[0]):
                t_dict_single[slice_t] = [stack[slice_t]]

    return t_dict_single


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


if __name__ == "__main__":
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
