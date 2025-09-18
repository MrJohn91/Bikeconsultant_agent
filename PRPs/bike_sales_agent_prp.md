---
name: "Bike Sales AI Agent PRP"
description: "Comprehensive PRP for building a Sales AI Agent for an online bike shop using PydanticAI with FastAPI REST endpoints"
---

## Purpose

Build a production-ready Sales AI Agent for an online bike shop that conducts customer consultations via REST API endpoints. The agent uses RAG with vector search for bike recommendations, detects customer interest, collects lead information, and integrates with CRM systems while supporting conversation memory across API calls.

## Core Principles

1. **PydanticAI Best Practices**: Deep integration with PydanticAI patterns for agent creation, tools, and structured outputs
2. **Production Ready**: Include security, testing, and monitoring for production deployments
3. **Type Safety First**: Leverage PydanticAI's type-safe design and Pydantic validation throughout
4. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

### What NOT to do:
- ❌ **Don't create dozens of tools** - Build only the 4 core tools: product_search, create_lead, faq_search, conversation_memory
- ❌ **Don't over-complicate dependencies** - Keep dependency injection simple with vector DB, CRM client, and Redis
- ❌ **Don't add unnecessary abstractions** - Follow main_agent_reference patterns directly
- ❌ **Don't build complex workflows** unless specifically required
- ❌ **Don't add structured output** for conversation responses (default to string), only for lead collection
- ❌ **Don't build in the examples/ folder**

### What TO do:
- ✅ **Start simple** - Build the minimum viable agent that meets requirements
- ✅ **Add tools incrementally** - Implement only the 4 required tools
- ✅ **Follow main_agent_reference** - Use proven patterns, don't reinvent
- ✅ **Use string output by default** - Only add result_type for lead collection validation
- ✅ **Test early and often** - Use TestModel to validate as you build

### Key Question:
**"Does this agent really need this feature to accomplish its core sales consultation purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

Create a Sales AI Agent that acts as a knowledgeable bike shop consultant, helping customers find the perfect bike through natural conversation, detecting genuine purchase interest, collecting lead information when appropriate, and integrating with CRM systems for follow-up sales processes.

## Why

Online bike shops need intelligent sales assistance that can:
- Provide personalized bike recommendations based on customer needs
- Maintain conversation context across multiple API interactions
- Detect genuine purchase interest and collect leads efficiently
- Answer common questions without human intervention
- Scale customer consultations beyond human capacity
- Integrate seamlessly with existing CRM and sales workflows

## What

### Agent Type Classification
- [x] **Chat Agent**: Conversational interface with memory and context
- [x] **Tool-Enabled Agent**: Agent with external tool integration capabilities
- [ ] **Workflow Agent**: Multi-step task processing and orchestration
- [x] **Structured Output Agent**: Complex data validation and formatting (for lead collection only)

### Model Provider Requirements
- [x] **OpenAI**: `openai:gpt-4o` or `openai:gpt-4o-mini`
- [x] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022` or `anthropic:claude-3-5-haiku-20241022`
- [x] **Google**: `gemini-1.5-flash` or `gemini-1.5-pro`
- [x] **Fallback Strategy**: Multiple provider support with automatic failover

### External Integrations
- [x] Database connections: Qdrant vector database for product and FAQ search
- [x] REST API integrations: CRM system for lead management
- [x] File system operations: Loading bike catalog (bike_shop.json) and FAQ (faq.txt)
- [ ] Web scraping or search capabilities
- [x] Real-time data sources: Redis for conversation state management

### Success Criteria
- [x] Agent successfully handles bike consultation conversations with natural flow
- [x] All 4 tools work correctly with proper error handling (product_search, create_lead, faq_search, conversation_memory)
- [x] Structured outputs validate for lead collection with Pydantic models
- [x] Comprehensive test coverage with TestModel and FunctionModel
- [x] Security measures implemented (API keys, input validation, rate limiting)
- [x] Performance meets requirements (response time < 2s, handles concurrent conversations)
- [x] FastAPI REST endpoints with proper OpenAPI documentation
- [x] Docker deployment with environment-based configuration

## All Needed Context

### PydanticAI Documentation & Research

```yaml
# MCP servers
- mcp: Archon
  query: "PydanticAI agent creation model providers tools dependencies FastAPI integration"
  why: Core framework understanding and latest patterns for web API integration

# ESSENTIAL PYDANTIC AI DOCUMENTATION - Must be researched
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with getting started guide
  content: Agent creation, model providers, dependency injection patterns

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns
  content: System prompts, output types, execution methods, agent composition

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration
  content: @agent.tool decorators, RunContext usage, parameter validation

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to PydanticAI agents
  content: TestModel, FunctionModel, Agent.override(), pytest patterns

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and authentication
  content: OpenAI, Anthropic, Gemini setup, API key management, fallback models

# Prebuilt examples
- path: examples/
  why: Reference implementations for Pydantic AI agents
  content: A bunch of already built simple Pydantic AI examples to reference including how to set up models and providers

- path: examples/main_agent_reference/
  why: Shows production-ready agent architecture patterns
  content: settings.py, providers.py, tools.py, models.py structure for scalable agents
```

### Agent Architecture Research

```yaml
# PydanticAI Architecture Patterns (follow main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Environment-based configuration with pydantic-settings
    - providers.py: Model provider abstraction with get_llm_model()
    - Environment variables: OPENAI_API_KEY, CRM_API_URL, VECTOR_DB_PATH, REDIS_URL
    - Never hardcode model strings like "openai:gpt-4o"
  
  agent_definition:
    - Default to string output for conversations (no result_type)
    - Use structured output only for lead collection (LeadData model)
    - Use get_llm_model() from providers.py for model configuration
    - System prompts focused on sales consultation behavior
    - Dataclass dependencies for vector DB, CRM client, Redis
  
  tool_integration:
    - @agent.tool for context-aware tools with RunContext[DepsType]
    - 4 core tools: product_search, create_lead, faq_search, conversation_memory
    - Tool functions as pure functions that can be called independently
    - Proper error handling and logging in tool implementations
    - Dependency injection through RunContext.deps
  
  testing_strategy:
    - TestModel for rapid development validation
    - FunctionModel for custom behavior testing  
    - Agent.override() for test isolation
    - Comprehensive tool testing with mocks for vector DB and CRM
```

### Security and Production Considerations

```yaml
# PydanticAI Security Patterns (research required)
security_requirements:
  api_management:
    environment_variables: ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "CRM_API_KEY"]
    secure_storage: "Never commit API keys to version control"
    rotation_strategy: "Plan for key rotation and management"
  
  input_validation:
    sanitization: "Validate all user inputs with Pydantic models"
    prompt_injection: "Implement prompt injection prevention strategies"
    rate_limiting: "Prevent abuse with proper throttling on FastAPI endpoints"
  
  output_security:
    data_filtering: "Ensure no sensitive data in agent responses"
    content_validation: "Validate output structure and content"
    logging_safety: "Safe logging without exposing secrets or customer data"
```

### Common PydanticAI Gotchas (research and document)

```yaml
# Agent-specific gotchas to research and address
implementation_gotchas:
  async_patterns:
    issue: "Mixing sync and async agent calls inconsistently with FastAPI"
    research: "PydanticAI async/await best practices with web frameworks"
    solution: "[To be documented based on research]"
  
  model_limits:
    issue: "Different models have different capabilities and token limits"
    research: "Model provider comparison and capabilities for sales conversations"
    solution: "[To be documented based on research]"
  
  dependency_complexity:
    issue: "Complex dependency graphs with vector DB, CRM, and Redis can be hard to debug"
    research: "Dependency injection best practices in PydanticAI for web services"
    solution: "[To be documented based on research]"
  
  tool_error_handling:
    issue: "Tool failures (vector search, CRM API) can crash entire agent runs"
    research: "Error handling and retry patterns for tools in production"
    solution: "[To be documented based on research]"
```

## Implementation Blueprint

### Technology Research Phase

**RESEARCH REQUIRED - Complete before implementation:**

✅ **PydanticAI Framework Deep Dive:**
- [ ] Agent creation patterns and best practices for sales conversations
- [ ] Model provider configuration and fallback strategies
- [ ] Tool integration patterns (@agent.tool vs @agent.tool_plain)
- [ ] Dependency injection system for external services (vector DB, CRM, Redis)
- [ ] Testing strategies with TestModel and FunctionModel

✅ **FastAPI Integration Investigation:**
- [ ] PydanticAI agent integration with FastAPI endpoints
- [ ] Async request handling and conversation state management
- [ ] OpenAPI documentation generation for agent endpoints
- [ ] Error handling and response formatting
- [ ] Rate limiting and security middleware

✅ **Vector Search and RAG Patterns:**
- [ ] Qdrant integration for bike catalog and FAQ search
- [ ] Vector embedding strategies for product recommendations
- [ ] RAG implementation patterns with PydanticAI tools
- [ ] Performance optimization for vector search
- [ ] Data loading and indexing strategies

✅ **CRM Integration and Lead Management:**
- [ ] REST API client patterns for CRM integration
- [ ] Lead data validation with Pydantic models
- [ ] Error handling and retry mechanisms for external APIs
- [ ] Data mapping and transformation strategies
- [ ] Webhook integration for real-time updates

### Agent Implementation Plan

```yaml
Implementation Task 1 - Project Structure and Configuration:
  CREATE bike_sales_agent project structure:
    - settings.py: Environment-based configuration with pydantic-settings
    - providers.py: Model provider abstraction with get_llm_model()
    - agent.py: Main sales agent definition (default string output)
    - tools.py: 4 core tool functions with proper decorators
    - dependencies.py: Vector DB, CRM, Redis integrations (dataclasses)
    - models.py: Pydantic models for lead data and API responses
    - api.py: FastAPI endpoints for agent interaction
    - tests/: Comprehensive test suite
    - docker/: Docker configuration and deployment files
    - data/: bike_shop.json and faq.txt data files

Implementation Task 2 - Core Sales Agent Development:
  IMPLEMENT agent.py following main_agent_reference patterns:
    - Use get_llm_model() from providers.py for model configuration
    - Sales consultant system prompt with bike shop expertise
    - Dependency injection with SalesAgentDependencies dataclass
    - NO result_type for conversations (default string output)
    - Error handling and logging for production use

Implementation Task 3 - Tool Integration (4 Core Tools):
  DEVELOP tools.py with required sales tools:
    - product_search: Vector search in bike catalog with filters
    - create_lead: CRM integration with structured lead data
    - faq_search: Vector search in FAQ knowledge base
    - conversation_memory: Redis-based conversation state management
    - RunContext[SalesAgentDependencies] integration
    - Parameter validation with proper type hints
    - Error handling and retry mechanisms for external services

Implementation Task 4 - Data Models and Dependencies:
  CREATE models.py and dependencies.py:
    - LeadData: Pydantic model for lead collection (name, email, phone)
    - BikeRecommendation: Model for product search results
    - ConversationState: Model for conversation memory
    - SalesAgentDependencies: Dataclass for vector DB, CRM, Redis clients
    - Input validation models for API endpoints
    - Custom validators and business logic constraints

Implementation Task 5 - FastAPI Integration:
  IMPLEMENT api.py with REST endpoints:
    - POST /chat: Main conversation endpoint with conversation_id
    - GET /health: Health check endpoint
    - POST /leads: Direct lead creation endpoint
    - GET /products/search: Product search endpoint
    - OpenAPI documentation with proper schemas
    - Rate limiting and security middleware
    - Error handling and response formatting

Implementation Task 6 - Vector Database and Data Loading:
  SETUP vector search infrastructure:
    - Qdrant database initialization and configuration
    - Data loading scripts for bike_shop.json and faq.txt
    - Vector embedding generation for products and FAQs
    - Search optimization and indexing strategies
    - Database migration and update procedures

Implementation Task 7 - Comprehensive Testing:
  IMPLEMENT testing suite:
    - TestModel integration for rapid development
    - FunctionModel tests for custom sales behavior
    - Agent.override() patterns for isolation
    - Integration tests with real providers
    - Tool validation and error scenario testing
    - FastAPI endpoint testing with test client
    - Load testing for concurrent conversations

Implementation Task 8 - Docker Deployment and Production Setup:
  SETUP production deployment:
    - Multi-stage Dockerfile for optimized builds
    - Docker Compose with Qdrant, Redis, and application services
    - Environment variable management for different environments
    - Health checks and monitoring configuration
    - Logging and observability setup
    - CI/CD pipeline configuration
```

## Validation Loop

### Level 1: Agent Structure Validation

```bash
# Verify complete agent project structure
find bike_sales_agent -name "*.py" | sort
test -f bike_sales_agent/agent.py && echo "Sales agent definition present"
test -f bike_sales_agent/tools.py && echo "Tools module present"
test -f bike_sales_agent/models.py && echo "Models module present"
test -f bike_sales_agent/dependencies.py && echo "Dependencies module present"
test -f bike_sales_agent/api.py && echo "FastAPI module present"

# Verify proper PydanticAI imports
grep -q "from pydantic_ai import Agent" bike_sales_agent/agent.py
grep -q "@agent.tool" bike_sales_agent/tools.py
grep -q "from pydantic import BaseModel" bike_sales_agent/models.py
grep -q "from fastapi import FastAPI" bike_sales_agent/api.py

# Expected: All required files with proper PydanticAI and FastAPI patterns
# If missing: Generate missing components with correct patterns
```

### Level 2: Agent Functionality Validation

```bash
# Test agent can be imported and instantiated
python -c "
from bike_sales_agent.agent import sales_agent
print('Sales agent created successfully')
print(f'Model: {sales_agent.model}')
print(f'Tools: {len(sales_agent.tools)}')
print(f'Expected tools: product_search, create_lead, faq_search, conversation_memory')
"

# Test with TestModel for validation
python -c "
from pydantic_ai.models.test import TestModel
from bike_sales_agent.agent import sales_agent
test_model = TestModel()
with sales_agent.override(model=test_model):
    result = sales_agent.run_sync('I need help finding a bike for commuting')
    print(f'Agent response: {result.data}')
"

# Expected: Agent instantiation works, 4 tools registered, TestModel validation passes
# If failing: Debug agent configuration and tool registration
```

### Level 3: FastAPI Integration Validation

```bash
# Test FastAPI application startup
cd bike_sales_agent
python -c "
from api import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get('/health')
print(f'Health check status: {response.status_code}')
print(f'Health check response: {response.json()}')
"

# Test main chat endpoint
python -c "
from api import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.post('/chat', json={
    'message': 'Hello, I need help finding a bike',
    'conversation_id': 'test-123'
})
print(f'Chat endpoint status: {response.status_code}')
print(f'Chat response: {response.json()}')
"

# Expected: FastAPI app starts, health check passes, chat endpoint responds
# If failing: Debug FastAPI integration and endpoint configuration
```

### Level 4: Tool Integration Validation

```bash
# Test vector database connection
python -c "
from bike_sales_agent.dependencies import SalesAgentDependencies
from bike_sales_agent.tools import product_search
# Test with mock dependencies
print('Testing product search tool...')
"

# Test CRM integration
python -c "
from bike_sales_agent.tools import create_lead
from bike_sales_agent.models import LeadData
# Test lead creation with validation
print('Testing lead creation tool...')
"

# Run complete test suite
python -m pytest tests/ -v

# Expected: All tools work with proper error handling, tests pass
# If failing: Fix tool implementations and external service integrations
```

### Level 5: Production Readiness Validation

```bash
# Verify security patterns
grep -r "API_KEY" bike_sales_agent/ | grep -v ".py:" # Should not expose keys
test -f bike_sales_agent/.env.example && echo "Environment template present"

# Check Docker configuration
test -f Dockerfile && echo "Dockerfile present"
test -f docker-compose.yml && echo "Docker Compose present"

# Verify data files
test -f data/bike_shop.json && echo "Bike catalog present"
test -f data/faq.txt && echo "FAQ data present"

# Check error handling
grep -r "try:" bike_sales_agent/ | wc -l  # Should have error handling
grep -r "except" bike_sales_agent/ | wc -l  # Should have exception handling

# Expected: Security measures in place, Docker ready, data files present, error handling comprehensive
# If issues: Implement missing security and production patterns
```

## Final Validation Checklist

### Agent Implementation Completeness

- [ ] Complete agent project structure: `agent.py`, `tools.py`, `models.py`, `dependencies.py`, `api.py`
- [ ] Sales agent instantiation with proper model provider configuration
- [ ] 4 core tools registered: product_search, create_lead, faq_search, conversation_memory
- [ ] Structured outputs with Pydantic model validation for lead collection
- [ ] Dependency injection for vector DB, CRM, and Redis properly configured and tested
- [ ] FastAPI integration with proper REST endpoints and OpenAPI documentation
- [ ] Comprehensive test suite with TestModel and FunctionModel

### PydanticAI Best Practices

- [ ] Type safety throughout with proper type hints and validation
- [ ] Security patterns implemented (API keys, input validation, rate limiting)
- [ ] Error handling and retry mechanisms for robust operation
- [ ] Async/sync patterns consistent and appropriate for web API
- [ ] Documentation and code comments for maintainability

### Production Readiness

- [ ] Environment configuration with .env files and validation
- [ ] Docker deployment with multi-service orchestration
- [ ] Vector database initialization and data loading
- [ ] CRM integration with proper error handling
- [ ] Conversation state management with Redis
- [ ] Logging and monitoring setup for observability
- [ ] Performance optimization and resource management
- [ ] Maintenance and update strategies documented

---

## Anti-Patterns to Avoid

### PydanticAI Agent Development

- ❌ Don't skip TestModel validation - always test with TestModel during development
- ❌ Don't hardcode API keys - use environment variables for all credentials
- ❌ Don't ignore async patterns - PydanticAI has specific async/sync requirements for FastAPI
- ❌ Don't create complex tool chains - keep the 4 tools focused and composable
- ❌ Don't skip error handling - implement comprehensive retry and fallback mechanisms

### Sales Agent Architecture

- ❌ Don't mix conversation and lead collection outputs - use string for chat, structured for leads
- ❌ Don't ignore conversation state - implement proper memory management across API calls
- ❌ Don't skip input validation - sanitize and validate all customer inputs
- ❌ Don't forget tool documentation - ensure all 4 tools have proper descriptions and schemas
- ❌ Don't ignore sales flow - design natural conversation patterns that detect genuine interest

### Security and Production

- ❌ Don't expose customer data - validate all outputs and logs for privacy
- ❌ Don't skip rate limiting - implement proper throttling for API endpoints
- ❌ Don't ignore CRM failures - implement graceful degradation when external services fail
- ❌ Don't deploy without monitoring - include proper observability from the start
- ❌ Don't forget data persistence - ensure conversation state and leads are properly stored

**RESEARCH STATUS: [TO BE COMPLETED]** - Complete comprehensive PydanticAI and FastAPI integration research before implementation begins.