"""
This code has the functions: split_line, get_filelist, get_frames, get_men, get_max
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import sys
import psutil


def split_line(line):
    """Gets directory and time points from a single line of string given"""
    if line.find(',') > -1:
       line = line.split(',')
       dir_ = line[0]
       t = line[1]
    else:
        line = line.split('\n')
        dir_ =line[0]
        try:
           t = int(line[1])
        except:
            t = None
            print('Time point not mentioned!')
    return dir_, t

def get_filelist(dir_, filetype='*.tif'):
    """ This returns lists of files in the directory with given file formate (default is .tif) """
    filelist = glob.glob(dir_+filetype)
    return filelist

def get_frames(file_):
    """This reads a stack of images from a given file and returns dictionary of frames."""
    t_dict_single = {}
    stack = io.imread(file_)
    print("reading slices...from shape", stack.shape)
    if psutil.virtual_memory()[2] > 88: #this to avoid malfuntioning due to memory sortage of the computer
        print(f'Program quits for insufficient RAM! >88%!')
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
    """Returns list of mean value(s) of each frame(s) of a given image/stack file"""
    meanlist = []
    print("Listing mean values...")
    if len(imgfile) > 1:
        for slice_pos in imgfile:
            slice_ = np.array(imgfile[slice_pos])
            meanlist.append(slice_.mean())
    else:
        meanlist = np.array(imgfile).mean()
    return meanlist

def get_max(imgfile):
    """Returns lists of max value(s) of each frame(s) of a given image/stack file"""
    maxlist = []
    print('Listing max values...')
    if len(imgfile) > 1:
        for slice_pos in imgfile:
            slice_ = np.array(imgfile[slice_pos])
            maxlist.append(slice_.max())
    else:
        maxlist = np.array(imgfile).max()
    return maxlist

def make_dir_out(dir_in):
    """Makes a new directory named '_out' inside the given path."""
    try:
        os.makedirs(dir_in + '_out\\', exist_ok=True)
        dir_out = (dir_in + '_out\\')
        return dir_out
    except:
        raise IOError(f"Unable to make new directory: {dir_in}")


def save_csv(dir_out, file_names, result):
    """This will save the results in the output folder as a '.csv' format. Filename goes to header"""
    try:
        np.savetxt(f"{dir_out}_Individual_mean_of_{len(file_names)}-files.csv",
                   result, delimiter=",", header=f'{file_names}')
    except:
        print("Problem with saving csv file!")
        exit()


def show_plot(results):

    print('Ploting...')

    # x1 = results[0]
    y1 = results[0]
    y2 = results[1]
    # plt.plot(x1, y1, 'ro')
    plt.plot(y1, 'ro')
    plt.plot(y2, "bs")
    plt.show()

def show_plot_multi(results):

    print('Ploting...')

    for n in range(len(results)):
        y = results[n]
        # plt.plot(x1, y1, 'ro')
        plt.plot(y, 'ro')
    plt.show()

def plot_save_fig(results): #dir_out, no_of_files, results
    """This will plot figure according to the results and saves the figure in the output folder as a '.png' format"""
    try:
        y_value = results[0]
        fig = plt.figure()
        plt.plot(y_value, fmt='rs-', linewidth=2, markersize=5, figure = fig)
        # plt.errorbar(results[0], results[1], yerr = results[2], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg_int_with_time, SD', fontsize=12)
        plt.xlabel('Time (h)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        # plt.savefig(f"{dir_out}_avrg_int_with_SD_from_{no_of_files}-files.png")
        plt.show()
        plt.close()

        # fig = plt.figure()
        # plt.errorbar(results[0], results[1], yerr = results[3], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        # plt.title('Avrg_int_with_time, SEM', fontsize=12)
        # plt.xlabel('Time (h)', fontsize=12)
        # plt.ylabel('Average Int, (Gray value)', fontsize=12)
        # # plt.savefig(f"{dir_out}_avrg_int_with_SE_from_{no_of_files}-files.png")
        # # plt.show()
        # # plt.close()

    except:
        print("Problem with saving figure!")
        exit()


if __name__ == "__main__":

    pass