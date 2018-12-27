# -*- coding: utf-8 -*-
"""
This code reads ".tif" files/stacks from given directory (excluding the first file).
Extracts slices from stacks and process them to get...
MAX and mean projection of the slices.
Calculate the means, SD, SEM, MAX, SUM value and make array
Save them in a separate folder inside destination folder.


Inputs requires during run:
script -am for automatic mode which will read files and time interval from info.txt file
script -mm for manual input of directory and time interval

The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (64bit), scikit image, numpy, psutil, math, glob, matplotlib.pyplot
Author: Subhas Ch Bera (suggested by Kesavan)
Created on Tue Sep 18 09:02:20 2018
Last updated: 28 September, 2018

"""

from skimage import io
from sys import argv
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import sys
import glob
import psutil
import time



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
        os.makedirs(dir_in + '_out\\', exist_ok=True)
        dir_out = (dir_in + '_out\\')
        return dir_out
    except:
        raise IOError(f"Unable to make new directory: {dir_in}")


def get_filelist(dir_, filetype='*.tif'):
    """This gets the lists of files in the directory given"""
    files = glob.glob(dir_ + filetype)
    # return files[1:] # returns fileslist except the 1st file
    return files


def extract_frames_single_file(file_):
    """This reads a stack of images from a file and returns dictionary of frames."""

    t_dict_single = {}
        
    stack = io.imread(file_)
    
    print("reading slices...")

    if psutil.virtual_memory()[2] > 88:
        print(f'Sytem RAM not sufficient!')
    elif stack.shape[0] > 300: # this analyzes the stack with shape: (y,x,z)
        for slice_t in range(stack.shape[2]):
                t_dict_single[slice_t] = [stack[:, :, slice_t]]
    else: # this analyzes the stack with shape: (z,y,x)
        for slice_t in range(stack.shape[0]):
                t_dict_single[slice_t] = [stack[slice_t]]

    return t_dict_single

def z_project_frames(t_dict_dbl):
    t_dict_z_proj = {}
    for t in t_dict_dbl:
        new_stack_t = np.array(t_dict_dbl[t])

        max_of_stacks = np.max(new_stack_t, axis = 0)
        # mean_of_stacks = np.mean(new_stack_t, axis = 0).astype(float) # converts int/float array to float or trancated int (eg., 2.9 to 2)

        t_dict_z_proj[t] = max_of_stacks
    return t_dict_z_proj


def calculate_mean(t_dict):
    """Reads frames and returns a list of mean intensity values"""
    mean = []
    for t in t_dict:
        slice_ = np.array(t_dict[t])
        # slice_ = np.array(t_dict[t]).astype(float)
        mean.append(slice_.mean())
    return mean


def save_csv(dir_out, files, result):
    """This will save resultant values in the output folder as a '.csv' format"""
    try:
        np.savetxt(f"{dir_out}_Individual_mean_of_{len(files)}-files.csv",
                   result, delimiter=",", header=f'{files}')
    except:
        print("Existing csv file is not accessible!")
        exit()

def list_mean_auto(info_file = 'info.txt'):
        info_file = open('info.txt')
        for line in info_file:

            start_2 = time.time()

            # line = line.split(',')
            dir_ = line[:-1]+'\\'
            # dir_ = get_dir(line[:-1])
            # t = int(line[1])
            # list_of_files = get_filelist(dir_)
            list_of_files = glob.glob(dir_ + '*.tif')

            
            print(f"\nReading {len(list_of_files)} files from '{dir_[-50:]}'\n")

            dir_out = make_dir_out(dir_) # better not to reuse variable names which are same with any function name!
            # that may cause "TypeError: 'str' object is not callable" error.

            mean_all = []
            header_all = []
            for file_ in list_of_files:
                t_dict = extract_frames_single_file(file_)
                mean = calculate_mean(t_dict)
                mean_all.append(mean)
                header_all.append(file_[-21:])
            result = np.array(mean_all).T

            save_csv(dir_out, header_all, result)
        print("\nTime required(sec): ", time.time() - start_2)
         

def list_mean_manual(dir_):
        # dir_ = input("Directory>")+'\\'
        # dir_ = get_dir(input("Directory>"))
        # t = int(input("Time point/interval>"))

        list_of_files = glob.glob(dir_+'*.tif')

        print(f"\nReading {len(list_of_files)} files...\n")

        dir_out = make_dir_out(dir_)

        mean_all = []
        header_all = []
        for file_ in list_of_files:
            t_dict = extract_frames_single_file(file_)
            mean = calculate_mean(t_dict)
            mean_all.append(mean)
            header_all.append(file_[-21:])        
        result = np.array(mean_all).T

        save_csv(dir_out, header_all, result)




if __name__ == "__main__":

    if len(argv) < 2:
        print("Please specify arguments: '-am' for auto-mean, '-mm' for manual-mean.")
        exit()

    elif argv[1] == '-am':
        start_1 = time.time()     
        list_mean_auto()

    elif argv[1] == '-mm':    
        dir_ = input("Directory>")+'\\'        
        start_1 = time.time()
        list_mean_manual(dir_)


    print("\nTotal time required(sec): ", time.time() - start_1)
