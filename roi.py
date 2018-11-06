from skimage import io
import matplotlib.pyplot as plt
import random
import numpy as np



# def get_shape(stack):
    
#     stack_shape = Z_shape, Y_shape, X_shape
#     return stack_shape

def get_xy(X_shape, Y_shape):
    x_list = []
    y_list = []
    limit = 200
    for n in range(10):
        x = random.choice(range(0, X_shape-limit))
        y = random.choice(range(0, Y_shape-limit))
        x_list.append(x)
        y_list.append(y)
        # print(x_list)
    return [x_list, y_list]


# roi = get_roi(img)
# plt.imshow(roi, cmap='gray')
# plt.show()


if __name__ == "__main__":
        
    stack = io.imread("D:\\Codes\\Image_Analysis\\Sample_stack\\11_first_stack.tif")

    print("Stack shape (Z, Y, X):", stack.shape)

# this will take care of the stack shapes with reverse order, but Z need to be below 500."""
    if stack.shape[0] > 500:
        Y_shape = stack.shape[0]
        X_shape = stack.shape[1]
        Z_shape = stack.shape[2]
    else:
        Z_shape = stack.shape[0]
        Y_shape = stack.shape[1]
        X_shape = stack.shape[2]

    xy_list = get_xy(X_shape, Y_shape)
    x_l, y_l = xy_list[0], xy_list[1]
    # x_l, y_l = [200, 300], [150, 250]



    limit = 200
    roi_mean_all = []
    for slice_ in range(stack.shape[0]):
        slice_ = stack[slice_]
        roi_mean = []
        for (x, y) in zip(x_l, y_l):
            roi = slice_[x:x+limit, y:y+limit]
            roi_mean.append(roi.mean())
        roi_mean_all.append(roi_mean)
        result = np.array(roi_mean_all).T
    # print(result.T)

    for roi in result:

        print("ROI:", roi)
        # fig = plt.figure()
        plt.plot(roi, 'ro')
        # plt.plot(result[0], fmt='rs-', linewidth=2, markersize=5, figure = fig)
        plt.title('Avrg int. with time', fontsize=12)
        plt.xlabel('Time (h)', fontsize=12)
        plt.ylabel('Average Int, (Gray value)', fontsize=12)
        plt.show()
