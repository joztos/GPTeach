import logging
from pathlib import Path
import os 
import time
import sys

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import PDFToTextConverter, EmbeddingRetriever, OpenAIAnswerGenerator
from haystack.utils import launch_es
from haystack.pipelines import GenerativeQAPipeline

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.WARNING)

documents = []
pdf_path = Path("./pdfs")

host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
for pdf_file in pdf_path.glob("*.pdf"):
    text = converter.convert(file_path=pdf_file, meta={"name": pdf_file.name})
    documents.append(text)


document_store = ElasticsearchDocumentStore(
    host = host,
    username="",
    password="",
    index="document-small-test",
    embedding_field="embedding",
    excluded_meta_data=["embedding"],
    embedding_dim=768,
)

retriever = EmbeddingRetriever(
    document_store=document_store, 
    embedding_model="text-embedding-ada-002",
    api_key="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",
    max_seq_len=500,
    )

document_store.write_documents(documents=documents)
document_store.update_embeddings(retriever)

print(documents[0].embedding)

generator = OpenAIAnswerGenerator(
    model="text-davinci-003", 
    api_key="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"
    )

pipeline = GenerativeQAPipeline(generator=generator, retriever=retriever)

user_query = sys.argv[1]

result = pipeline.run(query=user_query, top_k_retriever=10, top_k_reader=5)