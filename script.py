import numpy as np
import gdal
import os
import warnings
import xlwt
import matplotlib.pyplot as plt


''' 

 EXCEL SETUP 

'''
def setup_excel():

    column_names = ["Input File", "B1_Mean", "B2_Mean","B3_Mean","B4_Mean","B1_Median","B2_Median","B3_Median",
                   "B4_Median"]
    for no,column_name in enumerate(column_names):
        sheet.write(0,no,column_name)
    
        

def write_mean(stats,row_no):
    for no, band in enumerate(stats):
                   sheet.write(row_no+1,no+1,float(band))
            
def write_median(stats,row_no):
    for no, band in enumerate(stats):
                   sheet.write(row_no+1,no+5,float(band))



''' 
   FUNC TO FIND ALL THE FILES IN A PARTICULAR DIRECTORY

'''
            
def findFiles(path):
    tif_files = []
    for file in os.listdir("{}".format(path)):
        if file.endswith('.tif'):
            tif_files.append(file)
    return tif_files


''' 

  FUNC TO VISUALISE THE TIF FILE (ONE BAND AT A TIME)

'''

def visualise(band1):
    plt.figure()
    plt.imshow(band1)
    plt.show()
     

'''

  MAIN FILE STARTS HERE

'''
        
def main():
    
    print("Started....")
    setup_excel()
    path = '/media/saravanan/Back UP/Bachmanity Games/purdue/Input Files/718' # <- GIVE INPUT HERE 
    row_no = 0

    for file in findFiles(path):
        raster = gdal.Open('{0}/{1}'.format(path,file))
        band = []
        for i in range(raster.RasterCount):
            band.append(np.absolute(raster.GetRasterBand(i+1).ReadAsArray())) # The tiff image is read as an array 
        
        band1 = band[0]  # The 4 band image array is being split into 4 different array
        band2 = band[1]
        band3 = band[2] 
        band4 = band[3]

        for i in range(band1.shape[0]):
            for j in range(band1.shape[1]):
                if(band1[i][j]>=0.061): # <- Threshold Value is Given Here
                    band1[i][j] = 0
                    band2[i][j] = 0
                    band3[i][j] = 0
                    band4[i][j] = 0

        band1 = np.array(band1,dtype=np.float64)  
        band2 = np.array(band2,dtype=np.float64)
        band3 = np.array(band3,dtype=np.float64)
        band4 = np.array(band4,dtype=np.float64)


        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mean = [np.nanmean(band1,dtype=np.float64),np.nanmean(band2,dtype=np.float64),np.nanmean(band3,dtype=np.float64),
                    np.nanmean(band4,dtype=np.float64)]
            median = [np.median(band1[np.nonzero(band1)]),np.median(band2[np.nonzero(band2)]),np.median(band3[np.nonzero(band3)])
                  ,np.median(band4[np.nonzero(band4)])]
 
        sheet.write(row_no+1,0,file)
        write_mean(mean,row_no)
        write_median(median,row_no)
        row_no = row_no  +1
        book.save('OUTPUT NAME.xls') # <- Output Excel File Name
    
       #visualise(band1) 
       # Uncomment above line if and only if you're using Jupyter Notebook

    
book = xlwt.Workbook()
sheet = book.add_sheet("Stats")

main()
print("Done....")

    
    

