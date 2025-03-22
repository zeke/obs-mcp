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
pip install obs-mcp
```

## Usage

1. Make sure OBS Studio is running with WebSocket server enabled (Tools > WebSocket Server Settings)
2. Set the WebSocket password in environment variable:

```bash
export OBS_WS_PASSWORD="your_password_here"
```

3. Run the OBS MCP server:

```bash
python -m obs_mcp
```

Or run directly:

```bash
python main.py
```

4. Connect to the MCP server with an MCP client and use the provided tools to control OBS.

## Available Tools

The server provides tools organized by category:

- General tools: Version info, stats, hotkeys
- Scene tools: List scenes, switch scenes, create/remove scenes
- Source tools: Manage sources, filters, screenshots
- Scene item tools: Manage items in scenes (position, visibility, etc.)
- Streaming tools: Start/stop streaming, recording, replay buffer
- Transition tools: Set transitions, durations, trigger transitions

## Development

To set up a development environment:

```bash
pip install -e ".[dev]"
```

Run linting:

```bash
black .
ruff check .
```

## Requirements

- Python 3.10+
- OBS Studio 31+ with WebSocket server enabled
- MCP client

## License

See the [LICENSE](LICENSE) file for details.