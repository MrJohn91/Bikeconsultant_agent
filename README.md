# 🚴‍♂️ Bike Sales AI Agent

A production-ready PydanticAI-powered sales consultant for online bike shops that conducts intelligent customer consultations via REST API with conversation memory, vector search, and CRM integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This AI agent acts as a knowledgeable bike shop consultant that:
- **Understands customer needs** through natural conversation
- **Recommends bikes** using vector similarity search
- **Maintains conversation memory** across multiple API calls
- **Detects purchase interest** and collects leads
- **Answers FAQ questions** using semantic search
- **Integrates with CRM systems** for lead management

### Key Capabilities
- 🧠 **Conversation Memory**: Remembers context across chat sessions
- 🔍 **Vector Search**: Semantic search through 15+ bike catalog
- 📚 **FAQ Support**: Intelligent answers from knowledge base
- 🎯 **Interest Detection**: Identifies purchase signals automatically
- 🔗 **CRM Integration**: Automated lead collection and management
- 🔒 **Secure**: Environment-based configuration with no exposed credentials

## 🏗️ Architecture

### System Design

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   PydanticAI    │
│   (Postman/Web) │───▶│   REST API      │───▶│   Agent         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Vector DB     │    │   Tools Layer   │
│   • Bikes JSON  │───▶│   (Qdrant)      │◀───│   • product_search
│   • FAQ.txt     │    │   • 15 bikes    │    │   • faq_search  │
└─────────────────┘    │   • 12 FAQs     │    │   • create_lead │
                       └─────────────────┘    │   • memory      │
                                              └─────────────────┘
```

### Component Architecture

```
bike_sales_agent/
├── 📁 Data/                    # Data sources
│   ├── product_catalog.json    # 15 bikes with specs
│   └── faq.txt                # Customer FAQ knowledge base
├── 📁 src/                     # Main application
│   ├── agent.py               # PydanticAI agent + conversation memory
│   ├── tools.py               # 4 core tools implementation
│   ├── models.py              # Pydantic models for API
│   ├── dependencies.py        # Dependency injection
│   ├── vector_db.py           # Qdrant vector database
│   ├── settings.py            # Environment configuration
│   └── api.py                 # FastAPI REST endpoints
├── .env                       # Environment variables (secure)
├── pyproject.toml            # Dependencies
└── run.py                    # Server startup
```

## ✨ Features

### 🤖 Intelligent Sales Agent
- **Natural Conversations**: Understands customer needs in plain language
- **Context Awareness**: Remembers previous messages in conversation
- **Product Expertise**: Deep knowledge of bike specifications and features
- **Sales Process**: Guides customers from inquiry to lead conversion

### 🔍 Vector-Powered Search
- **Semantic Search**: Finds bikes based on meaning, not just keywords
- **Smart Filtering**: Price, type, and feature-based filtering
- **Relevance Ranking**: Returns most relevant bikes first
- **Fast Performance**: Local Qdrant database for quick responses

### 💾 Conversation Memory
- **Per-User Sessions**: Each `conversation_id` maintains separate history
- **Context Retention**: Remembers budget, preferences, and previous questions
- **Multi-Turn Conversations**: Natural flow across multiple messages
- **Memory Management**: Keeps last 6 messages for optimal context

### 🎯 Interest Detection & Lead Management
- **Automatic Detection**: Identifies purchase signals in customer messages
- **Lead Collection**: Captures name, email, phone when interest confirmed
- **CRM Integration**: Sends leads to external CRM systems
- **Follow-up Ready**: Structured data for sales team follow-up

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv package manager
- OpenAI API key

### Installation

1. **Clone and Setup**
```bash
cd Bike_sales_agent
```

2. **Configure Environment**
```bash
# Edit .env file with your API key
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Install Dependencies**
```bash
uv sync
```

4. **Start Server**
```bash
uv run uvicorn src.api:app --port 8005
```

5. **Test Health**
```bash
curl http://localhost:8005/health
```

### First Conversation

```bash
curl -X POST http://localhost:8005/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, I need a mountain bike under €1500",
    "conversation_id": "customer-001"
  }'
```

## 📡 API Documentation

### Base URL
```
http://localhost:8005
```

### Endpoints

#### 🏥 Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "bike_sales_agent",
  "version": "1.0.0"
}
```

#### 💬 Chat with Agent
```http
POST /chat
```
**Request:**
```json
{
  "message": "I'm looking for a commuter bike under €800",
  "conversation_id": "user-123"
}
```
**Response:**
```json
{
  "response": "Great! I found several excellent commuter bikes under €800...",
  "conversation_id": "user-123",
  "interest_detected": false
}
```

#### 🚴 List All Bikes
```http
GET /bikes
```
**Response:**
```json
{
  "bikes": [
    {
      "id": 1,
      "name": "Urban Cruiser X",
      "brand": "Cube",
      "type": "City Bike",
      "price_eur": 799,
      "intended_use": ["Commuting", "Urban"]
    }
  ]
}
```

#### ❓ Get FAQ
```http
GET /faq
```
**Response:**
```json
{
  "faq": "FAQ – Online Bike Shop\n\n1. Do you offer repair..."
}
```

### Conversation Memory Example

**Message 1:**
```json
{
  "message": "Hi, I need a bike under €1000",
  "conversation_id": "user-456"
}
```

**Message 2:**
```json
{
  "message": "What about mountain bikes?",
  "conversation_id": "user-456"
}
```
*Agent remembers the €1000 budget from Message 1*

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ |
| `LLM_MODEL` | Model name | `gpt-4o-mini` | ❌ |
| `QDRANT_HOST` | Qdrant host | `localhost` | ❌ |
| `QDRANT_PORT` | Qdrant port | `6333` | ❌ |
| `CRM_API_URL` | CRM endpoint | `https://api.example-crm.com` | ❌ |
| `CRM_API_KEY` | CRM API key | - | ❌ |

### Data Sources

#### Bike Catalog (`Data/product_catalog.json`)
```json
{
  "id": 1,
  "name": "Trailblazer 500",
  "brand": "RockRider",
  "type": "Mountain Bike",
  "price_eur": 1499,
  "frame_material": "Aluminum",
  "intended_use": ["Trail", "Off-road", "Downhill"]
}
```

#### FAQ (`Data/faq.txt`)
```
1. Do you offer repair and maintenance services?
Yes, we provide repair and maintenance services...

2. What is the warranty period for new bikes?
All new bikes come with a 2-year warranty...
```

## 🧪 Testing

### Automated Testing
```bash
# Run all component tests
uv run python test_customer_simulation.py

# Test FAQ with real questions
uv run python test_faq_simulation.py
```

### Manual Testing Scenarios

#### 1. Basic Product Search
```json
{
  "message": "I need a mountain bike for trails",
  "conversation_id": "test-1"
}
```

#### 2. Budget-Constrained Search
```json
{
  "message": "Show me city bikes under €600",
  "conversation_id": "test-2"
}
```

#### 3. FAQ Questions
```json
{
  "message": "What's your return policy?",
  "conversation_id": "test-3"
}
```

#### 4. Interest Detection & Lead Collection
```json
{
  "message": "I'm interested in the Urban Cruiser X. My name is John Smith, email john@example.com",
  "conversation_id": "test-4"
}
```

### Expected Results
- ✅ **Product Search**: Returns relevant bikes with specifications
- ✅ **FAQ Search**: Provides accurate answers from knowledge base
- ✅ **Interest Detection**: `interest_detected: true` for purchase signals
- ✅ **Conversation Memory**: Maintains context across messages
- ✅ **Lead Creation**: Captures customer information when interest confirmed

## 🚀 Deployment

### Local Development
```bash
uv run uvicorn src.api:app --port 8005 --reload
```

### Production
```bash
uv run uvicorn src.api:app --host 0.0.0.0 --port 8005
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["uv", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8005"]
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill existing processes
pkill -f uvicorn

# Or use different port
uv run uvicorn src.api:app --port 8006
```

#### Missing API Key
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY

# Set temporarily
export OPENAI_API_KEY=your_key_here
```

#### Vector Database Issues
```bash
# Test vector search
uv run python -c "
from bike_sales_agent.vector_db import vector_db
import asyncio
async def test():
    await vector_db.initialize()
    bikes = await vector_db.search_bikes('mountain bike')
    print(f'Found {len(bikes)} bikes')
asyncio.run(test())
"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uv run uvicorn bike_sales_agent.api:app --port 8005 --log-level debug
```

### Performance Monitoring
- **Response Time**: Typical < 2 seconds for bike search
- **Memory Usage**: ~200MB with vector embeddings loaded
- **Concurrent Users**: Supports multiple conversation sessions

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| **Bike Catalog Size** | 15 bikes indexed |
| **FAQ Knowledge Base** | 12 Q&A pairs |
| **Vector Dimensions** | 384 (sentence-transformers) |
| **Average Response Time** | < 2 seconds |
| **Memory Usage** | ~200MB |
| **Conversation History** | Last 6 messages per user |

## 🤝 Contributing

1. Follow PydanticAI best practices
2. Add tests for new features
3. Update documentation
4. Use type hints throughout
5. Maintain conversation memory compatibility

## 📄 License

MIT License - see LICENSE file for details.

---

**🎯 Ready for Production!** The bike sales agent is fully functional with conversation memory, vector search, and CRM integration. Start the server and begin testing with Postman!