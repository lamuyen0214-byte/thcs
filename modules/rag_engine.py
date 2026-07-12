import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader # Hoặc PyPDFLoader nếu dùng PDF

def process_rag_engine(uploaded_file, user_query):
    if not uploaded_file:
        return "Vui lòng tải tài liệu lên."
    
    # 1. Lưu file tạm để LangChain đọc
    with open("temp_file.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 2. Load và phân tách văn bản (Chunking)
    loader = TextLoader("temp_file.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    # 3. Tạo Vector Database (sử dụng Embedding của Google)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=st.session_state["user_gemini_key"])
    db = Chroma.from_documents(texts, embeddings)
    
    # 4. Thiết lập chuỗi RetrievalQA với Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=st.session_state["user_gemini_key"])
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    
    # 5. Truy vấn
    response = qa_chain.invoke({"query": user_query})
    return response["result"]
