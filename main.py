#!/usr/bin/env python3

import sys
import os
import logging
import importlib.util
import importlib.machinery
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Make sure we have the required environment variables
if not os.environ.get("OBS_WS_PASSWORD"):
    print("WARNING: OBS_WS_PASSWORD environment variable is not set.")
    print("You will need to set this to the WebSocket password configured in OBS.")
    print("Example: export OBS_WS_PASSWORD='your_password_here'")

# Run the server
if __name__ == "__main__":
    # This is to make sure the modules import correctly
    import obs_mcp
    
    # Import the server module
    spec = importlib.util.spec_from_file_location("obs_mcp_server", 
                                               Path(__file__).parent / "obs-mcp.py")
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
    
    # Server is already configured to run when imported
    # The last line of obs-mcp.py calls server.serve()