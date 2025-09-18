"""Main bike sales agent using PydanticAI."""

from pydantic_ai import Agent, RunContext
from .dependencies import SalesAgentDependencies
from .tools import product_search_tool, create_lead_tool, faq_search_tool, conversation_memory_tool
from .settings import settings
from .vector_db import vector_db

# Create the sales agent with proper dependencies
sales_agent = Agent(
    f'openai:{settings.llm_model}',
    deps_type=SalesAgentDependencies,
    system_prompt="""You are a friendly and knowledgeable sales consultant for an online bike shop. Your goal is to help customers find the perfect bike by understanding their needs, preferences, and budget.

Key behaviors:
- Recommend specific bikes from the catalog based on customer needs using product_search tool
- Ask clarifying questions about intended use, experience level, budget when needed
- Detect genuine interest signals (asking about pricing, availability, specifications)
- When interest is confirmed, naturally collect contact information for follow-up using create_lead tool
- Answer general questions using the FAQ knowledge base with faq_search tool
- Maintain a consultative, helpful tone throughout the conversation

IMPORTANT: When customers mention bike types or budgets, use the product_search tool to show them actual bikes from our catalog. Don't just ask questions - provide concrete recommendations.

Tools available:
- product_search: Search bike catalog with query and optional filters
- create_lead: Create lead when customer shows interest
- faq_search: Search FAQ for common questions
- conversation_memory: Maintain conversation context"""
)


# Register the 4 required tools
@sales_agent.tool
async def product_search(
    ctx: RunContext[SalesAgentDependencies],
    query: str,
    filters: dict = None
) -> str:
    """Search bike catalog using vector similarity."""
    return await product_search_tool(ctx, query, filters)


@sales_agent.tool
async def create_lead(
    ctx: RunContext[SalesAgentDependencies],
    name: str,
    email: str,
    phone: str = None,
    interested_bike: str = None
) -> str:
    """Create lead in CRM system."""
    return await create_lead_tool(ctx, name, email, phone, interested_bike)


@sales_agent.tool
async def faq_search(
    ctx: RunContext[SalesAgentDependencies],
    question: str
) -> str:
    """Search FAQ knowledge base."""
    return await faq_search_tool(ctx, question)


@sales_agent.tool
async def conversation_memory(
    ctx: RunContext[SalesAgentDependencies],
    conversation_id: str,
    action: str,
    message: str = None,
    role: str = "user"
) -> str:
    """Maintain conversation context across API calls."""
    return await conversation_memory_tool(ctx, conversation_id, action, message, role)


# Global memory store to persist across requests
GLOBAL_MEMORY = {}

# Chat function for API
async def chat_with_sales_agent(message: str, conversation_id: str) -> str:
    """Chat with the sales agent."""
    dependencies = SalesAgentDependencies()
    
    # Use global memory instead of dependencies memory
    if conversation_id not in GLOBAL_MEMORY:
        GLOBAL_MEMORY[conversation_id] = []
    
    history = GLOBAL_MEMORY[conversation_id]
    
    # Build context from history
    context_prompt = ""
    if history:
        context_prompt = "\nConversation history:\n"
        for msg in history[-4:]:  # Last 4 messages
            context_prompt += f"{msg['role']}: {msg['message']}\n"
        context_prompt += f"\nCustomer: {message}\n\nBased on our conversation above, "
    
    # Add user message to memory
    GLOBAL_MEMORY[conversation_id].append({
        "role": "user",
        "message": message,
        "timestamp": "now"
    })
    
    # Run agent with context
    full_message = context_prompt + message if context_prompt else message
    result = await sales_agent.run(full_message, deps=dependencies)
    
    # Add agent response to memory
    GLOBAL_MEMORY[conversation_id].append({
        "role": "assistant", 
        "message": result.output,
        "timestamp": "now"
    })
    
    return result.output


def detect_interest(message: str) -> bool:
    """Detect if customer shows purchase interest."""
    interest_keywords = [
        'interested', 'want', 'buy', 'purchase', 'price', 'cost', 'how much',
        'available', 'in stock', 'order', 'get this', 'take this'
    ]
    return any(keyword in message.lower() for keyword in interest_keywords)