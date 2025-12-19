"""
Terminal Interface for RAG Pipeline
Run this if you want a simple terminal interface instead of Streamlit
"""
from document_loader import DocumentLoader
from rag_pipeline import RAGPipeline
from mongodb_manager import mongo
import os

def main():
    print("=" * 60)
    print("🤖 Simple RAG System - Terminal Interface")
    print("=" * 60)
    
    # Initialize
    rag = RAGPipeline(use_groq=True)
    loader = DocumentLoader()
    
    while True:
        print("\n" + "=" * 60)
        print("Options:")
        print("1. Load documents from directory")
        print("2. Ask a question")
        print("3. View database stats")
        print("4. Clear database")
        print("5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            directory = input("Enter directory path: ").strip()
            if os.path.exists(directory):
                print("\nLoading documents...")
                chunks = loader.load_directory(directory)
                rag.vector_store.add_documents(chunks)
                print(f"✓ Added {len(chunks)} chunks to knowledge base")
            else:
                print("❌ Directory not found")
        
        elif choice == "2":
            question = input("\n💬 Your question: ").strip()
            if question:
                print("\n🤖 Thinking...")
                response = rag.query(question)
                
                print("\n" + "=" * 60)
                print("ANSWER:")
                print("=" * 60)
                print(response["answer"])
                
                if response["sources"]:
                    print("\n" + "=" * 60)
                    print("SOURCES:")
                    print("=" * 60)
                    for i, source in enumerate(response["sources"], 1):
                        print(f"\n[{i}] {source['source']}")
                        print(f"    Similarity: {source['similarity']:.3f}")
                        print(f"    {source['text']}")
        
        elif choice == "3":
            collection = mongo.get_collection("documents")
            count = collection.count_documents({})
            print(f"\n📊 Total documents in database: {count}")
        
        elif choice == "4":
            confirm = input("Are you sure you want to clear the database? (yes/no): ").strip().lower()
            if confirm == "yes":
                rag.vector_store.clear()
                print("✓ Database cleared")
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            mongo.close()
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
