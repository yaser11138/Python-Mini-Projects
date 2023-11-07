from PIL import Image
import pytesseract
import pathlib

#tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

paths_of_images = []

end_of_string = '' # end input when this string is seen

for line in iter(input, end_of_string): # loop of input to get multiple inputs in row
    paths_of_images.append(pathlib.Path(line))
    
text_of_images = [] 

language = input("please enter a language \nenglish -> eng \npersian -> fas \n")
while language not in ["fas", "eng"]:
    language = input("please enter in correct format \nfor english -> eng \nfor persian -> fas \n")

for path in paths_of_images:
        text_of_images.append(pytesseract.image_to_string(Image.open(path), lang=language))
        
type_of_response = input("please enter the type ypu like to get text \nF for write in file  \nT for text output\n")
while type_of_response not in ["T","F"]:
    type_of_response = input("please enter in correct format \nF for write in file  \nT for text output\n")

if type_of_response == "T":
    print("text_of_image")
else:
    for i in range(len(paths_of_images)):
        with open(f"{paths_of_images[i].stem}_text.txt","w") as text_file:
            text_file.write(text_of_images[i])
            
            