
# WebWise_RAG_CHATBOT

## Overview
This project is a web-based application designed to leverage advanced language model integrations for natural language processing tasks. Utilizing Streamlit for an interactive user interface, it incorporates LangChain for seamless interaction with language models, document processing, and information retrieval functionalities. It's ideal for users looking to explore language model capabilities within a user-friendly web environment.
 
## Objectives
- To create a chatbot that leverages the LangChain library to communicate with and extract data from websites.
- To implement the latest Large Language Models for natural language understanding and generation, ensuring the system is equipped to handle complex queries.
- To build a user-friendly interface using Streamlit, allowing users from diverse backgrounds to interact with the chatbot without technical barriers.
- To enhance the language model's knowledge base by preprocessing and vectorizing website content for efficient retrieval during conversations.

## Features
 - Interactive web interface using Streamlit.
 - Integration with LangChain for advanced language model processing.
 - Document loading, text splitting, and information retrieval.
 - Vector storage with Chroma for efficient data handling.
 - OpenAI embeddings for enhanced language understanding.

## Methodology

- **Data Acquisition:** The chatbot will use BeautifulSoup, a Python library, to scrape content from specified websites. The scraped HTML content will be the primary data source that the chatbot will refer to during interactions.  
  
- **Data Preprocessing:**  The retrieved data will undergo text-splitting, breaking down the content into manageable chunks (documents). Each chunk represents a potential source of information that the chatbot could draw upon.  
  
- **Vectorization:**  The preprocessed text chunks will be vectorized—converted into numerical representations known as embeddings. These embeddings capture the semantic content of the text in a form that can be efficiently processed by computational models.  
  
- **Semantic Search:**  A vector database will store the embeddings, enabling semantic search capabilities. When a query is received, it will be embedded into the same vector space, and a semantic search will be conducted to find the most relevant text chunks.  
  
- **Large Language Model Integration:**  The most relevant text chunks will be used to augment the knowledge of the LLM. This "augmented knowledge" will be passed as a prefix to the language model to inform its responses.  
  
- **User Interface:**  A Streamlit-based graphical user interface (GUI) will be developed, providing a clean and intuitive platform for users to interact with the chatbot.  
  
- **Retrieval-Augmented Generation (RAG):**  The chatbot will use a Retrieval-Augmented Generation approach, where the LLM's responses are informed by the information retrieved from the website content, ensuring that the chatbot's replies are both informative and up-to-date.

## Outcomes

- A fully functional chatbot capable of providing accurate and contextually relevant information sourced from websites in real-time.

- A user-friendly interface that democratizes access to complex language model technologies.

- A versatile system that can be adapted to various domains by simply changing the websites it interacts with.







