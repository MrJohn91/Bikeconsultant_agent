## FEATURE:

Build a Sales AI Agent for an online bike shop that conducts customer consultations via REST API. The agent should recommend products using RAG and vector search from a bike catalog, detect customer interest, collect lead information when interest is confirmed, and integrate with a CRM system. The agent must also answer FAQ questions and support both OpenAI and local LLM options.

Core functionality:
- Multi-turn conversation API (REST) with context awareness
- Product recommendations from bike_shop.json using RAG and vector search
- Lead collection (name, email, phone) when interest confirmed
- CRM integration via POST 
- FAQ support from faq.txt using vector search
- Docker deployment with flexible LLM options

## TOOLS:

- **product_search**: Search bike catalog using vector similarity, arguments: query (string), filters (optional dict for price/type), returns: list of matching bikes with details
- **create_lead**: Create lead in CRM system, arguments: name, email, phone, returns: lead_id or error
- **faq_search**: Search FAQ knowledge base, arguments: question (string), returns: relevant FAQ answers
- **conversation_memory**: Maintain conversation context across API calls, arguments: conversation_id, message, returns: updated context

## DEPENDENCIES

- Vector database (Qdrant) for product and FAQ search
- HTTP client for CRM API integration
- Conversation state management (Redis or in-memory)
- Environment variables: OPENAI_API_KEY, CRM_API_URL, VECTOR_DB_PATH
- FastAPI for REST endpoints
- Pydantic models for lead data validation

## SYSTEM PROMPT(S)

You are a friendly and knowledgeable sales consultant for an online bike shop. Your goal is to help customers find the perfect bike by understanding their needs, preferences, and budget. 

Key behaviors:
- Ask clarifying questions about intended use, experience level, budget
- Recommend specific bikes from the catalog based on customer needs
- Detect genuine interest signals (asking about pricing, availability, specifications)
- When interest is confirmed, naturally collect contact information for follow-up
- Answer general questions using the FAQ knowledge base
- Maintain a consultative, helpful tone throughout the conversation

## EXAMPLES:

Follow these existing patterns:
- examples/tool_enabled_agent - For CRM API integration and external tool calls
- examples/structured_output_agent - For lead data collection with validation
- examples/main_agent_reference - For multi-tool architecture and configuration
- examples/basic_chat_agent - For conversation memory and context management

## DOCUMENTATION:

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Qdrant Documentation: https://qdrant.tech/documentation/
- Pydantic AI Official Documentation: https://ai.pydantic.dev/
- Vector Search Best Practices: https://ai.pydantic.dev/tools/
- Docker Deployment Guide: https://fastapi.tiangolo.com/deployment/docker/

## OTHER CONSIDERATIONS:

- Implement conversation state management across API calls using conversation_id
- Handle CRM API failures gracefully with retry logic and user-friendly error messages
- Initialize vector database with bike catalog and FAQ data on startup
- Use prompt engineering for natural sales conversations that don't feel robotic
- Implement rate limiting and basic API security
- Support both streaming and non-streaming responses
- Ensure proper error handling for malformed requests
- Use environment-based configuration for easy deployment switching between OpenAI and local LLMs
