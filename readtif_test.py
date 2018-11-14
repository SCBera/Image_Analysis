from func import *
# from func import get_filelist
# import func

info = open('info.txt')
# reading file info from file
for line in info:
    splited_line = split_line(line)
    dir_ = splited_line[0]
    try:
        t = float(splited_line[1])
        print(t)
    except:
        print('Time point not mentioned!')

# dir_ = input("Dir>")+'\\'

# filelists = get_filelist(dir_)

# for file_ in filelists:
#     print(file_)
#     dict_ = get_frames(file_)
#     print(len(dict_))
#     mean = get_mean(dict_)
#     max = get_max(dict_)

    print(dir_)

