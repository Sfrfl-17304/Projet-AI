"""
RAG Pipeline - Retrieval Augmented Generation
"""
import os
from typing import List
from dotenv import load_dotenv
from vector_store import VectorStore
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

class RAGPipeline:
    def __init__(self, use_openai=True):
        """Initialize RAG pipeline"""
        self.vector_store = VectorStore()
        
        # Initialize LLM (OpenAI or fallback to simple template)
        self.use_openai = use_openai
        if use_openai and os.getenv("OPENAI_API_KEY"):
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                print("✓ Using OpenAI for response generation")
            except Exception as e:
                print(f"⚠ Could not initialize OpenAI: {e}")
                self.use_openai = False
        else:
            self.use_openai = False
            print("✓ Using template-based responses (no LLM)")
        
        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the question based on the context provided. If you cannot answer from the context, say so."),
            ("user", """Context:
{context}

Question: {question}

Answer:""")
        ])
    
    def query(self, question: str, k: int = 4) -> dict:
        """Query the RAG pipeline"""
        # Retrieve relevant documents
        relevant_docs = self.vector_store.similarity_search(question, k=k)
        
        if not relevant_docs:
            return {
                "answer": "I couldn't find any relevant information in the knowledge base.",
                "sources": []
            }
        
        # Prepare context
        context = "\n\n".join([
            f"[Source: {doc['source']}]\n{doc['text']}"
            for doc in relevant_docs
        ])
        
        # Generate answer
        if self.use_openai:
            try:
                messages = self.prompt_template.format_messages(
                    context=context,
                    question=question
                )
                response = self.llm.invoke(messages)
                answer = response.content
            except Exception as e:
                answer = f"Error generating response: {e}\n\nHere's the relevant context:\n{context[:500]}..."
        else:
            # Simple template-based response
            answer = f"Based on the documents, here's what I found:\n\n{context[:1000]}...\n\n(Install OpenAI for better responses)"
        
        return {
            "answer": answer,
            "sources": [
                {
                    "source": doc["source"],
                    "text": doc["text"][:200] + "...",
                    "similarity": doc["similarity"]
                }
                for doc in relevant_docs
            ]
        }
