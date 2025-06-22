from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

def create_vector_db(txt_file='data/bhrigu_text.txt'):
    loader = TextLoader(txt_file)
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local("llm/faiss_index")
    print("✅ FAISS vector DB created.")

if __name__ == "__main__":
    create_vector_db()
