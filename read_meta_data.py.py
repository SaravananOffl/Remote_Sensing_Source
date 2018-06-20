import os 
import numpy
import xlwt 

def setup_excel():
    
    column_names = ["Input File" , "Area"]

    for no, column_name in enumerate(column_names):
        sheet.write(0,no,column_name)

def write_area(area,row_no,filename  =False):
    if(filename):
         sheet.write(row_no+1,0, area)
         return 0 
    sheet.write(row_no+1,1, float(area))



def FindFiles(path):
    tif_files = []
    for file in os.listdir("{}".format(path)):
        if file.endswith('.tif'):
            tif_files.append(file)
    return tif_files


def write_meta():
        setup_excel()
        
        path = r"H:\Bachmanity_Games\purdue\Input_Files\718"
        print(path)
        row_no = 0
        for file in FindFiles(path):
            write_area(file,row_no,filename=True)
            metadata = os.popen(f'gdalinfo {file}').read()
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

            area = 1/2*numpy.absolute(dx - dy)
            write_area(area,row_no)
            row_no = row_no +1 
        
        book.save("Area.xls")




book = xlwt.Workbook()
sheet = book.add_sheet("Area")
write_meta()