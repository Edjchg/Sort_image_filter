# Instituto Tecnológico de Costa Rica               #
# Curso:                                            #
# Escuela de                                        #
# Proyecto:                                         #
# Estudiante:                                       #
# Carné:                                            #
# Fecha:                                            #
#####################################################
# Este script contiene todos los metodos o funciones necesarias para el procesado de imagenes por ordenamiento:
# 0) Como etapa preliminar se encuentran las bibliotecas utilizadas para el uso de imagenes: matplotlib(convertir imagenes
#    a gris), numpy (para la elaboración de estructuras de datos en dos dimensiones como lo son las matrices), imageio (para
#    abrir y escribir imagenes en disco duro) y finalmente time( para la toma del tiempo)
# 1) Primero se encuentran los algoritmos de ordenamiento de listas o arreglos de datos: Bubble, Insertion y Merge sort.
# 2) Como segunda parte estan los algoritmos de creacion de kernels o ventanas de filtrado tanto para tamaños de
#    3x3, 5x5 y 7x7.
# 3) Finalmente se encuentra la etapa de interacción con el usuario, en la cual se van a tomar como entradas:
#    -La ruta de la imagen de entrada, el tipo de ordenamiento que se desee, el tamaño de la ventana o kernel y finalmente
#     la ruta y nombre que se le dará a la imagen de salida.
# --------------------------------------Parte 0: Uso de bibliotecas----------------------------------------------------#
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import imageio
import time


# --------------------------------------Parte 1: Algoritmos de ordenamiento--------------------------------------------#
# Esta funcion recibe como para metros una lista, a su vez el parámetro l, que 
# es la frontera izquierda o el inicio de la lista y r es el final de la lista.
# Se deben de pasar esos argumentos por la naturaleza recursiva de este algoritmo.
def merge_sort(list_, left, right):
    if left < right:
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = (left + (right - 1)) // 2
        # Recursive call for slicing the list
        merge_sort(list_, left, m)
        merge_sort(list_, m + 1, right)
        # Take everything together
        merge_aux(list_, left, m, right)
    else:
        return list_


# Esta función toma la lista entera y la parte según los valores de l(left), 
# r(right), y m que corresponde al elemento medio de las lista.
        
def merge_aux(arr, l, m, r):
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

    # Merge the temp arrays back into arr[left..right]
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

# Esta funcion ordena la lista con el algoritmo de Insertion sort.
# Recibe una lista.
# Retorna una lista ordenada.
def insertion_sort(list_):
    # Se recorre la lista:
    for i in range(1, len(list_)):
        key = list_[i]
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        j = i - 1
        # Corre los elementos una posición a la derecha para poder insertar 
        # el valor correspondiente en esa sección de la lista:
        while j >= 0 and key < list_[j]:
            list_[j + 1] = list_[j]
            j -= 1
        list_[j + 1] = key
    return list_

# Esta función ordena una lista con el algoritmo de Bubble sort.
# Recibe una lista.
# Retorna una lista ordenada.
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
            # [.., a, b, ...]
            # If a is greater than b so the algorithm should swapp the values:
            if a > b:
                list_[i + 1] = a
                list_[i] = b
            else:
                continue
    return list_


# Esta función verifica que una lista este ordenada.
# Recibe una lista.
# Retorna un booleano indicando True si esta ordenada la lista y false
# en caso contrario.
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

# Esta funcion ordena una lista según la elija el usuario:
# Recibe una lista en y el tipo de ordenamiento.
# Retorna la lista ordenada.
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


# --------------------------------------------Fin de la primera parte--------------------------------------------------#
# ---------------------------------Parte 2: Algoritmos de procesamiento de imágenes------------------------------------#

def matriz_a_lista(matriz, ancho_alto):
    lista_salida = [0] * ancho_alto * ancho_alto
    contador_lineal = 0
    # Iterate over rows
    for i in range(ancho_alto):
        # Iterate over columns:
        for j in range(ancho_alto):
            lista_salida[contador_lineal] = matriz[i][j]
            contador_lineal += 1
    return lista_salida


# Generates the kernel of each pixel: i is the row counter, and j is column counter:
# i is the row index
# j is the column index
# len is length
def constructor_ventana(i, j, imagen, tamanno_ventana):
    x_imagen_len = len(imagen[0]) - 1
    y_imagen_len = len(imagen) - 1
    ventana_salida = np.zeros((tamanno_ventana, tamanno_ventana))
    if tamanno_ventana == 3:
        #  __
        # |
        if i == 0 and j == 0:
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and 0 < j < x_imagen_len:
            j -= 1
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 0 and j == x_imagen_len:
            j -= 1
            n = 1
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 0 < i < y_imagen_len and j == 0:
            i -= 1
            n = 0
            while n < tamanno_ventana:
                m = 1
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len and j == 0:
            i -= 1
            n = 0
            while n < tamanno_ventana - 1:
                m = 1
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_imagen_len and 0 < j < x_imagen_len:
            i -= 1
            j -= 1
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # ___|
        elif i == y_imagen_len and j == x_imagen_len:
            i -= 1
            j -= 1
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 0 < i < y_imagen_len and j == x_imagen_len:
            i -= 1
            j -= 1
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        else:
            i -= 1
            j -= 1
            i_ = i
            for n in range(tamanno_ventana):
                j_ = j
                for m in range(tamanno_ventana):
                    ventana_salida[n][m] = imagen[i_][j_]
                    j_ += 1
                i_ += 1
    # ------------------------------------------------------------------------------------------------------------- #
    if tamanno_ventana == 5:
        #  __
        # |
        if i == 0 and j == 0:
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
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
            while n < tamanno_ventana:
                m = 1
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 0 and j == x_imagen_len:
            n = 2
            j -= 3
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 1 and j == x_imagen_len - 1:
            n = 1
            j -= 3
            i -= 1
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len and j == 0:
            i -= 2
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len - 1 and j == 1:
            j -= 1
            i -= 2
            n = 0
            while n < tamanno_ventana - 1:
                m = 1
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_imagen_len and j == x_imagen_len:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_imagen_len - 1 and j == x_imagen_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                m = 0
                j_ = j
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                 -----
        #                |     |
        elif i == 0 and 1 < j < x_imagen_len - 1:
            j -= 2
            n = 2
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                 -----
        #                |     |
        elif i == 1 and 1 < j < x_imagen_len - 1:
            j -= 3
            i -= 1
            n = 1
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1

        #  -----
        # |     |
        elif i == 0 and j == 1:
            j -= 1
            n = 2
            while n < tamanno_ventana:
                m = 1
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #                                  -----
        #                                 |     |
        elif i == 0 and j == x_imagen_len - 1:
            j -= 2
            n = 2
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
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
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif i == y_imagen_len - 1 and j == 0:
            i -= 2
            n = 0
            while n < tamanno_ventana - 1:
                m = 2
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 1 < i < y_imagen_len - 1 and j == 0:
            i -= 2
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 1 < i < y_imagen_len - 1 and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif i == 1 and j == x_imagen_len:
            i -= 1
            j -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif i == y_imagen_len - 1 and j == x_imagen_len:
            i -= 2
            j -= 2
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 1 < i < y_imagen_len - 1 and j == x_imagen_len:
            i -= 2
            j -= 2
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 1 < i < y_imagen_len - 1 and j == x_imagen_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < tamanno_ventana:
                m = 0
                j_ = j
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_imagen_len and j == 1:
            j -= 1
            i -= 2
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |____|
        elif i == y_imagen_len and j == x_imagen_len - 1:
            j -= 2
            i -= 2
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_____|
        elif i == y_imagen_len and 1 < j < x_imagen_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and 1 < j < x_imagen_len - 1:
            i -= 2
            j -= 2
            n = 0
            while n < tamanno_ventana - 1:
                m = 0
                j_ = j
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        else:
            i -= 2
            j -= 2
            for n in range(tamanno_ventana):
                j_ = j
                for m in range(tamanno_ventana):
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                i += 1
    # ------------------------------------------------------------------------------------------------------------- #
    if tamanno_ventana == 7:
        #  __
        # |
        if i == 0 and j == 0:
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    m += 1
                    j_ += 1
                n += 1
                i += 1
        #  __
        # |
        elif i == 1 and j == 1:
            i -= 1
            j -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  __
        # |
        elif i == 2 and j == 2:
            i -= 2
            j -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 0 and j == x_imagen_len:
            j -= 3
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 1 and j == x_imagen_len - 1:
            j -= 3
            i -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #   |
        elif i == 2 and j == x_imagen_len - 2:
            j -= 3
            i -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len and j == 0:
            i -= 3
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len - 1 and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |__
        elif i == y_imagen_len - 2 and j == 2:
            i -= 3
            j -= 2
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_imagen_len and j == x_imagen_len:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_imagen_len - 1 and j == x_imagen_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __|
        elif i == y_imagen_len - 2 and j == x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and j == 1:
            j -= 1
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and j == 2:
            j -= 2
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 1 and j == 2:
            j -= 3
            i -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1

        #  -----
        # |     |
        elif i == 0 and 3 <= j < x_imagen_len - 2:
            j -= 3
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 1 and 3 <= j < x_imagen_len - 2:
            j -= 3
            i -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 2 and 3 <= j < x_imagen_len - 2:
            j -= 3
            i -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 1 and j == 0:
            i -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 2 and j == 0:
            i -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 2 and j == 1:
            i -= 2
            j -= 1
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 3 <= i < y_imagen_len - 2 and j == 0:
            i -= 3
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 3 <= i < y_imagen_len - 2 and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  ___
        # |
        # |___
        elif 3 <= i < y_imagen_len - 2 and j == 2:
            j -= 2
            i -= 3
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and j == x_imagen_len - 2:
            j -= 3
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 0 and j == x_imagen_len - 1:
            j -= 3
            n = 3
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 1 and j == x_imagen_len - 2:
            j -= 3
            i -= 1
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 1 and j == x_imagen_len:
            i -= 1
            j -= 3
            n = 2
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 2 and j == x_imagen_len - 1:
            i -= 2
            j -= 3
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        #  -----
        # |     |
        elif i == 2 and j == x_imagen_len:
            j -= 3
            i -= 2
            n = 1
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 3 <= i < y_imagen_len - 2 and j == x_imagen_len:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 3 <= i < y_imagen_len - 2 and j == x_imagen_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # __
        #    |
        # __ |
        elif 3 <= i < y_imagen_len - 2 and j == x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 2 and j == 0:
            i -= 3
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 2 and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and j == 0:
            i -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 3
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len and j == 1:
            i -= 3
            j -= 1
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 2
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len and j == 2:
            i -= 3
            j -= 2
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and j == 2:
            i -= 3
            j -= 2
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 1
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len and 3 <= j < x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and 3 <= j < x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 2 and 3 <= j < x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 2 and j == x_imagen_len:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 2 and j == x_imagen_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 1:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and j == x_imagen_len:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana - 3:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len and j == x_imagen_len - 1:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 0
                while m < tamanno_ventana - 2:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len and j == x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 3:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        # |_______|
        elif i == y_imagen_len - 1 and j == x_imagen_len - 2:
            i -= 3
            j -= 3
            n = 0
            while n < tamanno_ventana - 2:
                j_ = j
                m = 0
                while m < tamanno_ventana - 1:
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                    m += 1
                n += 1
                i += 1
        else:
            i -= 3
            j -= 3
            for n in range(tamanno_ventana):
                j_ = j
                for m in range(tamanno_ventana):
                    ventana_salida[n][m] = imagen[i][j_]
                    j_ += 1
                i += 1
    return ventana_salida


def to_grey(imagen):
    x_imagen_len = len(imagen[0])
    y_imagen_len = len(imagen)
    imagen_nueva_salida = np.zeros((y_imagen_len, x_imagen_len), np.uint8)
    for i in range(y_imagen_len):
        for j in range(y_imagen_len):
            imagen_nueva_salida[j][i] = imagen[j][i][0]
    return imagen_nueva_salida


def abrir_imagen_procesar(ruta_imagen, tamanno_ventana, tipo_ordenamiento, save_path):
    if tipo_ordenamiento == 0:
        tipo_ordenamiento_str = "Bubble sort"
    elif tipo_ordenamiento == 1:
        tipo_ordenamiento_str = "Insertion sort"
    elif tipo_ordenamiento == 2:
        tipo_ordenamiento_str = "Merge sort"
        
    imagen = mpimg.imread(ruta_imagen)
    if ruta_imagen.find(".jpg") != - 1:
        imagen_gris = to_grey(imagen)
        plt.imshow(imagen_gris, cmap=plt.get_cmap('gray'))
        plt.show()
        print("Procesando la imagen con un tamaño de ventana de " + str(tamanno_ventana)+"x" +str(tamanno_ventana) +" y con el algoritmo de "+tipo_ordenamiento_str+".")
        tiempo_inicio = time.time()
        imagen_procesada = procesar_imagen(imagen_gris, tamanno_ventana, tipo_ordenamiento)
        tiempo_final = time.time() - tiempo_inicio
    elif ruta_imagen.find(".png") != - 1:
        plt.imshow(imagen, cmap=plt.get_cmap('gray'))
        plt.show()
        print("Procesando la imagen con un tamaño de ventana de " + str(tamanno_ventana) + "x"+str(tamanno_ventana) +" y con el algoritmo de "+tipo_ordenamiento_str+".")
        tiempo_inicio = time.time()
        imagen_procesada = procesar_imagen(imagen, tamanno_ventana, tipo_ordenamiento)
        tiempo_final = time.time() - tiempo_inicio

    

    print("El procesamiento de la imagen duró " + str(tiempo_final*1000) + " milisegundos, con una ventana de tamaño " + str(
        tamanno_ventana) + " y usando el algoritmo de ordenamiento " + str(tipo_ordenamiento_str) + ".")
    plt.imshow(imagen_procesada, cmap=plt.get_cmap('gray'))
    plt.show()
    imagen_procesada.astype(int)
    imageio.imwrite(save_path, imagen_procesada)


def procesar_imagen(imagen, tamanno_ventana, sort_type):
    x_imagen_len = len(imagen[0])
    y_imagen_len = len(imagen)
    imagen_procesada = np.zeros((y_imagen_len, x_imagen_len))
    for i in range(y_imagen_len):
        for j in range(x_imagen_len):
            # Building the kernel for this i,j pixel:
            ventana = constructor_ventana(i, j, imagen, tamanno_ventana)
            # Convert the kernel in array:
            ventana_a_lista = matriz_a_lista(ventana, tamanno_ventana)
            # Sort the array:
            lista_ordenada = sort_list_by(ventana_a_lista, sort_type)
            # Find the index of the middle element
            elemento_medio = tamanno_ventana * tamanno_ventana // 2
            # Find the middle element
            nuevo_pixel = lista_ordenada[elemento_medio]
            imagen_procesada[i][j] = nuevo_pixel
    return imagen_procesada
def abrir_imagen(imagen):
    nueva_imagen = mpimg.imread(imagen)
    if imagen.find(".jpg") != - 1:
        imagen_gris = to_grey(nueva_imagen)
        plt.imshow(imagen_gris, cmap=plt.get_cmap('gray'))
        plt.show()
    elif imagen.find(".png") != - 1:
        plt.imshow(nueva_imagen, cmap=plt.get_cmap('gray'))
        plt.show()
# --------------------------------------------Fin de la segunda parte--------------------------------------------------#
# ---------------------------------Parte 3: Interacción con el usuario-------------------------------------------------#

input_image = "C:/Users/Edgar/Documents/filtrado_por_ordenamiento/Sort_image_filter/filtrado_por_ordenamiento/monalisa.png"
kernel_size = 7
sort_type = 2
# 0 -> Bubble
# 1 -> Insertion
# 2 -> Merge
output_image = "C:/Users/Edgar/Documents/filtrado_por_ordenamiento/Sort_image_filter/filtrado_por_ordenamiento/monalisa_7x7.png"

usuario_elige_opcion = 1
if usuario_elige_opcion == 1:
    abrir_imagen_procesar(input_image, kernel_size, sort_type, output_image)
elif usuario_elige_opcion == 2:
    abrir_imagen(input_image)