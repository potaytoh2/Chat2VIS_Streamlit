import openai
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from dotenv import dotenv_values
import chromadb

config = dotenv_values(".env")  
openai.api_key = config["OPENAI_API_KEY"]

class RetrievalSystem:
    embedding = None
    db3 = None
    llm = None
    custom_prompt = """ Given the context, answer the question
{context}
Question: {question}"""
    PROMPT = PromptTemplate.from_template(custom_prompt)
    llm_name = "gpt-4"
    retriever = None
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key='question',
        output_key='answer'
    )
    @staticmethod
    def initialize(OpenAIKey):
        print("yay")
        RetrievalSystem.embedding = OpenAIEmbeddings(openai_api_key=OpenAIKey)
        RetrievalSystem.db3 = Chroma(persist_directory="./VectorStore", embedding_function=RetrievalSystem.embedding, collection_name="openai_collection")
        RetrievalSystem.llm = ChatOpenAI(model_name=RetrievalSystem.llm_name, temperature=0.1)
        RetrievalSystem.retriever = RetrievalSystem.db3.as_retriever(search_type="mmr")

    @staticmethod
    def query(question, OpenAIKey=openai.api_key):
        # Ensure components are initialized
        if RetrievalSystem.embedding is None or RetrievalSystem.llm is None:
            RetrievalSystem.initialize(OpenAIKey)
        qa = ConversationalRetrievalChain.from_llm(
            RetrievalSystem.llm,
            combine_docs_chain_kwargs={"prompt": RetrievalSystem.PROMPT},
            retriever=RetrievalSystem.retriever,
            return_source_documents=True,
            return_generated_question=True,
            memory=RetrievalSystem.memory
        )
        result = qa.invoke({"question": question})
        print(result)
        return result["answer"]
