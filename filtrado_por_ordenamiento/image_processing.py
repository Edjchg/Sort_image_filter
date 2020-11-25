from sort_types import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import imageio
import time


def linearize_matrix(matrix, with_height):
    out_put_list = [0] * with_height * with_height
    counter = 0
    # Iterate over rows
    for i in range(with_height):
        # Iterate over columns:
        for j in range(with_height):
            out_put_list[counter] = matrix[i][j]
            counter += 1
    return out_put_list


# Generates the kernel of each pixel: i is the row counter, and j is column counter:
def build_kernel(i, j, image, kernel_size):
    x_image_len = len(image[0]) - 1
    y_image_len = len(image) - 1
    out_put_kernel = np.zeros((kernel_size, kernel_size))
    if kernel_size == 3:
        #  __
        # |
        if i == 0 and j == 0:
            n = 1
            while n < kernel_size:
                j_ = j
                m = 1
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and 0 < j < x_image_len:
            j -= 1
            n = 1
            while n < kernel_size:
                j_ = j
                m = 0
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 0 and j == x_image_len:
            j -= 1
            n = 1
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 0 < i < y_image_len and j == 0:
            i -= 1
            n = 0
            while n < kernel_size:
                m = 1
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |__
        elif i == y_image_len and j == 0:
            i -= 1
            n = 0
            while n < kernel_size - 1:
                m = 1
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_image_len and 0 < j < x_image_len:
            i -= 1
            j -= 1
            n = 0
            while n < kernel_size - 1:
                j_ = j
                m = 0
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # ___|
        elif i == y_image_len and j == x_image_len:
            i -= 1
            j -= 1
            n = 0
            while n < kernel_size -1:
                j_ = j
                m = 0
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 0 < i < y_image_len and j == x_image_len:
            i -= 1
            j -= 1
            n = 0
            while n < kernel_size:
                j_ = j
                m = 0
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        else:
            i -= 1
            j -= 1
            i_ = i
            for n in range(kernel_size):
                j_ = j
                for m in range(kernel_size):
                    out_put_kernel[n][m] = image[i_][j_]
                    j_ += 1
                i_ += 1
    # ------------------------------------------------------------------------------------------------------------- #
    if kernel_size == 5:
        #  __
        # |
        if i == 0 and j == 0:
            n = 2
            while n < kernel_size:
                j_ = j
                m = 2
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        #  __
        # |
        elif i == 1 and j == 1:
            n = 1
            i -= 1
            j -= 1
            while n < kernel_size:
                m = 1
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 0 and j == x_image_len:
            n = 2
            j -= 3
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 1 and j == x_image_len - 1:
            n = 1
            j -= 3
            i -= 1
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # |__
        elif i == y_image_len and j == 0:
            i -= 2
            n = 0
            while n < kernel_size - 2:
                j_ = j
                m = 2
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # |__
        elif i == y_image_len - 1 and j == 1:
            j -= 1
            i -= 2
            n = 0
            while n < kernel_size - 1:
                m = 1
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_image_len and j == x_image_len:
            i -= 3
            j -= 3
            n = 0
            while n < kernel_size - 2:
                j_ = j
                m = 0
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_image_len - 1 and j == x_image_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < kernel_size - 2:
                m = 0
                j_ = j
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                 -----
        #                |     |
        elif i == 0 and 1 < j < x_image_len - 1:
            j -= 2
            n = 2
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                 -----
        #                |     |
        elif i == 1 and 1 < j < x_image_len - 1:
            j -= 3
            i -= 1
            n = 1
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1

        #  -----
        # |     |
        elif i == 0 and j == 1:
            j -= 1
            n = 2
            while n < kernel_size:
                m = 1
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                                  -----
        #                                 |     |
        elif i == 0 and j == x_image_len - 1:
            j -= 2
            n = 2
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif i == 1 and j == 0:
            i -= 1
            n = 1
            while n < kernel_size:
                j_ = j
                m = 2
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif i == y_image_len - 1 and j == 0:
            i -= 2
            n = 0
            while n < kernel_size - 1:
                m = 2
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 1 < i < y_image_len - 1 and j == 0:
            i -= 2
            n = 0
            while n < kernel_size:
                j_ = j
                m = 2
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 1 < i < y_image_len - 1 and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < kernel_size:
                j_ = j
                m = 1
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif i == 1 and j == x_image_len:
            i -= 1
            j -= 2
            n = 1
            while n < kernel_size:
                j_ = j
                m = 0
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif i == y_image_len - 1 and j == x_image_len:
            i -= 2
            j -= 2
            n = 0
            while n < kernel_size - 1:
                j_ = j
                m = 0
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 1 < i < y_image_len - 1 and j == x_image_len:
            i -= 2
            j -= 2
            n = 0
            while n < kernel_size:
                j_ = j
                m = 0
                while m < kernel_size - 2:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 1 < i < y_image_len - 1 and j == x_image_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < kernel_size:
                m = 0
                j_ = j
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_image_len and j == 1:
            j -= 1
            i -= 2
            n = 0
            while n < kernel_size - 2:
                j_ = j
                m = 1
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_image_len and j == x_image_len - 1:
            j -= 2
            i -= 2
            n = 0
            while n < kernel_size - 2:
                j_ = j
                m = 0
                while m < kernel_size - 1:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_____|
        elif i == y_image_len and 1 < j < x_image_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < kernel_size - 2:
                j_ = j
                m = 0
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_image_len - 1 and 1 < j < x_image_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < kernel_size - 1:
                m = 0
                j_ = j
                while m < kernel_size:
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        else:
            i -= 2
            j -= 2
            for n in range(kernel_size):
                j_ = j
                for m in range(kernel_size):
                    out_put_kernel[n][m] = image[i][j_]
                    j_ += 1
                i += 1

    return out_put_kernel


def to_grey(img):
    x_len = len(img[0])
    y_len = len(img)
    new_im = np.zeros((y_len, x_len), np.uint8)
    for i in range(y_len):
        for j in range(x_len):
            new_im[j][i] = img[j][i][0]
    return new_im


def open_image(file_path, kernel_size, sort_type, save_path):
    img = mpimg.imread(file_path)
    new_im = to_grey(img)
    kernel = build_kernel(0, 450, new_im, 5)
    print(kernel)
    plt.imshow(new_im, cmap=plt.get_cmap('gray'))
    plt.show()
    start_time = time.time()
    new_image = process_image(new_im, kernel_size, sort_type)
    end_time = time.time() - start_time
    if sort_type == 0:
        sort_type = "Bubble sort"
    elif sort_type == 1:
        sort_type = "Insertion sort"
    elif sort_type == 2:
        sort_type = "Merge sort"

    print("El procesamiento de la imagen duró " + str(end_time) + " segundos, con una ventana de tamaño " + str(
        kernel_size) + " y usando el algoritmo de ordenamiento " + str(sort_type) + ".")
    plt.imshow(new_image, cmap=plt.get_cmap('gray'))
    plt.show()
    new_image.astype(int)
    imageio.imwrite(save_path, new_image)


def process_image(image, kernel_size, sort_type):
    x_len = len(image[0])
    y_len = len(image)
    new_im = np.zeros((y_len, x_len))
    for i in range(y_len):
        for j in range(x_len):
            # Building the kernel for this i,j pixel:
            kernel = build_kernel(i, j, image, kernel_size)
            # Convert the kernel in array:
            kernel_to_array = linearize_matrix(kernel, kernel_size)
            # Sort the array:
            kernel_sorted = sort_list_by(kernel_to_array, sort_type)
            # Find the index of the middle element
            middle_element = kernel_size * kernel_size // 2
            # Find the middle element
            key_element = kernel_sorted[middle_element]
            new_im[i][j] = key_element
    return new_im
