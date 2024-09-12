import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader, JSONLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Available gemini models:
# gemini-1.5-flash-latest
# gemini-1.5-pro-latest
# gemini-1.5-pro

llm = ChatGoogleGenerativeAI(
    google_api_key=GEMINI_API_KEY, model="gemini-1.5-pro-latest", temperature=0
)

def load_csv(file_path: str):
    loader = CSVLoader(file_path)
    documents = loader.load()
    return documents

def load_json(file_path: str):
    loader = JSONLoader(
    file_path=file_path,
    jq_schema='.',
    text_content=False)
    documents = loader.load()
    return documents

def combine_documents_to_text(documents):
    text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=500)
    texts = text_splitter.split_documents(documents=documents)
    return texts

def createVectorDB_retriever(texts):
    vector_db = Chroma.from_documents(texts, GoogleGenerativeAIEmbeddings(
                model="models/embedding-001", google_api_key=GEMINI_API_KEY
            )
        )
    retriever = vector_db.as_retriever(
                search_type="mmr",  # Also test "similarity" mmr = (Maximal Marginal Relevance)
                search_kwargs={"k": 7},
            )
    return retriever

def getDocumentInsights(question,retriever,llm,chat_history=[]):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation and the context of the provided JSON, generate a search query to look up information relevant to the conversation.",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
    "system",
    '''You are an expert data analyst. Your task is to analyze the provided JSON or CSV file and generate a summary based on the data in human readable format without mentioning the filetype or any datatype. Use the information from the JSON or CSV to provide insights that are relevant and accurate.
    **Context:**\n\n{context}\n\n 

    Please provide a concise summary of the data, focusing only on the content of the JSON or CSV.
    Do not provide responses unrelated to the context or general knowledge not contained in the given data. If the user's question cannot be answered based on the given data or the given context, politely inform them that the information is not available.'''
),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ],
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    qa = create_retrieval_chain(retriever_chain, document_chain)
    result = qa.invoke({"input": question, "chat_history": chat_history})
    return result

if __name__ == '__main__':
    # text_json = load_json('inp_json/NL-1.json')
    # print(load_json)
    # text_json = combine_documents_to_text(text_json)

    # retriever = createVectorDB_retriever(text_json)

    text_csv = load_csv('Public Disclosure June_ 2024.csv')
    text_csv = combine_documents_to_text(text_csv)
    retriever = createVectorDB_retriever(text_csv)

    question = '''Please provide a brief summary of the JSON file, 
                including its main content and purpose, 
                so that someone can understand the data without opening the file. 
                '''

    # question = 'what are the values at Interest, Dividend & Rent – Gross? and show it in python dictanry with proper keays and values'
    # Additionally, if the data appears incomplete or has many missing values, 
    # please indicate this and request more data if necessary.
    chat_history = []

    question = input('Ask a question: ')

    result = getDocumentInsights(question,retriever,llm,chat_history=chat_history)

    print(result['answer'])

    # { "For the quarter\nended June 2024": "36,783", "Up to the period\nended June 2024": "36,783", "For the quarter\nended June 2023": "33,843", "Up to the period\nended June 2023": "33,843" }