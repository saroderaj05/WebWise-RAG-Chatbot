import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# load environment variables, useful for API keys or sensitive data
load_dotenv()



# function to load and vectorize text from a given URL
def get_vectorestore_from_url(url):
    #get the text in document form
    loader = WebBaseLoader(url)
    document = loader.load()

    #split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    # convert the document chunks into a vector store for retrieval
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings() )

    return vector_store


# function to create a context-aware retriever chain using the vector store
def get_context_retriever_chain(vector_store):

    llm = ChatOpenAI() # initialize the language model

    # convert the vector store into a retriever for querying
    retriever = vector_store.as_retriever()

    # define the prompt template for the retriever
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}" ),
        ("user", "Given the aove conversation, generate a search quesry to look up in the document")
    ])

    # create a retriever chain that is aware of the conversation history
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    return retriever_chain

# function to create a conversational chain for document retrieval and generation
def get_conversational_rag_chain(retriever_chain):

    llm = ChatOpenAI()

    # define the prompt for generating responses based on retrieved documents
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's question based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}" ),
    ])

    # create a chain that combines document retrieval with response generation
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

# main function to generate a response based on user input and conversation history
def get_response(user_input):

    # vector_store = get_vectorestore_from_url(website_url)

    # retrieve the appropriate chains for context retrieval and conversation
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    # response = get_response(user_query)

    # generate a response using the conversation chain
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_query
    })

    return response['answer']



# streamlit app configuration
st.set_page_config(page_title="Chat with website", page_icon="🤖")
st.title("Chat With Websites")


# sidebar for input settings
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")

# ensure a website URL is provided
if website_url is not None and website_url == "":
    st.info("Please enter a valid website URL")

else:
    # initialize session state for chat history and vector store if not already done
    #session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am WebWise, How can I help you today?"),
        ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorestore_from_url(website_url)

    # document_chunks = get_vectorestore_from_url(website_url)
    
    # handle user input and generate responses
    #user input
    user_query = st.chat_input("Type your message here")
    if user_query is not None and user_query != "":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

        # retrieved_documents = retriever_chain.invoke({
        #     "chat_history": st.session_state.chat_history,
        #     "input": user_query
        # })
        # st.write(retrieved_documents)

    # display conversation history
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):            
                st.write(message.content)
