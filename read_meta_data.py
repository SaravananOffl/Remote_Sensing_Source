import os 
import numpy as np
import gdal
import xlwt 


def setup_excel():
    """
        Setup the required columns
    """
    column_names = ["Input File" ,"Total #Soy Bean Pixels", "Total Pixels" ,"#soybean_pixels/TotalPixels ","Total Area"]

    for no, column_name in enumerate(column_names):
        sheet.write(0,no,column_name)


def write_area(area,row_no,filename  =False,no_pixels =False):
    """
       To write the area/filename/#pixels
    """
    size = 83*82
    if(no_pixels):
        percentage = float((area/size)*100)
        sheet.write(row_no+1,1,area)
        sheet.write(row_no+1,2,size)
        sheet.write(row_no+1,3,percentage)
        return 0

    if(filename):
         sheet.write(row_no+1,0, area)
         return 0 
    
    sheet.write(row_no+1,4, float(area))



def FindFiles(path):
    """
        To find the Tiff files in a folder(path)
    """

    tif_files = []
    for file in os.listdir("{}".format(path)):
        if file.endswith('.tif'):
            tif_files.append(file)
    return tif_files
    
def read_bands(path, file):
    """ 
        To read and split each bands.
        Returns #nonzero values in Band4
    """

        raster = gdal.Open(f'{path}/{file}')

        band = []
        for i in range(raster.RasterCount):
                band.append(raster.GetRasterBand(i+1).ReadAsArray())

        band1 = band[0]  
        band2 = band[1]
        band3 = band[2] 
        band4 = band[3]

        for i in range(band1.shape[0]):
            for j in range(band1.shape[1]):
                if(band4[i][j]<=0.38): 
                            band1[i][j] = 0
                            band2[i][j] = 0
                            band3[i][j] = 0
                            band4[i][j] = 0
        
        band4_nonzero = np.count_nonzero(band4)
        return band4_nonzero
                            



def write_meta():
    """
        To find the total area from metadata and also
        to loop through the files.
    """
        setup_excel()
        
        path = r"H:\Bachmanity_Games\purdue\Input_Files\718"
        print(path)
        row_no = 0
        for file in FindFiles(path):
            write_area(file,row_no,filename=True)
            metadata = os.popen(f'gdalinfo {path}\{file}').read()
            coordinates = [] 
            
            f = metadata.find("Upper")
            upper_left_x = float(metadata[f+15:(f+25)])
            upper_left_y = float(metadata[f+27:(f+38)])
            coordinates.append(upper_left_x)
            coordinates.append(upper_left_y)

            f = metadata.find("Lower")
            lower_left_x = float(metadata[f+15:(f+25)])
            lower_left_y = float(metadata[f+27:(f+38)])
            coordinates.append(lower_left_x)
            coordinates.append(lower_left_y)

            f= metadata.find("Upper Right")
            upper_right_x = float(metadata[f+15:(f+25)])
            upper_right_y = float(metadata[f+27:(f+38)])
            coordinates.append(upper_right_x)
            coordinates.append(upper_right_y)

            f= metadata.find("Lower Right")
            lower_right_x = float(metadata[f+15:(f+25)])
            lower_right_y = float(metadata[f+27:(f+38)])
            coordinates.append(lower_right_x)
            coordinates.append(lower_right_y)

            d1_x = coordinates[6] - coordinates[0]
            d1_y = coordinates[7] - coordinates[1]

            d2_x = coordinates[4] - coordinates[2]
            d2_y = coordinates[5] - coordinates[3]

            dx = d1_x*d2_y
            dy = d2_x*d1_y

            area = 1/2*np.absolute(dx - dy)
            non_zero = read_bands(path,file)
            write_area(non_zero, row_no, no_pixels=True)
            write_area(area,row_no)
            row_no = row_no +1 
        
        book.save("Area.xls")



book = xlwt.Workbook()
sheet = book.add_sheet("Area")
write_meta()