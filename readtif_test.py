from func import *
# from func import get_filelist
# import func

dir_ = input("Dir>")+'\\'

filelists = get_filelist(dir_)

for file_ in filelists:
    print(file_)
    dict_ = get_frames(file_)
    print(len(dict_))
    mean = get_mean(dict_)
    max = get_max(dict_)

print(mean, max)

