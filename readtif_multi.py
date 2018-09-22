# -*- coding: utf-8 -*-
"""
This code reads ".tif" files/stacks from given directory (excluding the first file).
Extracts slices from stacks and make a MAX projection of the slices.
Save it in a separate folder inside destination folder.


Inputs requires during run:
script -a for automatic mode then files derectory

script -(anything) for manual mode then files derectory that must end with '\' and
position of the slice/stack need be extracted, number of files to be read.

The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (64bit), scikit image, numpy, psutil, math, glob, matplotlib.pyplot
Author: Subhas Ch Bera (and Kesavan)
Created on Tue Sep 18 09:02:20 2018
Last updated: 21 September, 2018

"""

# To Do:
# 1. Use decorators to decorate functions that need to raise IOError.
# 2. Matplotlib, use the fig, ax syntax. Not the plt state function.
# 3. Rewrite the part of the code that requires empty array creation - instead append to a list and convert into an array.
# 4. Input method should be fully automated

from skimage import io
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


def dir_out(dir_in):
    """This makes a new directory '_out' inside the given path."""
    try:
        os.makedirs(dir_ + '_out/', exist_ok=True)
        dir_out = (dir_ + '_out/')
        return dir_out
    except:
        raise IOError(f"Unable to make new directory: {dir_in}")


def get_filelist(dir_, filetype='*.tif'):
    """This gets the lists of files in the directory given (excluding the first file)
    """
    files = glob.glob(dir_ + filetype)
    return files[1:]


def extract_frame(list_of_files):
    """This reads all the stacks in a given directory. Separates each frame from each time poins.
    Gives out a 4D numpy array with total frames, total files, length and width of the image """

    t_dict = {}
    nfiles = 0
    for file_ in list_of_files:
        img = io.imread(file_)
        nfiles += 1

        if img.shape[0] > 300:
            print('Stack shape is different!')
            exit()
        elif psutil.virtual_memory()[2] > 80:
            print(f'Sytem RAM not sufficient. Stopes after {nfiles} files!')
            break
        else:
            for slice_t in range(img.shape[0]):
                if slice_t not in t_dict:
                    t_dict[slice_t] = [img[slice_t]]
                else:
                    t_dict[slice_t].append(img[slice_t])

        # print(f"Reading_file..{file_[-19:]}, image_shape:{img.shape}")
    # t_dict = np.array([np.array(t_dict[key_]) for key_ in t_dict])
    return t_dict


def save_tif(dir_out, list_of_files, result, mode):
    """This will save resultant frame or stack in the output folder as '.tif' format"""
    try:
        path = f"{dir_out}{mode}_from_{len(list_of_files)}-files.tif"
        io.imsave(path, result)
    except:
        # raise error here.
        print("Existing image file is not accessible!")
        exit()


def save_csv(dir_out, list_of_files, result):
    """This will save resultant values in the output folder as a '.csv' format"""
    try:
        np.savetxt(f"{dir_out}_results_from_{len(list_of_files)}-files.csv",
                   result.T, delimiter=",", header='Time, Avrg_int, SD, SE, Sum_int, Max_int')
    except:
        print("Existing csv file is not accessible!")
        exit()


def plot_save_fig(dir_out, filelists, results):
    """This will plot figure according to the results and saves the figure in the output folder as a '.png' format"""
    try:
        fig = plt.figure()
        plt.errorbar(results[0], results[1], yerr = results[2], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg_int_with_time, SD', fontsize=12)
        plt.xlabel('Time (min)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        plt.savefig(f"{dir_out}_avrg_int_with_SD_from_{len(filelists)}-files.png")
        # plt.show()
        # plt.close()

        fig = plt.figure()
        plt.errorbar(results[0], results[1], yerr = results[3], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg_int_with_time, SEM', fontsize=12)
        plt.xlabel('Time (min)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        plt.savefig(f"{dir_out}_avrg_int_with_SE_from_{len(filelists)}-files.png")
        # plt.show()
        # plt.close()

    except:
        print("Problem with saving figure!")
        exit()




if __name__ == "__main__":
    dir_ = get_dir(input("Directory>"))
    t = int(input("Time point/interval>"))

    start = time.time()
    list_of_files = get_filelist(dir_)
    dir_out = dir_out(dir_)

    # new_stack_sum = []
    new_stack_mean = []
    new_stack_max = []

    list_of_mean_all = []
    list_of_max_all = []    
    list_of_sum_all = []
    list_of_sd_all = []
    list_of_sem_all = []
 
    print("\nReading files...\n")
    
    t_dict = extract_frame(list_of_files)

    # t_points = (np.arange(len(t_dict)) * t)
    t_points = (np.arange(len(t_dict.keys())) * t)

    print("\nAnalyzing time points...\n")

    for t in t_dict:

        new_stack_t = np.array(t_dict[t])

        list_of_mean = []

        # calculates values for each frame of each time points and lists them
        #
        for n in range(len(new_stack_t)):
            slice_ = new_stack_t[n]
            slice_ = slice_[slice_ > 0]

            list_of_mean.append(slice_.mean())

        # calculates mean and sd from all the frames(mean) of a time point and makes lists of
        # the values of each time points
        list_of_mean_all.append(np.array(list_of_mean).mean())
        list_of_sd_all.append(np.array(list_of_mean).std())
        list_of_sem_all.append(np.array(list_of_mean).std()/math.sqrt(len(list_of_files)))

        # listing sum and max values from all the frames of each time points
        # list_of_sum_all.append(new_stack_t.sum())
        list_of_max_all.append(new_stack_t.max())

        # print(f"Analyzing_time_point-{t+1}")

        # sum_of_stacks = np.sum(new_stack_t, axis = 0)
        max_of_stacks = np.max(new_stack_t, axis = 0)
        mean_of_stacks = np.mean(new_stack_t, axis = 0).astype(int) # converts float array to trancated int (eg., 2.9 to 2)
    #        mean_of_stacks = np.mean(new_stack, axis = 0).astype(np.float16) # converts 16bit float
    #        mean_of_stacks = np.rint(np.mean(new_stack, axis = 0)) # rounding float to float

        # new_stack_sum.append(sum_of_stacks)
        new_stack_mean.append(mean_of_stacks)
        new_stack_max.append(max_of_stacks)

    # saving the calculated stacks in a csv
    result_csv = np.array([t_points, list_of_mean_all, list_of_sd_all, list_of_sem_all, list_of_sum_all, list_of_max_all])

    # saving the resultent stacks in tif_stack
    save_tif(dir_out, list_of_files, np.array(new_stack_max), 'Max')
    save_tif(dir_out, list_of_files, np.array(new_stack_mean), 'Mean')
    # save_tif(dir_out, list_of_files, np.array(new_stack_sum, np.uint32), 'Sum')

    save_csv(dir_out, list_of_files, result_csv)
    plot_save_fig(dir_out, list_of_files, result_csv)

    

# if __name__ == "__main__":
#     # This will run if no argument is prodived or the argument is not '-a'
#     if len(sys.argv) < 2 or sys.argv[1] != '-a':
#         Dir = (input('Directory>') + '\\')
#     #    Dir = dir.replace('\\', '/')
#         filelists = get_filelist(Dir)
#         slice_pos = input('slice_position>')
#         nfiles = input('How many files to read>')
#         result = get_max_limited(filelists, slice_pos, nfiles)
#     #    plt.imshow(result, cmap='gray')
#     #    plt.show()
#     elif sys.argv[1] == '-a':
#         Dir = (input('Directory>') + '\\')
#         tm_int = int(input('Time interval between frames>'))
#         filelists = get_filelist(Dir)
#         results = get_max_all(filelists)


    print("\nTotal time : ", time.time() - start)