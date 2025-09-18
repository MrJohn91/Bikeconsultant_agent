"""FastAPI application for bike sales agent."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse
from .agent import chat_with_sales_agent, detect_interest
from .dependencies import SalesAgentDependencies

app = FastAPI(
    title="Bike Sales Agent API",
    description="PydanticAI-powered bike sales consultant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "bike_sales_agent", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the bike sales agent."""
    try:
        # Check if dependencies are available
        deps = SalesAgentDependencies()
        if not deps.bike_catalog:
            raise HTTPException(status_code=503, detail="Service dependencies not initialized")
        
        # Run the agent
        response = await chat_with_sales_agent(request.message, request.conversation_id)
        
        # Detect interest
        interest_detected = detect_interest(request.message)
        
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id,
            interest_detected=interest_detected
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.get("/bikes")
async def list_bikes():
    """List all available bikes."""
    deps = SalesAgentDependencies()
    return {"bikes": deps.bike_catalog}


@app.get("/faq")
async def get_faq():
    """Get FAQ information."""
    deps = SalesAgentDependencies()
    return {"faq": deps.faq_data}