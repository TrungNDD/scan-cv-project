from cv2 import split
import numpy
from pdf2image import convert_from_bytes
from platformdirs import os
from scan_cv import scanCV

def convertPdf2Image(file):
    pages = convert_from_bytes(file.read(), 500)

    #image_counter = 1
    
    filename = os.path.basename(file.name)
    newFileName = 'tmp/' + filename.split('.')[0] + '.txt'
    f = open(newFileName, "w", encoding="utf-8")

    for page in pages:

        #image_name = "tmp/page_"+str(image_counter)+".jpg"
        
        # Save the image of the page in system
        #page.save(image_name, 'JPEG')

        pil_image = page.convert('RGB')
        open_cv_image = numpy.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[: ,: , ::-1].copy()

        # Increment the counter to update filename
        #image_counter = image_counter + 1

        #filelimit = image_counter-1
        
        retrievedText = scanCV(open_cv_image)
  
        if retrievedText:
            #print(retrievedText)
            f.write(retrievedText)

    f.close()
    return f.name.split('/')[1]