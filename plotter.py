import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

path = 'path'  # <- GIVE INPUT HERE


raster = gdal.Open(path)

band = []
for i in range(raster.RasterCount):
        # The tiff image is read as an array
        band.append(np.absolute(raster.GetRasterBand(i+1).ReadAsArray()))

band1 = band[0]  # The 4 band image array is being split into 4 different array
band2 = band[1]
band3 = band[2]
band4 = band[3]

for i in range(band1.shape[0]):
    for j in range(band1.shape[1]):
           if(band4[i][j] <= 0.35):  # <- Threshold Value is Given Here

                    band1[i][j] = 0
                    band2[i][j] = 0
                    band3[i][j] = 0
                    band4[i][j] = 0

band1 = np.array(band1, dtype=np.float64)
band2 = np.array(band2, dtype=np.float64)
band3 = np.array(band3, dtype=np.float64)
band4 = np.array(band4, dtype=np.float64)
binary_image = np.zeros([100, 110], dtype=float)

for i in range(band1.shape[0]):
    for j in range(band1.shape[1]-1):

        if(band1[i][j] and band1[i][j+1]):  # 1110
                binary_image[i][j] = 1

edge = cv2.Canny(np.uint8(binary_image), 0, 0.5)

plt.subplot(221)
plt.imshow(band4, 'copper')
plt.title("Original")

plt.subplot(222)
plt.imshow(binary_image, 'copper')
plt.title("Binary Image")

plt.subplot(223)
plt.imshow(edge, 'copper')
plt.title("Edge Image")

plt.subplot(224)
plt.imshow(edge, 'copper')
plt.title("Identified Left and Right Pixel")

matrix = np.zeros([83, 20])

for i in range(edge.shape[0]):
        j = -1
        m = 0
        while j < edge.shape[1]:

                if(j <= 0.5):
                        edge[i][j] = 0

                if( edge[i][j] ):
                     plt.scatter(j,i,color = "red", s=20)
                     count = 0
                     for k in range(j+2,edge.shape[1]-1):
                        
                        if( edge[i][k] ):    
                                matrix[i][m] = count
                                plt.scatter(k,i,color = "green", s=5)
                                m = m +1                     
                                j = k+1
                                break
                        else:
                                j=j+1
                                count = count +1
                                if(count > 8):
                                        break

                j = j+1
plt.show()
