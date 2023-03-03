# GPTeach

GPTeach/NAVI is a web-based tool for teaching and learning where the user can learn about any subject. The information provided by the chatbot is always correct as it is deriving it from a vector dataset of books and articles. This is achieved using haystack to retrieve information and GPT-3 to generate the answers. The user can also ask questions to the chatbot and it will answer them.
The back end is running in two docker containers and the front end is made using ReactJS.
One docker container is running the latest version of haystack and the other is other is running the elasticsearch instance.
We are using the latest version of GPT-3 to generate the answers.
 