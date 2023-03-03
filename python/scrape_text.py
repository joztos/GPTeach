import os
import fitz
from tqdm import tqdm

# Set the input and output folder paths
input_folder = 'python\pdfs'
output_folder = 'python\output'


# Loop through each file in the input folder
for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith('.pdf'):
        # Open the PDF file and create a PDF reader object
        pdf_file = fitz.open(os.path.join(input_folder, filename))

        # Loop through each page in the PDF and extract the text
        text = ''
        for page in pdf_file:
            text += page.get_text()

       # Create a new text file in the output folder with the extracted text
        output_file = open(os.path.join(output_folder, os.path.splitext(filename)[0] + '.txt'), 'w', encoding='utf-8')
        output_file.write(text)

        # Close the input and output files
        pdf_file.close()
        output_file.close()