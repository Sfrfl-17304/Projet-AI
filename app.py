"""
Simple Streamlit Interface for RAG Pipeline
"""
import streamlit as st
import os
from document_loader import DocumentLoader
from rag_pipeline import RAGPipeline
from mongodb_manager import mongo

# Page config
st.set_page_config(
    page_title="Simple RAG System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline(use_openai=True)
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar for document management
with st.sidebar:
    st.title("Document Management")
    
    # Upload documents
    uploaded_files = st.file_uploader(
        "Upload Documents (PDF or TXT)",
        type=['pdf', 'txt'],
        accept_multiple_files=True
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                loader = DocumentLoader()
                
                # Save uploaded files temporarily
                os.makedirs("temp_uploads", exist_ok=True)
                
                all_chunks = []
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("temp_uploads", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Load document
                    if uploaded_file.name.endswith('.pdf'):
                        chunks = loader.load_pdf(file_path)
                    else:
                        chunks = loader.load_text(file_path)
                    
                    all_chunks.extend(chunks)
                    st.success(f"✓ Processed {uploaded_file.name}: {len(chunks)} chunks")
                
                # Add to vector store
                st.session_state.rag_pipeline.vector_store.add_documents(all_chunks)
                st.success(f"✓ Added {len(all_chunks)} total chunks to knowledge base")
        else:
            st.warning("Please upload at least one document")
    
    st.divider()
    
    # Database info
    st.subheader("📊 Database Info")
    try:
        collection = mongo.get_collection("documents")
        doc_count = collection.count_documents({})
        st.metric("Documents in DB", doc_count)
    except:
        st.error("⚠ MongoDB not connected")
    
    if st.button("Clear Database"):
        st.session_state.rag_pipeline.vector_store.clear()
        st.session_state.messages = []
        st.success(" Database cleared")
        st.rerun()

# Main chat interface
st.title("🤖 Simple RAG System")
st.caption("Ask questions about your documents")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if available
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📑 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}:** {source['source']}")
                    st.markdown(f"*Similarity: {source['similarity']:.3f}*")
                    st.text(source['text'])
                    st.divider()

# Chat input
if question := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_pipeline.query(question)
            st.markdown(response["answer"])
            
            # Show sources
            if response["sources"]:
                with st.expander("📑 View Sources"):
                    for i, source in enumerate(response["sources"], 1):
                        st.markdown(f"**Source {i}:** {source['source']}")
                        st.markdown(f"*Similarity: {source['similarity']:.3f}*")
                        st.text(source['text'])
                        st.divider()
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["answer"],
        "sources": response["sources"]
    })

# Instructions if no documents
if not st.session_state.messages:
    st.info("👈 Upload documents in the sidebar to get started!")
