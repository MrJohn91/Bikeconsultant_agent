"""Dependencies for the bike sales agent."""

from dataclasses import dataclass
from typing import Optional
import httpx
import json
import os


@dataclass
class SalesAgentDependencies:
    """Dependencies for the sales agent."""
    
    # Vector database client (mock for now)
    vector_client: Optional[object] = None
    
    # HTTP client for CRM integration
    http_client: Optional[httpx.AsyncClient] = None
    
    # Conversation memory (mock for now)
    conversation_memory: Optional[dict] = None
    
    # Bike catalog data
    bike_catalog: Optional[list] = None
    
    # FAQ data
    faq_data: Optional[str] = None
    
    def __post_init__(self):
        """Initialize dependencies."""
        if self.http_client is None:
            self.http_client = httpx.AsyncClient()
        
        if self.conversation_memory is None:
            self.conversation_memory = {}
            
        if self.bike_catalog is None:
            self.bike_catalog = self._load_bike_catalog()
            
        if self.faq_data is None:
            self.faq_data = self._load_faq_data()
    
    def _load_bike_catalog(self) -> list:
        """Load bike catalog from Data folder."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "product_catalog.json")
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def _load_faq_data(self) -> str:
        """Load FAQ data from Data folder."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "faq.txt")
            with open(data_path, 'r') as f:
                return f.read()
        except Exception:
            return "FAQ not available"