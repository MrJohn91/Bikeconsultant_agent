"""Vector database integration with Qdrant."""

import json
import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from .settings import settings
import tempfile


class VectorDB:
    """Vector database for bike catalog and FAQ search."""
    
    def __init__(self):
        # Use local file-based Qdrant (no server needed)
        self.client = QdrantClient(path=tempfile.mkdtemp())
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.bike_collection = "bikes"
        self.faq_collection = "faq"
        
    async def initialize(self):
        """Initialize vector database with bike catalog and FAQ data."""
        try:
            # Create collections
            await self._create_collection(self.bike_collection)
            await self._create_collection(self.faq_collection)
            
            # Load and index data
            await self._index_bikes()
            await self._index_faq()
            
        except Exception as e:
            print(f"Vector DB initialization failed: {e}")
    
    async def _create_collection(self, collection_name: str):
        """Create a collection if it doesn't exist."""
        try:
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except Exception as e:
            print(f"Failed to create collection {collection_name}: {e}")
    
    async def _index_bikes(self):
        """Index bike catalog data."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "product_catalog.json")
            with open(data_path, 'r') as f:
                bikes = json.load(f)
            
            points = []
            for bike in bikes:
                # Create searchable text
                text = f"{bike['name']} {bike['brand']} {bike['type']} {' '.join(bike['intended_use'])}"
                vector = self.encoder.encode(text).tolist()
                
                points.append(PointStruct(
                    id=bike['id'],
                    vector=vector,
                    payload=bike
                ))
            
            self.client.upsert(collection_name=self.bike_collection, points=points)
            print(f"Indexed {len(points)} bikes")
            
        except Exception as e:
            print(f"Failed to index bikes: {e}")
    
    async def _index_faq(self):
        """Index FAQ data."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "faq.txt")
            with open(data_path, 'r') as f:
                faq_content = f.read()
            
            # Parse FAQ format: numbered questions followed by answers
            lines = faq_content.split('\n')
            points = []
            faq_id = 1
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Look for numbered questions (e.g., "1. Do you offer...")
                if line and line[0].isdigit() and '. ' in line:
                    question = line.split('. ', 1)[1] if '. ' in line else line
                    answer = ""
                    
                    # Collect answer lines until next question or end
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if next_line and next_line[0].isdigit() and '. ' in next_line:
                            break
                        if next_line:  # Skip empty lines
                            answer += next_line + " "
                        j += 1
                    
                    answer = answer.strip()
                    
                    if question and answer:
                        text = f"{question} {answer}"
                        vector = self.encoder.encode(text).tolist()
                        
                        points.append(PointStruct(
                            id=faq_id,
                            vector=vector,
                            payload={"question": question, "answer": answer}
                        ))
                        faq_id += 1
                
                i += 1
            
            self.client.upsert(collection_name=self.faq_collection, points=points)
            print(f"Indexed {len(points)} FAQ items")
            
        except Exception as e:
            print(f"Failed to index FAQ: {e}")
    
    async def search_bikes(self, query: str, limit: int = 5, filters: Dict = None) -> List[Dict]:
        """Search bikes using vector similarity."""
        try:
            query_vector = self.encoder.encode(query).tolist()
            
            results = self.client.search(
                collection_name=self.bike_collection,
                query_vector=query_vector,
                limit=limit
            )
            
            bikes = []
            for result in results:
                bike = result.payload
                # Apply filters
                if filters:
                    if 'price_max' in filters and bike['price_eur'] > filters['price_max']:
                        continue
                    if 'type' in filters and bike['type'].lower() != filters['type'].lower():
                        continue
                bikes.append(bike)
            
            return bikes
            
        except Exception as e:
            print(f"Bike search failed: {e}")
            return []
    
    async def search_faq(self, question: str, limit: int = 3) -> List[Dict]:
        """Search FAQ using vector similarity."""
        try:
            query_vector = self.encoder.encode(question).tolist()
            
            results = self.client.search(
                collection_name=self.faq_collection,
                query_vector=query_vector,
                limit=limit
            )
            
            return [result.payload for result in results]
            
        except Exception as e:
            print(f"FAQ search failed: {e}")
            return []


# Global vector DB instance
vector_db = VectorDB()