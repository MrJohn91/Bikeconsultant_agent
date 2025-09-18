#!/usr/bin/env python3
"""Simple server runner."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("bike_sales_agent.api:app", host="0.0.0.0", port=8002, reload=True)