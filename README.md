# NAVI (GPTeach)

GPTeach/NAVI is a web-based learning platform for learning and interacting with subjects and topics of interest. The project was developed during the lablab.ai openAi hackathon in February 2023.

The beta version can be found at https://navitutor.com

The answers provided by NAVI as a tutor are considered reliable as they derive from curated information sources stored as dense vectors in an elasticsearch document store instance. In addition to the use of davinci-003 as a generative model, the pipeline also uses text-embedding-ada002 as an embedding retriever model.
This was made possible through the usage of the haystack open-source NLP framework. https://github.com/deepset-ai/haystack

## Solution Design

Check our presentation for the project objectives and the architecture design:
https://docs.google.com/presentation/d/1jhfrR_fRazsBLNq4vDa1OaU96nMoqA2ZoVJrbSS0bN4/edit#slide=id.g214c9b7a8bf_1_53
Our solution makes use of containerized pipelines that offer API endpoints and allow ingestion and preprocessing of information sources, vector embedding and cosine similarity retrieval (using text-embedding-ada-002) of both documents and queries and finally answer generation using davinci-003. 

We released the core engine for the hackathon with the main question answering module. It can be tested at https://navitutor.com

We intend to continue contributing to this project and expanding its capabilities, including but not limited to:
+ Adding quizzes and other topic exploration tools.
+ Allowing study plan customization based on a student's learning style and mood.
+ Introducing Speech capabilities by using OpenAI whisper.
+ Increasing the knowledge base in the ElasticSearch Documentstore.

## Hardware Infrastructure

The infrastructure used to build and host the solution is a bare Ubuntu Linode server, offered to us by Intelijus a legal AI company [Intelijus AI](https://www.intelijus.ai), with and having the following specifications:
+ AMD EPYC 7F72 24-Core Processor
+ 32 GB RAM
+ 600 GB SSD Drive
+ 24GB Nvidia Ada RTX 6000 GPU card

Our hackathon team configured and installed all packages required to get the server ready and up and running.
   
## Hosting and Front-end

We have acquired the domain navitutor.com for our project from [namecheap](https://namecheap.com)
We installed and use Apache2 as the main webserver to host our frontend. 
We also use Apache2 for Proxying some of the requests that are intended for the haystack Api nodes.

We used certbot to get Let's encrypt SSL certificates for the domain.
The domain is also protected behind cloudflare.

The frontend is written entirely using react.js
The github hosting our frontend source code can be found here: https://github.com/zubair480/GPtech

## Main NLP pipeline and back-end setup

What makes the core QA function of NAVI possible is a retriever augmented generative model pipeline powered by the Haystsack NLP opensource framework.
The pipeline we used to make NAVI possible has the following components:
+ We used the approach detailed in this Haystack guide [Using Haystack with REST API](https://haystack.deepset.ai/tutorials/20_using_haystack_with_rest_api) as a basis of our rest api architecture.
+ One Docker Container instance of Elastic Search 7.17.6. Elastic Search serves as the documentstore for the source of information of NAVI. The information is stored in the documentstore as dense vector embeddings with an embeddings dimension of 1536.
+ One Docker container instance of Haystack: Haystack helps orchestrate the whole pipeline from preprocessing documents, creating and updating embeddings, retrieving contexts using text-embedding-ada-002 as an embedding retriever model, and final answer generation using OpenAI's davinci. The Haystack framework allows developers to define the pipeline by configuring yaml configuration files. We configured the [docker-compose.yaml](https://github.com/joztos/GPTeach/blob/main/yaml_files/docker-compose.yml) config file to define the required docker containers , their inter-depenencies, environent variables, and other failsafe settings. Then we set-up the [navi.haystsack-pipeline.yml](https://github.com/joztos/GPTeach/blob/main/yaml_files/navi.haystack-pipeline.yml) file to define the components of the pipeline (being preprocessing , documentstore, retriever model, generative model) and the pipeline construction.
+ The pipeline takes care of passing results to the next element in the pipeline and return a final result.
+ The two containers were then started using a simple docker-compose up command.
+ The container uses fast_api to allow acccess to pipeline capabilities using rest_api.
+ We hand-picked initial information about Machine Learning for the demo, and stored it into the document store using haystack's /file-upload rest_api endpoint.
+ The front-end communicates user queries via the /query endpoint which then proxies the query to the rest_api /query endpoint of the haystack container and returns an answer to the user.







 
