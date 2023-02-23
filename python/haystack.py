import logging
import os
from pathlib import Path

import pandas as pd

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import EmbeddingRetriever, OpenAIAnswerGenerator
from haystack.pipelines import GenerativeQAPipeline
from haystack.utils import launch_es
from haystack.nodes.file_converter.pdf import PDFToTextConverter
from haystack import Document


logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.WARNING)


doc_dir = "data/tutorial7/"

# Read PDF files from a local directory
pdf_dir = Path("/pdfs")
pdf_paths = list(pdf_dir.glob("*.pdf"))

# Convert PDFs to text and create documents
documents = []
for pdf_path in pdf_paths:
    converter = PDFToTextConverter(remove_numeric_tables=False, keep_physical_layout=False)
    text = converter.convert(file_path=pdf_path)
    document = Document(content=text, meta={"name": pdf_path.stem})
    documents.append(document)


# Initialize ElasticsearchDocumentStore
launch_es()
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document-small-test",
    search_fields=["content", "meta.name"],
    embedding_field="embedding",
    excluded_meta_data=["embedding"],
    embedding_dim=768,
)

# Write documents to Elasticsearch
document_store.write_documents(documents)

# Initialize EmbeddingRetriever
retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="deepset/sentence_bert",
    model_format="farm",
    use_gpu=False,
)

# Update document embeddings in Elasticsearch
document_store.update_embeddings(retriever)

# Initialize OpenAIAnswerGenerator
generator = OpenAIAnswerGenerator(
    model="text-davinci-002",
    api_key="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",
)

# Initialize GenerativeQAPipeline
pipeline = GenerativeQAPipeline(generator=generator, retriever=retriever)

# Run pipeline to get answers to a question
result = pipeline.run(query="What is the capital city of France?", params={"Retriever": {"top_k": 5}})
print(result)