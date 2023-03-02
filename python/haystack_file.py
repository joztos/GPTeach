import logging
from pathlib import Path
import os 
import time

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import PDFToTextConverter, EmbeddingRetriever, OpenAIAnswerGenerator
from haystack.utils import launch_es
from haystack.pipelines import GenerativeQAPipeline

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.WARNING)

documents = []


host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
docs = converter.convert(file_path=Path("python\pdfs\9781785040207.pdf"), meta={"name": "test"})


time.sleep(30)

document_store = ElasticsearchDocumentStore(
    host = host,
    username="",
    password="",
    index="document-small-test",
    search_fields=["title","text"],
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

document_store.write_documents(docs)
document_store.update_embeddings(retriever)

print(docs[0].embedding)

generator = OpenAIAnswerGenerator(
    model="text-davinchi-003", 
    api_key="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"
    )

pipeline = GenerativeQAPipeline(reader=generator, retriever=retriever)

input = input("Enter your question: ")
result = pipeline.run(query=input, top_k_retriever=10, top_k_reader=5)