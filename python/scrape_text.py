import PdfReader 

# Open the PDF file
pdf_file = open('python/pdfs/9781785040207.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PdfReader.PdfFileReader(pdf_file)

# Get the total number of pages
num_pages = pdf_reader.numPages

# Initialize a string variable to hold all the text
full_text = ""

# Loop through each page and extract the text
for i in range(num_pages):
    page = pdf_reader.getPage(i)
    text = page.extractText()
    full_text += text

# Close the PDF file
pdf_file.close()

# Write the text to a file
with open('python/output/text.txt', 'w') as f:
    f.write(full_text)