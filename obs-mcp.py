#!/usr/bin/env python3

import asyncio
import os
import mcp

# Import all our modules
from obs_mcp.client import obs_client
from obs_mcp import general
from obs_mcp import scenes
from obs_mcp import sources
from obs_mcp import scene_items
from obs_mcp import streaming
from obs_mcp import transitions

# MCP server setup
server = mcp.Server("obs_mcp", description="OBS Studio MCP Server")

# Import all tools from our modules
for module in [general, scenes, sources, scene_items, streaming, transitions]:
    # Register all tools from each module
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if hasattr(attr, "__mcp_tool__") and attr.__mcp_tool__:
            # This is an MCP tool, register it directly on our server
            server.add_tool(attr)

async def startup():
    """Connect to OBS WebSocket server on startup"""
    try:
        await obs_client.connect()
        print("Connected to OBS WebSocket server")
    except Exception as e:
        print(f"Failed to connect to OBS WebSocket server: {e}")
        print("Make sure OBS is running and WebSocket server is enabled")
        print("Will try to connect when the first request is made")

async def shutdown():
    """Close connection to OBS WebSocket server on shutdown"""
    await obs_client.close()
    print("Disconnected from OBS WebSocket server")

if __name__ == "__main__":
    # Set startup and shutdown handlers
    server.on_startup(startup)
    server.on_shutdown(shutdown)
    
    # Start the server
    server.serve()