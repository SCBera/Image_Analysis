"""
This code provides (.csv and plot) average intesity (gray value) of  slices fromm ".tif" stacks
from given directory (excluding the first file).

Can also extracts slices from stacks and make a MAX projection of the slices.
Save it in a separate folder inside destination folder.


Inputs requires during run:
'script -a' for automatic mode then files derectory

'script -(anything)' for manual mode
then files derectory, position of the slice/stack need be analyzed and number of files to be read.

The code is mostly adopted from:http://www.bioimgtutorials.com/2016/08/03/creating-a-z-stack-in-python/
Runs in 64bit environment with Python3 (32/64bit), scikit image, numpy, matplotlib.pyplot, glob
Author: Subhas Ch Bera
Last updated: 16 September, 2018.
"""
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import sys

# This gets the lists of files in the directory given excluding the first file
def get_filelist(Dir, filetype='*.tif'):
    files = glob.glob(Dir+filetype)
    del files[0] # deletes first file form the list
    files_mod = files
    return files_mod

# This function gives average intesity of all the slices of same time point
# from all the files in the above list of files
def get_max_all(filelists):
    img = io.imread(filelists[0])
    mean = []
    mean_all_tm_points = []
    std_all_tm_points = []
    tm_points =[]

    if len(img.shape) < 3:
        print('\nImage is not a stack! Please choose a stack of images.')
        result = img
        return result
    else:
        for slice in range(0, img.shape[0]):
            slice_tm = slice*tm_int
            for n in range(0, len(filelists)):
                img = io.imread(filelists[n])
                new_img = (img[slice])
                filename = ((filelists[n])[(len(filelists[0])-20):])
                print(f"Reading slice-{slice+1} of file ..{filename}")
                img_mean = new_img.mean()  # gets the mean intensity of image
                mean.append(img_mean)
            mean_all = np.array([mean])
            tm_points.append(slice_tm)
            mean_all_tm_points.append(mean_all.mean())
            std_all_tm_points.append(mean_all.std())
        results = np.array([tm_points, mean_all_tm_points, std_all_tm_points])
        try:
            os.makedirs(Dir+'Processed/', exist_ok=True)
            np.savetxt(f"{Dir}Processed/Results_from_{len(filelists)}-files.csv",
                       results.T, delimiter=",", header='Time, Avrg_int, YError')
            #np.savetxt(Dir+'Processed/' + 'Results.csv', (tm_points, mean_all_tm_points, std_all_tm_points),
            #                   delimiter=",", header='Time, Avrg_int, YError')
        except:
            print("Existing results file is not accessible!")
    return results

# This function gives average intesity of selected slice of a time point
# from selected/all the files in the above list of files
def get_max_limited(filelists, slice_pos, nfiles):
    img = io.imread(filelists[0])
    mean = []
    if len(img.shape) < 3:
        print('\nImage is not a stack! Please choose a stack of images.')
        result = img
        return result
    else:
        if slice_pos.lower() != 'all' and nfiles.lower() == 'all':
            for n in range(0, len(filelists)):
                img = io.imread(filelists[n])
                new_img = (img[int(slice_pos)-1])
                filename = ((filelists[n])[(len(filelists[0])-20):])
                print(f"Reading slice-{slice_pos} of file '...{filename}'")
                img_mean = new_img.mean()  # gets the mean intensity of image
                mean.append(img_mean)
            mean_all = np.array([mean])
            results = [mean_all.mean(), mean_all.std()]


        elif slice_pos.lower() != 'all' and nfiles.lower() != 'all':
            for n in range(0, int(nfiles)):
                img = io.imread(filelists[n])
                new_img = (img[int(slice_pos)-1]) #counting starts from 0 in python
                filename = ((filelists[n])[(len(filelists[0])-20):])
                print(f"Reading slice-{slice_pos} of file '...{filename}'")
                img_mean = new_img.mean()  # gets the mean intensity of image
                mean.append(img_mean)
            mean_all = np.array([mean])
            results = [mean_all.mean(), mean_all.std()]
    return results

# This will run if no argument is prodived or the argument is not '-a'
if len(sys.argv) < 2 or sys.argv[1] != '-a':
    Dir = (input('Directory>') + '\\')
    filelists = get_filelist(Dir)
    slice_pos = input('slice_position>')
    nfiles = input('How many files to read>')
    results = get_max_limited(filelists, slice_pos, nfiles)
    print(results)
elif sys.argv[1] == '-a':
    Dir = (input('Directory>') + '\\')
    tm_int = int(input('Time interval between frames>'))
    filelists = get_filelist(Dir)
    results = get_max_all(filelists)
    #plt.plot(results[0], results[1], 'ro-', markersize=3)
    fig = plt.figure()
    plt.errorbar(results[0], results[1], yerr = results[2], fmt='rs-', linewidth=2, markersize=5, figure = fig)
    plt.title('Avrg_int_with_time', fontsize=12)
    #plt.text(0.002,1.035, 'RB', fontsize=12)
    plt.xlabel('Time (min)', fontsize=12)
    plt.ylabel('Average Int, (Gray value)', fontsize=12)
    plt.savefig(f"{Dir}Processed/Results_from_{len(filelists)}-files.png")
    plt.show()
    #fig.close()
    #plt.close("all")

#    print(results[0])
