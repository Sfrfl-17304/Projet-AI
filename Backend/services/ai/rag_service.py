"""
RAG (Retrieval-Augmented Generation) Service
Implements chat assistant with grounded responses using knowledge base
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict, Optional
from config.ai_config import ai_settings
from .llm_service import get_llm_service
import logging
import os

logger = logging.getLogger(__name__)


class RAGService:
    """RAG-based chat assistant for career guidance"""
    
    def __init__(self):
        """Initialize RAG service with vector store and retrieval chain"""
        self.embeddings = None
        self.vector_store = None
        self.retrieval_chain = None
        self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize RAG components"""
        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=ai_settings.embeddings_model,
                cache_folder=ai_settings.hf_model_cache_dir,
                model_kwargs={'device': ai_settings.device}
            )
            logger.info("RAG embeddings initialized")
            
            # Initialize or load vector store
            if os.path.exists(ai_settings.chroma_persist_directory):
                self.vector_store = Chroma(
                    persist_directory=ai_settings.chroma_persist_directory,
                    embedding_function=self.embeddings
                )
                logger.info("Loaded existing vector store")
            else:
                # Create new vector store with initial knowledge
                self._create_initial_knowledge_base()
            
            # Initialize retrieval chain
            self._setup_retrieval_chain()
        
        except Exception as e:
            logger.error(f"Error initializing RAG: {e}")
            raise
    
    def _create_initial_knowledge_base(self):
        """Create initial knowledge base with career information"""
        logger.info("Creating initial knowledge base")
        
        # Initial career guidance documents
        initial_docs = [
            {
                "content": """
                Data Engineer Role: Data Engineers design, build, and maintain data pipelines 
                and infrastructure. Key skills include Python, SQL, Apache Spark, Airflow, 
                cloud platforms (AWS/Azure/GCP), and data warehousing. They typically need 
                strong database knowledge and ETL experience. Career progression often leads 
                to Senior Data Engineer or Data Architect roles.
                """,
                "metadata": {"category": "role_description", "role": "Data Engineer"}
            },
            {
                "content": """
                Machine Learning Engineer: ML Engineers develop and deploy machine learning 
                models in production. Essential skills include Python, TensorFlow/PyTorch, 
                scikit-learn, MLOps, Docker, and cloud platforms. They need strong math 
                foundations and software engineering skills. Career paths include Senior 
                ML Engineer, ML Architect, or AI Research Scientist.
                """,
                "metadata": {"category": "role_description", "role": "ML Engineer"}
            },
            {
                "content": """
                Full Stack Developer: Full Stack Developers work on both frontend and backend. 
                Frontend skills: React, Vue.js, Angular, HTML/CSS, JavaScript. Backend skills: 
                Node.js, Python (Django/Flask), databases, APIs. They build complete web 
                applications and need versatile programming skills. Career growth leads to 
                Technical Lead or Solutions Architect.
                """,
                "metadata": {"category": "role_description", "role": "Full Stack Developer"}
            },
            {
                "content": """
                Frontend Developer: Frontend Developers create user interfaces and experiences. 
                Core skills include HTML, CSS, JavaScript, React/Vue/Angular, responsive design, 
                and accessibility. Modern frontend also requires TypeScript, state management, 
                and performance optimization. Career paths include Senior Frontend Developer 
                or UI/UX Engineering Lead.
                """,
                "metadata": {"category": "role_description", "role": "Frontend Developer"}
            },
            {
                "content": """
                Backend Developer: Backend Developers build server-side logic and APIs. 
                Languages include Python, Java, Node.js, Go. Skills needed: databases (SQL/NoSQL), 
                REST APIs, microservices, cloud platforms, security. They ensure scalability 
                and performance. Career progression includes Backend Architect or Platform Engineer.
                """,
                "metadata": {"category": "role_description", "role": "Backend Developer"}
            },
            {
                "content": """
                Python Learning Path: Start with basics (variables, loops, functions), then 
                learn OOP concepts. Move to popular libraries: pandas for data, Flask/Django 
                for web, NumPy for computation. Practice with projects like web scrapers, 
                data analysis scripts, or APIs. Timeline: 3-6 months for fundamentals.
                """,
                "metadata": {"category": "learning_path", "skill": "Python"}
            },
            {
                "content": """
                React Learning Path: Start with JavaScript ES6+ features, then React fundamentals 
                (components, props, state). Learn hooks, context API, and routing. Advanced: 
                state management (Redux), performance optimization, testing. Build projects: 
                todo app, weather app, e-commerce site. Timeline: 2-4 months.
                """,
                "metadata": {"category": "learning_path", "skill": "React"}
            },
            {
                "content": """
                Machine Learning Learning Path: Prerequisites: Python, math (linear algebra, 
                calculus, statistics). Learn ML fundamentals, supervised/unsupervised learning, 
                scikit-learn. Then deep learning with TensorFlow/PyTorch. Practice with Kaggle 
                datasets. Timeline: 6-12 months for solid foundation.
                """,
                "metadata": {"category": "learning_path", "skill": "Machine Learning"}
            },
            {
                "content": """
                SQL and Databases: Start with SQL basics (SELECT, JOIN, WHERE, GROUP BY). 
                Learn database design, normalization, indexing. Practice with PostgreSQL or 
                MySQL. Advanced: query optimization, transactions, stored procedures. Essential 
                for backend and data roles. Timeline: 1-3 months.
                """,
                "metadata": {"category": "learning_path", "skill": "SQL"}
            },
            {
                "content": """
                Career Transition Tips: Start by identifying transferable skills. Build projects 
                in your target field. Contribute to open source. Network on LinkedIn and attend 
                meetups. Consider bootcamps or online courses. Create a portfolio showcasing 
                your work. Be patient - transitions typically take 6-12 months of dedicated effort.
                """,
                "metadata": {"category": "career_advice", "topic": "career_transition"}
            },
            {
                "content": """
                Building a Portfolio: Include 3-5 quality projects demonstrating different skills. 
                Host on GitHub with detailed READMEs. Deploy projects (Netlify, Heroku, Vercel). 
                Write blog posts explaining your projects. Include personal website/portfolio. 
                Quality over quantity - show depth of understanding.
                """,
                "metadata": {"category": "career_advice", "topic": "portfolio"}
            },
            {
                "content": """
                Technical Interview Preparation: Practice data structures and algorithms on 
                LeetCode/HackerRank. Study system design for senior roles. Prepare behavioral 
                questions (STAR method). Review projects deeply. Do mock interviews. Typical 
                preparation: 2-3 months for entry level, 3-6 months for senior positions.
                """,
                "metadata": {"category": "career_advice", "topic": "interviews"}
            }
        ]
        
        # Add documents to vector store
        texts = [doc["content"] for doc in initial_docs]
        metadatas = [doc["metadata"] for doc in initial_docs]
        
        self.vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=ai_settings.chroma_persist_directory
        )
        self.vector_store.persist()
        logger.info(f"Created knowledge base with {len(initial_docs)} documents")
    
    def _setup_retrieval_chain(self):
        """Setup the retrieval QA chain"""
        if not self.vector_store:
            logger.warning("Vector store not initialized")
            return
        
        llm_service = get_llm_service()
        if not llm_service.llm:
            logger.warning("LLM not available for RAG chain")
            return
        
        # Create custom prompt
        prompt_template = """
        You are a helpful career advisor assistant for SkillAtlas. 
        Use the following context to answer the question. If you cannot answer 
        based on the context, say so and provide general guidance.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer: Provide a helpful, specific answer based on the context above.
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval chain
        self.retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm_service.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": ai_settings.retrieval_top_k}
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        logger.info("Retrieval chain initialized")
    
    def ask_question(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, any]:
        """
        Ask a question to the RAG assistant
        
        Args:
            question: User's question
            conversation_history: Optional previous conversation context
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.retrieval_chain:
            # Fallback to simple retrieval
            return self._fallback_answer(question)
        
        try:
            # Add conversation context if available
            context_question = question
            if conversation_history:
                recent_context = "\n".join([
                    f"Q: {item['question']}\nA: {item['answer']}"
                    for item in conversation_history[-3:]  # Last 3 exchanges
                ])
                context_question = f"Previous context:\n{recent_context}\n\nCurrent question: {question}"
            
            # Get answer from retrieval chain
            result = self.retrieval_chain({"query": context_question})
            
            answer = result.get("result", "I don't have enough information to answer that.")
            source_docs = result.get("source_documents", [])
            
            # Format sources
            sources = []
            for doc in source_docs:
                sources.append({
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": "high" if len(source_docs) > 0 else "low"
            }
        
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            return self._fallback_answer(question)
    
    def _fallback_answer(self, question: str) -> Dict[str, any]:
        """Fallback answer when RAG is not available"""
        # Simple retrieval without LLM
        if self.vector_store:
            docs = self.vector_store.similarity_search(question, k=3)
            if docs:
                answer = "Based on available information: " + " ".join([
                    doc.page_content[:150] for doc in docs
                ])
                return {
                    "answer": answer,
                    "sources": [{"content": doc.page_content} for doc in docs],
                    "confidence": "medium"
                }
        
        return {
            "answer": "I don't have specific information about that. Please try rephrasing your question or ask about career roles, learning paths, or skill development.",
            "sources": [],
            "confidence": "low"
        }
    
    def add_documents(
        self,
        documents: List[Dict[str, any]],
        chunk: bool = True
    ) -> int:
        """
        Add new documents to the knowledge base
        
        Args:
            documents: List of documents with 'content' and optional 'metadata'
            chunk: Whether to split documents into chunks
            
        Returns:
            Number of documents added
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return 0
        
        try:
            texts = []
            metadatas = []
            
            for doc in documents:
                content = doc.get("content", "")
                metadata = doc.get("metadata", {})
                
                if chunk and len(content) > ai_settings.chunk_size:
                    # Split large documents
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=ai_settings.chunk_size,
                        chunk_overlap=ai_settings.chunk_overlap
                    )
                    chunks = splitter.split_text(content)
                    texts.extend(chunks)
                    metadatas.extend([metadata] * len(chunks))
                else:
                    texts.append(content)
                    metadatas.append(metadata)
            
            # Add to vector store
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            self.vector_store.persist()
            
            logger.info(f"Added {len(texts)} text chunks to knowledge base")
            return len(texts)
        
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return 0
    
    def search_knowledge_base(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, any]]:
        """
        Search the knowledge base
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching documents with scores
        """
        if not self.vector_store:
            return []
        
        try:
            # Perform similarity search
            if filter_metadata:
                results = self.vector_store.similarity_search_with_score(
                    query,
                    k=top_k,
                    filter=filter_metadata
                )
            else:
                results = self.vector_store.similarity_search_with_score(
                    query,
                    k=top_k
                )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score)
                })
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_knowledge_base_stats(self) -> Dict[str, any]:
        """Get statistics about the knowledge base"""
        if not self.vector_store:
            return {"status": "not_initialized"}
        
        try:
            # Get collection stats
            collection = self.vector_store._collection
            count = collection.count()
            
            return {
                "status": "active",
                "document_count": count,
                "persist_directory": ai_settings.chroma_persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "message": str(e)}


# Global instance
_rag_service_instance = None


def get_rag_service() -> RAGService:
    """Get singleton instance of RAGService"""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance

