# GPTeach

GPTeach/NAVI is a web-based learning platform for learning and interacting with subjects and topics of interest. The project was developed during the lablab.ai openAi hackathon in February 2023.

The responses provided by NAVI are reliable as they derive from curated information sources stored as dense vectors in an elasticsearch document store instsance. In addition to the use of davinci-003 as a generative model, the pipeline also uses text-embedding-retriever as an embedding retriever model.
This was made possible through the usage of the haystack open-source NLP framework. https://github.com/deepset-ai/haystack

## Infrastructure and hosting

The infrastructure used to build and host the solution is a Linode server with the following specifications:
   16 core CPU
   32 GB RAM
   600 GB SSD Drive
   Nvidia Ada RTX 6000 GPU
   


The back end is running in two docker containers and the front end is made using ReactJS.
One docker container is running the latest version of haystack and the other is other is running the elasticsearch instance.
We are using the latest version of GPT-3 to generate the answers.
 
