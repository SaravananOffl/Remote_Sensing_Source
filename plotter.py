import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

path = 'H:/Bachmanity_Games/purdue/Input_Files/718/r1_0002_0010.tif'  # <- GIVE INPUT HERE
# path = 'H:/Bachmanity_Games/purdue/Input_Files/718/r1_0000_0005.tif'  # <- GIVE INPUT HERE

# path = 'H:/Bachmanity_Games/purdue/Input_Files/718/r1_0002_0010.tif'  # <- GIVE INPUT HERE


raster = gdal.Open(path)

band = []
for i in range(raster.RasterCount):
        # The tiff image is read as an array
        band.append(np.absolute(raster.GetRasterBand(i+1).ReadAsArray()))

band1 = band[0]  # The 4 band image array is being split into 4 different array
band2 = band[1]
band3 = band[2]
band4 = band[3]


# plt.figure()

for i in range(band1.shape[0]):
    for j in range(band1.shape[1]):
           if(band4[i][j] <= 0.35):  # <- Threshold Value is Given Here

                #                     print(i,j)
                    # plt.scatter(j,i,label= "stars", color= "yellow",
            # marker= "*", s=30)
                    band1[i][j] = 0
                    band2[i][j] = 0
                    band3[i][j] = 0
                    band4[i][j] = 0

band1 = np.array(band1, dtype=np.float64)
band2 = np.array(band2, dtype=np.float64)
band3 = np.array(band3, dtype=np.float64)
band4 = np.array(band4, dtype=np.float64)

print(band1.shape)
front_column = np.zeros([100, 1], dtype=float)
binary_image = np.zeros([100, 110], dtype=float)
binary_image = np.append(binary_image, front_column, axis=1)
count_x = []
count_xx = 0
for i in range(band1.shape[0]):
    for j in range(band1.shape[1]-1):

        if(band1[i][j] and band1[i][j+1] and band1[i][j+1]):  # 1110
                # count_xx = count_xx+1
                binary_image[i][j] = 1
                # print(f"{i},{j}")
                # plt.scatter(j,i,color="blue")

        # print(i)
#     count_x.append(count_xx)
#     count_xx=0

    # print(f'Total Count in {i}th row is ', count_x[i] )

# plt.imshow(band1)
# # x_name = np.arange(0,85,1)
# plt.xticks(x_name)
# # plt.scatter(3,54)
# plt.show()

# plt.figure()
# band1 = np.uint8(band1)
# edge = cv2.Canny(band1,0,0.5)
# plt.subplot(133), plt.imshow(band4)
# plt.title("Original")

edge = cv2.Canny(np.uint8(binary_image), 0, 0.5)
# plt.ion()

# fig = plt.figure()
# fig.show()
# fig.canvas.draw()
plt.imshow(edge, cmap='gray')
plt.title("Edge")
matrix = np.zeros([83, 20])
for i in range(edge.shape[0]):
        j = -1
        m = 0
        # if(i > 0):
        #         break
        while j < edge.shape[1]:
                if(j <= 0.5):
                        # plt.scatter(j,i,color="pink")
                        edge[i][j] = 0
                # if(j>0):
                        # break
                # print("Entered")
                # print(j)
                #  range(1,edge.shape[1]-1):
                if(edge[i][j]):
                        #      m =0
                        #      print("found left")
                        #      print(i,j,'\n')
                     plt.scatter(j, i, color="red", s=20)
                #      fig.canvas.draw()
                     count = 0

                     for k in range(j+2, edge.shape[1]-1):

                        if(edge[i][k]):
                                #   and edge[i][k+1]==0):

                                # print("K value is ", k)
                                # print("J value is" , j,'\n')
                                # print("found right")
                                # print(i,j,'\n')
                                # diff = (i,k) - (i,j)
                                difference = np.absolute(j - i)
                                # print(difference)
                                # print("Difference",difference)

                                if(count > 8):
                                        break

                                matrix[i][m] = count
                                plt.scatter(k, i, color="green", s=5)

                                m = m + 1

                                # print(j,"After Updation")
                                j = k+1
                                # print(j)
                                break
                        else:
                                # print("No right found")
                                j = j+1
                                count = count + 1
                                if(count > 8):
                                        break

                j = j+1
print(matrix)


print(np.argmax(binary_image))

# i = np.arange(0,80)
# j = np.arange(0,80)
# plt.scatter(1,50,s=100,color = "blue")

# plt.subplot(132), plt.imshow(binary_image, cmap='gray')
# plt.title("Binary Image")
# plt.subplot(131),

plt.show()
