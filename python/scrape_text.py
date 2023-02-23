import PyPDF2

# Open the PDF file
pdf_file = open('path/to/your/file.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

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