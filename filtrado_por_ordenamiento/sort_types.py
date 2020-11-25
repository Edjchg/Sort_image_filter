def merge_sort(list_, left, right):
    if left < right:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = (left + (right - 1)) // 2
        # Recursive call for slicing the list
        merge_sort(list_, left, m)
        merge_sort(list_, m + 1, right)
        # Take everything together
        merge(list_, left, m, right)
    else:
        return list_


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * n1
    R = [0] * n2

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = arr[l + i]

    for j in range(0, n2):
        R[j] = arr[m + 1 + j]

    # Merge the temp arrays back into arr[left..rith]
    # Initial index of first subarray
    i = 0
    # Initial index of second subarray
    j = 0
    # Initial index of merged subarray
    k = l

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def insertion_sort(list_):
    for i in range(1, len(list_)):
        key = list_[i]
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < list_[j]:
            list_[j + 1] = list_[j]
            j -= 1
        list_[j + 1] = key
    return list_


def bubble_sort(list_):
    # This algorithm swap adjacent items of the list if they are in disorder
    # Getting the length of the input list
    length_list = len(list_) - 1
    # While the list is in disorder the algorithm has to sort it:
    while not sort_verifier(list_):
        # Iterate over the list swapping values as it is needed:
        for i in range(length_list):
            a = list_[i]
            b = list_[i + 1]
            if a > b:
                list_[i + 1] = a
                list_[i] = b
            else:
                continue
    return list_


# This function ensures that a list is in order
def sort_verifier(list_):
    # Getting the length of the input list
    length_list = len(list_) - 1
    flag = True
    for i in range(length_list):
        if list_[i] > list_[i + 1]:
            flag = False
            break
        else:
            continue
    return flag


def sort_list_by(list_, type_):
    out_put_list = []
    # Bubble sort
    if type_ == 0:
        out_put_list = bubble_sort(list_)
    # Insertion sort
    elif type_ == 1:
        out_put_list = insertion_sort(list_)
    # Merge sort
    elif type_ == 2:
        merge_sort(list_, 0, len(list_) - 1)
        out_put_list = list_
    return out_put_list
