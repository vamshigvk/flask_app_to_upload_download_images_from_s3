import cv2, os
base_path = "C:/Users/Vamshi Krishna Gundu/Desktop/Vamshi/LnD/Data_Science/Projects/image_to_text_NER/ImmEffedeca/20190509/00000001"
new_path = "static/tiff_to_jpg/"
for infile in os.listdir(base_path):
    print ("file : " + infile)
    read = cv2.imread(base_path + infile)
    outfile = infile.split('.')[0] + '.jpg'
    cv2.imwrite(new_path+outfile,read,[int(cv2.IMWRITE_JPEG_QUALITY), 200])
