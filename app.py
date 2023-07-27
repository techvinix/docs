import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.document_loaders import Docx2txtLoader, TextLoader, UnstructuredExcelLoader
from langchain.document_loaders.csv_loader import CSVLoader , UnstructuredCSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from css import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

import tempfile
from PIL import Image

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text(uploaded_files):
    documents =""
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

        doc = uploaded_file.name

        if doc.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                documents += page.extract_text()

        elif doc.endswith('.docx') or doc.endswith('.doc'):
            loader = Docx2txtLoader(tmp_file_path)
            documents += str(loader.load())

        elif doc.endswith('.txt'):       
            loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
            documents += str(loader.load())
        
        elif doc.endswith('.csv'):       
            loader = UnstructuredCSVLoader(file_path=tmp_file_path, mode="elements")
            documents += str(loader.load())

    return documents

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore, model, temperature):
    llm = ChatOpenAI(temperature=temperature,model_name=model)
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        max_tokens_limit=4000,
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    try:
        st.session_state.chat_history = response['chat_history']
    except:
        st.write("Select all parameters and upload documents")

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()

    logo = Image.open('static/chat-doc.png')
    st.set_page_config(page_title="DocConnect",   page_icon=":hugging_face:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("🦜️🔗 Chat with multiple files :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        try:
            if user_question is not None:
                handle_userinput(user_question)
        except Exception as e:
            st.write("Please select all parameters and upload documents before asking questons about your documents")
    else:
        st.write('Ask a question about your documents')

    with st.sidebar:
        st.sidebar.title('DocConnect: Empowering Conversations 🧠🦜️🔗')
        st.sidebar.image(logo, use_column_width=True)
        st.subheader("Choose Large Language Model and its temperature")
        models = ["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613"]
        model = st.sidebar.selectbox("Select a GPT Model", models, index=0)
        temperature = st.sidebar.slider('Select a value', min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        
        
        docs = st.file_uploader("Upload doc and click on 'Process'", accept_multiple_files=True)

        try:
            if st.button("Process"):
                with st.spinner("Processing..."):
                # get pdf text
                    raw_text = get_text(docs)

                # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore, model, temperature)
                st.success("Done!")

        except Exception as e:
            print(f"Caught an Exception: {e}")

            
        


if __name__ == '__main__':
    main()