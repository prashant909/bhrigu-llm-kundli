from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def run_bot():
    vectorstore = FAISS.load_local("llm/faiss_index", OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)

    while True:
        query = input("🧘 Ask Bhrigu Samhita: ")
        if query.lower() in ['exit', 'quit']: break
        answer = qa_chain.run(query)
        print("🔮", answer)

if __name__ == "__main__":
    run_bot()
