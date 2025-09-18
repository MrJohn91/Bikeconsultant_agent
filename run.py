#!/usr/bin/env python3
"""Simple server runner."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8005, reload=True)