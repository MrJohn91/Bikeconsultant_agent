"""Tools for the bike sales agent."""

from typing import Dict, List, Optional
from pydantic_ai import RunContext
from .dependencies import SalesAgentDependencies
import json


async def product_search_tool(
    ctx: RunContext[SalesAgentDependencies],
    query: str,
    filters: Optional[Dict] = None
) -> str:
    """Search bike catalog using vector similarity."""
    try:
        from bike_sales_agent.vector_db import vector_db
        
        # Initialize vector DB if needed
        await vector_db.initialize()
        
        # Use vector search
        bikes = await vector_db.search_bikes(query, limit=5, filters=filters)
        
        if not bikes:
            return f"No bikes found matching '{query}'"
        
        # Format results
        response = f"Found {len(bikes)} bike(s):\n\n"
        for bike in bikes[:3]:  # Top 3 results
            response += f"**{bike['name']}** by {bike['brand']}\n"
            response += f"Type: {bike['type']} | Price: €{bike['price_eur']}\n"
            response += f"Frame: {bike['frame_material']} | Gears: {bike['gears']}\n"
            response += f"Intended use: {', '.join(bike['intended_use'])}\n\n"
        
        return response
        
    except Exception as e:
        return f"Product search failed: {str(e)}"


async def create_lead_tool(
    ctx: RunContext[SalesAgentDependencies],
    name: str,
    email: str,
    phone: Optional[str] = None,
    interested_bike: Optional[str] = None
) -> str:
    """Create lead in CRM system."""
    try:
        # Mock CRM integration (would be real API call)
        lead_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "interested_bike": interested_bike,
            "source": "bike_sales_agent"
        }
        
        # Simulate CRM API call
        if ctx.deps.http_client:
            # In production: response = await ctx.deps.http_client.post(crm_url, json=lead_data)
            lead_id = f"LEAD_{hash(email) % 10000}"
            return f"Lead created successfully! Lead ID: {lead_id}"
        else:
            return "CRM service not available"
            
    except Exception as e:
        return f"Failed to create lead: {str(e)}"


async def faq_search_tool(
    ctx: RunContext[SalesAgentDependencies],
    question: str
) -> str:
    """Search FAQ knowledge base."""
    try:
        from bike_sales_agent.vector_db import vector_db
        
        # Initialize vector DB if needed
        await vector_db.initialize()
        
        # Use vector search
        faqs = await vector_db.search_faq(question, limit=3)
        
        if not faqs:
            return "I don't have specific information about that in our FAQ. Let me help you with what I know, or you can contact our customer service team."
        
        # Return best match
        best_faq = faqs[0]
        return f"Q: {best_faq['question']}\nA: {best_faq['answer']}"
        
    except Exception as e:
        return f"FAQ search failed: {str(e)}"


async def conversation_memory_tool(
    ctx: RunContext[SalesAgentDependencies],
    conversation_id: str,
    action: str,
    message: Optional[str] = None,
    role: Optional[str] = "user"
) -> str:
    """Maintain conversation context across API calls."""
    try:
        memory = ctx.deps.conversation_memory
        
        if action == "get":
            # Get conversation history
            history = memory.get(conversation_id, [])
            if not history:
                return "No conversation history found"
            return f"Conversation history: {len(history)} messages"
        
        elif action == "add_message":
            # Add message to conversation
            if conversation_id not in memory:
                memory[conversation_id] = []
            
            memory[conversation_id].append({
                "role": role,
                "message": message,
                "timestamp": "now"  # Would use real timestamp
            })
            return f"Message added to conversation {conversation_id}"
        
        elif action == "clear":
            # Clear conversation
            if conversation_id in memory:
                del memory[conversation_id]
            return f"Conversation {conversation_id} cleared"
        
        else:
            return f"Unknown action: {action}"
            
    except Exception as e:
        return f"Memory operation failed: {str(e)}"