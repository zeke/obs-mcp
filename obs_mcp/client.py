#!/usr/bin/env python3

import os
import json
import asyncio
import websockets
from typing import Any, Dict, List, Optional, Union

OBS_WS_URL = "ws://localhost:4455"
OBS_WS_PASSWORD = os.environ.get("OBS_WS_PASSWORD", "")

class OBSWebSocketClient:
    def __init__(self, url: str = OBS_WS_URL, password: str = OBS_WS_PASSWORD):
        self.url = url
        self.password = password
        self.ws = None
        self.message_id = 0
        self.authenticated = False
        self.responses = {}
        self.lock = asyncio.Lock()

    async def connect(self):
        """Connect to OBS WebSocket server"""
        if self.ws:
            return
        
        try:
            self.ws = await websockets.connect(self.url)
            await self._authenticate()
        except Exception as e:
            raise Exception(f"Failed to connect to OBS WebSocket server: {e}")

    async def _authenticate(self):
        """Authenticate with OBS WebSocket server"""
        # Receive hello message first
        hello = await self.ws.recv()
        hello_data = json.loads(hello)
        
        if hello_data["op"] != 0:  # Hello op code
            raise Exception("Did not receive Hello message from OBS WebSocket server")
        
        auth_data = {
            "op": 1,  # Identify op code
            "d": {
                "rpcVersion": 1,
                "authentication": self.password,
                "eventSubscriptions": 0  # We don't need events for now
            }
        }
        
        await self.ws.send(json.dumps(auth_data))
        response = await self.ws.recv()
        response_data = json.loads(response)
        
        if response_data["op"] != 2:  # Identified op code
            raise Exception("Authentication failed")
        
        self.authenticated = True
        # Start the response handler
        asyncio.create_task(self._response_handler())

    async def _response_handler(self):
        """Handle incoming messages from OBS WebSocket server"""
        while self.ws and not self.ws.closed:
            try:
                message = await self.ws.recv()
                data = json.loads(message)
                
                # Handle request responses
                if data["op"] == 7:  # RequestResponse op code
                    request_id = data["d"]["requestId"]
                    async with self.lock:
                        if request_id in self.responses:
                            self.responses[request_id] = data["d"]
                
                # We're not handling events for now
            except Exception as e:
                print(f"Error in response handler: {e}")
                break

    async def send_request(self, request_type: str, request_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a request to OBS WebSocket server and wait for response"""
        if not self.ws or not self.authenticated:
            await self.connect()
        
        request_id = str(self.message_id)
        self.message_id += 1
        
        payload = {
            "op": 6,  # Request op code
            "d": {
                "requestType": request_type,
                "requestId": request_id
            }
        }
        
        if request_data:
            payload["d"]["requestData"] = request_data
        
        # Register this request ID before sending
        async with self.lock:
            self.responses[request_id] = None
        
        await self.ws.send(json.dumps(payload))
        
        # Wait for response with timeout
        for _ in range(50):  # 5 seconds timeout
            async with self.lock:
                response = self.responses.get(request_id)
                if response is not None:
                    del self.responses[request_id]
                    if "requestStatus" in response and not response["requestStatus"]["result"]:
                        error = response["requestStatus"].get("comment", "Unknown error")
                        raise Exception(f"OBS WebSocket request failed: {error}")
                    return response.get("responseData", {})
            await asyncio.sleep(0.1)
        
        raise Exception("Timeout waiting for OBS WebSocket response")

    async def close(self):
        """Close the connection to OBS WebSocket server"""
        if self.ws:
            await self.ws.close()
            self.ws = None
            self.authenticated = False

# Create a singleton client
obs_client = OBSWebSocketClient()