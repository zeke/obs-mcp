# OBS MCP Server

An MCP server for OBS Studio that provides tools to control OBS via the OBS WebSocket protocol.

## Features

- Connect to OBS WebSocket server
- Control OBS via MCP tools
- Provides tools for:
  - General operations
  - Scene management
  - Source control
  - Scene item manipulation
  - Streaming and recording
  - Transitions

## Installation

```bash
npm install
npm run build
```

## Usage

1. Make sure OBS Studio is running with WebSocket server enabled (Tools > WebSocket Server Settings)
2. Set the WebSocket password in environment variable (if needed):

```bash
export OBS_WEBSOCKET_PASSWORD="your_password_here"
```

3. Run the OBS MCP server:

```bash
npm start
```

4. Connect to the MCP server with an MCP client and use the provided tools to control OBS.

## Available Tools

The server provides tools organized by category:

- General tools: Version info, stats, hotkeys, studio mode
- Scene tools: List scenes, switch scenes, create/remove scenes
- Source tools: Manage sources, settings, audio levels, mute/unmute
- Scene item tools: Manage items in scenes (position, visibility, etc.)
- Streaming tools: Start/stop streaming, recording, virtual camera
- Transition tools: Set transitions, durations, trigger transitions

## Environment Variables

- `OBS_WEBSOCKET_URL`: WebSocket URL (default: ws://localhost:4455)
- `OBS_WEBSOCKET_PASSWORD`: Password for authenticating with OBS WebSocket (if required)

## Requirements

- Node.js 16+
- OBS Studio 28+ with WebSocket server enabled
- MCP client

## License

See the [LICENSE](LICENSE) file for details.