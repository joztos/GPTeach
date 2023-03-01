import logging
from pathlib import Path
import os 

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import PDFToTextConverter, EmbeddingRetriever
from haystack.utils import launch_es

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.WARNING)

documents = []

host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])
docs = converter.convert(file_path=Path("python\pdfs\9781785040207.pdf"), meta={"name": "test"})

launch_es()

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
