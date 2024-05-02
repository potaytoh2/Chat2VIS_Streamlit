import openai
from dotenv import dotenv_values
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import asyncio
import chromadb



async def perform_embeddings_and_store_vectors(api_key, source_directory, persist_directory):
    # Set the OpenAI API key

    # Load documents from the source directory
    loader = DirectoryLoader(source_directory)
    docs = loader.load()
    

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    splits = text_splitter.split_documents(docs)

    # Initialize OpenAI embeddings
    embedding = OpenAIEmbeddings(openai_api_key=api_key)
    client = chromadb.PersistentClient("VectorStore")

    # Perform embeddings and store the vectors
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        client=client,
        persist_directory=persist_directory,
        collection_name="openai_collection"
    )
    print("This is vectordb: \n")
    print(vectordb)
    docs = vectordb.similarity_search("Give me the latest token transfered")
    print(docs[0].page_content)
if __name__ == "__main__":
    # Load configuration from .env file
    config = dotenv_values(".env")  
    openai.api_key = config["OPENAI_API_KEY"]
    loader = DirectoryLoader("./sourceDocuments/")

    # Call the function and print the number of vectors stored
    asyncio.run(perform_embeddings_and_store_vectors(
        api_key=openai.api_key,
        source_directory="./sourceDocuments/",
        persist_directory="./VectorStore"
    ))



# Print the number of vectors stored