#!/usr/bin/env python3
"""Start the bike sales agent server."""

import uvicorn
from bike_sales_agent.settings import settings

if __name__ == "__main__":
    print("🚀 Starting Bike Sales Agent Server...")
    print(f"📡 Server will start on http://localhost:8002")
    print(f"🔑 Using model: {settings.llm_model}")
    print(f"📊 API Key: {'✅ Loaded' if settings.openai_api_key else '❌ Missing'}")
    print()
    
    uvicorn.run(
        "bike_sales_agent.api:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )