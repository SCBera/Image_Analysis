from func import *
# from func import get_filelist
# import func

# dir_ = input("Dir>")+'\\'

info = open('info.txt')
# reads file info from file
for line in info:
    splited_line = split_line(line)
    dir_ = splited_line[0]+'\\'
    t = splited_line[1]

    # print(dir_, t)


    filelists = get_filelist(dir_)

    mn_all = []
    mx_all = []
    for file_ in filelists[:1]:
        # print(file_)
        dict_ = get_frames(file_)
        # print(len(dict_))
        mn = get_mean(dict_)
        mx = get_max(dict_)

        mn_all.append(mn)
        mx_all.append(mx)

    # print(np.array(mn_all).T, np.array(mx_all).T)

results = [np.array(mn_all), np.array(mx_all)]


# print(len(results[1]))

show_plot_multi(results[0])


