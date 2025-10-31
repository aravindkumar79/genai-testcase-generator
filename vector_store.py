from chromadb import Client, Settings
import hashlib
import json
from typing import List, Dict

class RequirementVectorStore:
    def __init__(self, persist_directory: str = "genai-testcase-generator/chroma_db/chroma_db"):
        self.client = Client(Settings(persist_directory=persist_directory, is_persistent=True))
        self.collection = self.client.get_or_create_collection("domain_agnostic_requirements")
    
    def add_requirements(self, requirements: List[Dict]):
        """Add requirements to vector database for semantic search"""
        documents = []
        metadatas = []
        ids = []
        
        for req in requirements:
            # Create unique ID from content
            doc_id = hashlib.md5(req['content'].encode()).hexdigest()[:12]
            documents.append(req['content'])
            metadatas.append({
                'type': req['type'],
                'testability_score': req['testability_score'],
                'keywords': ', '.join(req['keywords'][:5]),  # Top 5 keywords
                'validation_rules_count': len(req['validation_rules'])
            })
            ids.append(doc_id)
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(requirements)} requirements to vector store")
    
    def search_similar_requirements(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for similar requirements using semantic search"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            similar_requirements = []
            for i, doc in enumerate(results['documents'][0]):
                similar_requirements.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': results['distances'][0][i] if 'distances' in results else 0
                })
            
            return similar_requirements
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
    
    def get_requirements_by_type(self, req_type: str) -> List[Dict]:
        """Get all requirements of a specific type"""
        try:
            results = self.collection.get(
                where={"type": req_type}
            )
            
            requirements = []
            for i, doc in enumerate(results['documents']):
                requirements.append({
                    'content': doc,
                    'metadata': results['metadatas'][i]
                })
            
            return requirements
        except Exception as e:
            print(f"Filter error: {e}")
            return []
    
    def get_high_testability_requirements(self, min_score: int = 7) -> List[Dict]:
        """Get requirements with high testability scores"""
        try:
            results = self.collection.get(
                where={"testability_score": {"$gte": min_score}}
            )
            
            requirements = []
            for i, doc in enumerate(results['documents']):
                requirements.append({
                    'content': doc,
                    'metadata': results['metadatas'][i]
                })
            
            return requirements
        except Exception as e:
            print(f"Filter error: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Load extracted requirements
    with open("genai-testcase-generator/extracted_requirements/extracted_requirements.json", "r") as f:
        requirements = json.load(f)
    
    # Initialize vector store
    vector_store = RequirementVectorStore()
    
    # Add requirements to vector store
    vector_store.add_requirements(requirements)
    
    # Test semantic search
    test_query = "RTGS STP Utility real-time application"
    similar = vector_store.search_similar_requirements(test_query)
    
    print(f"\n🔍 Semantic search results for: '{test_query}'")
    for i, req in enumerate(similar):
        print(f"  {i+1}. [{req['metadata']['type']}] {req['content'][:80]}...")
    
    # Get requirements by type
    validation_reqs = vector_store.get_requirements_by_type("validation")
    print(f"\n📋 Found {len(validation_reqs)} validation requirements")
