import os
import findpapers

# Set up the search query
query="([artificial intelligence] OR [AI] OR [machine learning] OR [ML] OR [deep learning] OR [DL]) AND ([music] OR [s?ng])"
#query = "artificial intelligence"
engine = "google"
num_results = 50

# Create a folder to save the PDFs
if not os.path.exists("pdfs"):
    os.makedirs("pdfs")



# Search for the papers and download them
results = findpapers.search(query, engine, num_results)
for result in results:
    try:
        pdf_data = findpapers.download(result["url"], format="pdf")
        filename = os.path.join("pdfs", result["title"] + ".pdf")
        with open(filename, "wb") as f:
            f.write(pdf_data)
            print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {result['title']}: {e}")