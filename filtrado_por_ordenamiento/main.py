from image_processing import *


input_image = "C:/Users/WPC/Documents/Sort_image_filter/filtrado_por_ordenamiento/prueba.jpg"
kernel_size = 7
sort_type = 1
# 0 -> Bubble
# 1 -> Insertion
# 2 -> Merge
output_image = "C:/Users/WPC/Documents/Sort_image_filter/filtrado_por_ordenamiento/images/output_prueba_7x7.jpg"


abrir_imagen(input_image, kernel_size, sort_type, output_image)
