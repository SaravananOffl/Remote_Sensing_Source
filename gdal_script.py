import gdal
import matplotlib.pyplot as plt
import numpy as np

path = "path.tif"

raster = gdal.Open(path)

band = []
for i in range(raster.RasterCount):
        band.append(raster.GetRasterBand(i+1).ReadAsArray())

band1 = band[0]  
band2 = band[1]
band3 = band[2] 
band4 = band[3]

for i in range(band1.shape[0]):
    for j in range(band1.shape[1]):
           if(band4[i][j]<=0.39): 
                    band1[i][j] = 0
                    band2[i][j] = 0
                    band3[i][j] = 0
                    band4[i][j] = 0
                    

plt.imshow(band4, 'copper')
plt.title("Original")
new_mat = np.count_nonzero(band4, axis = 0)
new_mat = np.append(0,new_mat)
new_mat = np.append(new_mat,0)
print(new_mat, "\n")

length_matrix = []
if(np.count_nonzero(new_mat)>1):
        for i in range(new_mat.shape[0]-1):
                if(new_mat[i] and new_mat[i-1]==0 and new_mat[i+1]!=0): # 011
                        print(f'Left pixel found at {i}, Value is :  {new_mat[i]}')
                        for z in range(i+1,new_mat.shape[0]-1):
                                print(f'    checking  {z},  value is :{new_mat[z]}')

                                if((z-i)>=13 ):
                                        value = int((z-i+1)/2)
                                        length_matrix.append(new_mat[i+value])
                                        i = z 
                                       

                                if(new_mat[z] and new_mat[z+1]==0):#10
                                        length = int(z-i)
                                        value = int((z-i+1)//2)
                                        print(f"Found right....  Center Index {value+i}, value is {new_mat[value+i]} \n " )
                                        if(value!=1):
                                                length_matrix.append(new_mat[i+value])
                                                i = z
                                        
                                        break
                

else:
        length_matrix.append("NaN")
print(length_matrix)
        
plt.show()
