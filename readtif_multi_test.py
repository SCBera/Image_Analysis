# -*- coding: utf-8 -*-
"""
This code reads ".tif" files/stacks from given directory (excluding the first file).
Extracts slices from stacks and process them to get...
MAX and mean projection of the slices.
Calculate the means, SD, SEM, MAX, SUM value and make array
Save them in a separate folder inside destination folder.


Inputs requires during run:
script -a for automatic mode which will read files and time interval from info.txt file
script -m for manual input of directory and time interval

The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (64bit), scikit image, numpy, psutil, math, glob, matplotlib.pyplot
Author: Subhas Ch Bera (and Kesavan)
Created on Tue Sep 18 09:02:20 2018
Last updated: 28 September, 2018

"""

# To Do:
# 1. Use decorators to decorate functions that need to raise IOError.
# 2. Matplotlib, use the fig, ax syntax. Not the plt state function.
# 3. Rewrite the part of the code that requires empty array creation - instead append to a list and convert into an array.
# 4. Input method should be fully automated

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



def get_dir(dir_in='Sample_stack'):
    """This checks the path of the files provided."""
    print(dir_in)

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


def extract_frame(list_of_files):
    """This reads all the stacks in a given directory. Separates each frame from each time poins.
    Gives out a 4D numpy array with total frames, total files, length and width of the image """

    t_dict = {}
    nfiles = 0
    for file_ in list_of_files:
        img = io.imread(file_)
        nfiles += 1

        
        if psutil.virtual_memory()[2] > 88:
            print(f'Sytem RAM not sufficient. Stopes after {nfiles} files!')
            break
        elif img.shape[0] > 300: # this analyzes the stack with shape: (y,x,z)
            for slice_t in range(img.shape[2]):
                if slice_t not in t_dict:
                    t_dict[slice_t] = [img[:, :, slice_t]]
                else:
                    t_dict[slice_t].append(img[:, :, slice_t])
        else: # this analyzes the stack with shape: (z,y,x)
            for slice_t in range(img.shape[0]):
                if slice_t not in t_dict:
                    t_dict[slice_t] = [img[slice_t]]
                else:
                    t_dict[slice_t].append(img[slice_t])

        # print(f"Reading_file..{file_[-19:]}, image_shape:{img.shape}")
    # t_dict = np.array([np.array(t_dict[key_]) for key_ in t_dict])
    return t_dict, nfiles


def calculate_image(t_dict, t):
        t_points = (np.arange(len(t_dict.keys())) * (t/60))

        # new_stack_sum = []
        new_stack_mean = []
        new_stack_max = []

        list_of_mean_all = []
        list_of_max_all = []
        list_of_sum_all = []
        list_of_sd_all = []
        list_of_sem_all = []

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
            list_of_sem_all.append(
                np.array(list_of_mean).std()/math.sqrt(len(list_of_files)))

            # listing sum and max values from all the frames of each time points
            list_of_sum_all.append(new_stack_t.sum())
            list_of_max_all.append(new_stack_t.max())

            # print(f"Analyzing_time_point-{t+1}")

            # sum_of_stacks = np.sum(new_stack_t, axis=0)
            max_of_stacks = np.max(new_stack_t, axis = 0)
            # converts float array to trancated int (eg., 2.9 to 2)
            mean_of_stacks = np.mean(new_stack_t, axis=0).astype(int)
            # mean_of_stacks = np.mean(new_stack, axis = 0).astype(np.float16) # converts 16bit float
            # mean_of_stacks = np.rint(np.mean(new_stack, axis = 0)) # rounding float to float

            # new_stack_sum.append(sum_of_stacks)
            new_stack_mean.append(mean_of_stacks)
            new_stack_max.append(max_of_stacks)

        # saving the calculated stacks in a csv
        result_csv = np.array([t_points, list_of_mean_all, list_of_sd_all,
                               list_of_sem_all, list_of_sum_all, list_of_max_all])
        return [result_csv, new_stack_mean, new_stack_max]


def save_tif(dir_out, no_of_files, result, mode):
    """This will save resultant frame or stack in the output folder as '.tif' format"""
    try:
        path = f"{dir_out}{mode}_from_{no_of_files}-files.tif"
        io.imsave(path, result)
    except:
        # raise error here.
        print("Existing image file is not accessible!")
        exit()


def save_csv(dir_out, no_of_files, result):
    """This will save resultant values in the output folder as a '.csv' format"""
    try:
        np.savetxt(f"{dir_out}_results_from_{no_of_files}-files.csv",
                   result.T, delimiter=",", header='Time(h), Avrg_int, SD, SE, Sum_int, Max_int')
    except:
        print("Existing csv file is not accessible!")
        exit()


def plot_save_fig(dir_out, no_of_files, results):
    """This will plot figure according to the results and saves the figure in the output folder as a '.png' format"""
    try:
        fig = plt.figure()
        plt.errorbar(results[0], results[1], yerr = results[2], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg_int_with_time, SD', fontsize=12)
        plt.xlabel('Time (h)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        plt.savefig(f"{dir_out}_avrg_int_with_SD_from_{no_of_files}-files.png")
        # plt.show()
        # plt.close()

        fig = plt.figure()
        plt.errorbar(results[0], results[1], yerr = results[3], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg_int_with_time, SEM', fontsize=12)
        plt.xlabel('Time (h)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        plt.savefig(f"{dir_out}_avrg_int_with_SE_from_{no_of_files}-files.png")
        # plt.show()
        # plt.close()

    except:
        print("Problem with saving figure!")
        exit()




if __name__ == "__main__":

    if len(argv) < 2:
        print("Please define arguments: '-a' for auto, '-m' for manual.")
        exit()

    elif argv[1] == '-a':
        start_1 = time.time()

        info_file = open('info.txt')
        for line in info_file:

            start_2 = time.time()

            line = line.split(',')
            dir_ = get_dir(line[0])
            t = int(line[1])
            list_of_files = get_filelist(dir_)
            dir_out = make_dir_out(dir_) # better not to reuse variable names which are same with any function name!
            # that may cause "TypeError: 'str' object is not callable" error.

            print(f"\nReading files from..{dir_[40:]}\n")

            t_dict = extract_frame(list_of_files)[0]
            no_of_files_analysed = extract_frame(list_of_files)[1]

            new_stack_all = calculate_image(t_dict, t)

            # saving the resultent stacks in tif_stack
            save_tif(dir_out, no_of_files_analysed, np.array(new_stack_all[2]), 'Max')
            save_tif(dir_out, no_of_files_analysed, np.array(new_stack_all[1]), 'Mean')
            # save_tif(dir_out, list_of_files, np.array(new_stack_sum, np.uint32), 'Sum')

            save_csv(dir_out, no_of_files_analysed, new_stack_all[0])
            plot_save_fig(dir_out, no_of_files_analysed, new_stack_all[0])

            # this erase the existing memory or frees the RAM
            t_dict = 0
            
            print("\nTime required(sec): ", time.time() - start_2)
           

    elif argv[1] == '-m':
        dir_ = get_dir(input("Directory>"))
        t = int(input("Time point/interval>"))

        start_1 = time.time()
        list_of_files = get_filelist(dir_)

        print("\nReading files...\n")

        dir_out = make_dir_out(dir_)

        t_dict = extract_frame(list_of_files)
        no_of_files_analysed = extract_frame(list_of_files)[1]


        new_stack_all = calculate_image(t_dict, t)

        # saving the resultent stacks in tif_stack
        save_tif(dir_out, no_of_files_analysed, np.array(new_stack_all[2]), 'Max')
        save_tif(dir_out, no_of_files_analysed, np.array(new_stack_all[1]), 'Mean')
        # save_tif(dir_out, list_of_files, np.array(new_stack_sum, np.uint32), 'Sum')

        save_csv(dir_out, no_of_files_analysed, new_stack_all[0])
        plot_save_fig(dir_out, no_of_files_analysed, new_stack_all[0])

    

    print("\nTotal time required(sec): ", time.time() - start_1)
