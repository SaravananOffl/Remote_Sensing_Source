'''
        This is a standalone script for visualising the tiff image, binary image,
        and also the output images i.e segmented image and edge dectected image.
'''


import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

''' 
      Main code starts here
'''
path = r'H:\Bachmanity_Games\purdue\Input_Files\718\r1_0000_0000.tif' #input image

raster = gdal.Open(path)

band = []       
for i in range(raster.RasterCount):
        # The tiff image is read as an array
        band.append(raster.GetRasterBand(i+1).ReadAsArray())

band1 = band[0]  # The 4 band image array is being split into 4 different array
band2 = band[1]
band3 = band[2]
band4 = band[3]

for i in range(band1.shape[0]):
    for j in range(band1.shape[1]):
        ''' 
                 The preprocessed image is segmented in 
                 this loop. 
        '''

        if(band4[i][j] <= 0.35):  #0.35 is the threshold

                    band1[i][j] = 0
                    band2[i][j] = 0
                    band3[i][j] = 0
                    band4[i][j] = 0


binary_image = np.zeros([100, 110], dtype=float)


for i in range(band1.shape[0]):
    for j in range(band1.shape[1]-1):
        '''
            Filter is applied here for reducing
            the noise
        '''

        if(band1[i][j] and band1[i][j+1]):  # 1110
                binary_image[i][j] = 1

kernel = np.ones((5,5),np.float32)/25
band4  = cv2.filter2D(band4,-1,kernel)
edge = cv2.Canny(np.uint8(binary_image), 0, 0.5)


''' 
   The images are visualised here 
'''
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

"""
    Loop for detection of leftmost and 
    rightmost values of an area
"""

for i in range(edge.shape[0]):
        j = -1
        m = 0
        while j < edge.shape[1]:

                if(j <= 0.5):
                        edge[i][j] = 0

                if( edge[i][j] ):
                     plt.scatter(j,i,color = "red", s=2)
                     count = 0
                     for k in range(j+2,edge.shape[1]-1):
                        
                        if( edge[i][k] ):    
                                matrix[i][m] = count
                                plt.scatter(k,i,color = "green", s=2)
                                m = m +1                     
                                j = k+1
                                break
                        else:
                                j=j+1
                                count = count +1
                                if(count > 8):  # maximum number of pixels in line
                                        break
                j = j+1


plt.show()
