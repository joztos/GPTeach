from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever
import logging
import os

# set up logging
logging.basicConfig(format="%(levelname)s - %(name)s - %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.DEBUG)

# initialize document store

document_store = InMemoryDocumentStore(use_bm25=True)

doc_dir = "python/output"

files_to_index = [ doc_dir + "/" + f for f in os.listdir(doc_dir) if f.endswith(".txt") ]
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(files_to_index)
