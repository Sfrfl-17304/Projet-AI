"""
RAG Pipeline - Retrieval Augmented Generation with Neo4j
"""
import os
from typing import List, Optional
from dotenv import load_dotenv
from vector_store import VectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class RAGPipeline:
    def __init__(self, use_groq=True, neo4j_manager=None):
        """Initialize RAG pipeline"""
        self.vector_store = VectorStore()
        self.neo4j_manager = neo4j_manager

        # Initialize LLM (Groq or fallback to simple template)
        self.use_groq = use_groq
        groq_api_key = os.getenv("GROQ_API_KEY")
        groq_api_url = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
        if use_groq and groq_api_key:
            try:
                self.llm = ChatGroq(
                    model="llama-3.1-8b-instant",  # Updated to a supported Groq model
                    temperature=0.7,
                    groq_api_key=groq_api_key
                )
                print("✓ Using Groq for response generation")
            except Exception as e:
                print(f"⚠ Could not initialize Groq: {e}")
                self.use_groq = False
        else:
            self.use_groq = False
            print("✓ Using template-based responses (no LLM)")

        # Create prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the question based on the context provided. If you cannot answer from the context, say so."),
            ("user", """Context:
{context}

Question: {question}

Answer:""")
        ])
        
        # Create skills-focused prompt template
        self.skills_prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a career advisor AI assistant. Use the knowledge graph data and context provided to give personalized career recommendations. 
Be specific, helpful, and mention actual skills, fields, and percentages from the data."""),
            ("user", """Knowledge Graph Data:
{graph_context}

User's Skills: {user_skills}

Question: {question}

Provide a detailed, personalized answer based on the user's skills and the available career fields."""
)
        ])
    
    def query_with_skills(self, question: str, user_skills: List[str]) -> dict:
        """Query with skills context from Neo4j"""
        if not self.neo4j_manager or not user_skills:
            return self.query(question)
        
        # Get recommendations from Neo4j
        recommendations = self.neo4j_manager.get_field_recommendations(user_skills)
        evaluation = self.neo4j_manager.evaluate_skills(user_skills)
        
        # Build graph context
        graph_context = "Career Field Analysis:\n\n"
        
        for rec in recommendations[:3]:
            graph_context += f"**{rec['field']}** ({rec['match_percentage']:.1f}% match)\n"
            graph_context += f"- Your matching skills: {', '.join(rec['your_skills'][:5])}\n"
            if rec['skills_to_learn']:
                graph_context += f"- Skills to learn: {', '.join(rec['skills_to_learn'][:3])}\n"
            graph_context += "\n"
        
        # Generate answer using skills template
        if self.use_groq:
            try:
                messages = self.skills_prompt_template.format_messages(
                    graph_context=graph_context,
                    user_skills=", ".join(user_skills),
                    question=question
                )
                response = self.llm.invoke(messages)
                answer = response.content
            except Exception as e:
                answer = f"Based on your skills analysis:\n\n{graph_context}"
        else:
            answer = f"Based on your skills analysis:\n\n{graph_context}"
        
        return {
            "answer": answer,
            "sources": [],
            "recommendations": recommendations,
            "evaluation": evaluation
        }
    
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
        if self.use_groq:
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
            answer = f"Based on the documents, here's what I found:\n\n{context[:1000]}...\n\n(Install Groq for better responses)"

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
