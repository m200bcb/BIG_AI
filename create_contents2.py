import openai
import os
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

urls = [
    'https://wikidocs.net/20',
    'https://wikidocs.net/4307',
    'https://wikidocs.net/6',
    'https://wikidocs.net/12',
    'https://wikidocs.net/206257',
    'https://wikidocs.net/206265',
    'https://wikidocs.net/206316',
    'https://wikidocs.net/206317',
    'https://wikidocs.net/206354',
    'https://wikidocs.net/206429',
    'https://wikidocs.net/206430',
    'https://wikidocs.net/206592',
    'https://wikidocs.net/207256',
    'https://wikidocs.net/207014',

]


loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
doc = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings(
    model='text-embedding-ada-002')
vectorstore = Chroma.from_documents(doc, embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2})

chat_llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0
)

qa = RetrievalQA.from_chain_type(
    llm=chat_llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True)

# query = "if문에 대한 설명과 그에 관한 실습 과제를 만들어줘. 답도 알려줘."
# result = qa({"query": query})
#
# print(result["result"], result["source_documents"][0].metadata)