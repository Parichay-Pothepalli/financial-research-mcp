# AGENTS.md

Welcome to the **Financial Datasets MCP Server**!

This server provides financial data tools for accessing stock prices, financial statements, crypto prices, and SEC filings through the Model Context Protocol.

## What's Included

- **FastMCP Server** with Smithery session-scoped configuration support
- **Financial Tools** for accessing various financial data:
  - Income statements, balance sheets, and cash flow statements
  - Current and historical stock prices
  - Company news and SEC filings
  - Cryptocurrency prices and information
- **Development Workflow** (`uv run dev` for local testing, `uv run playground` for interactive testing)
- **Deployment Ready** configuration for the Smithery platform
- **Session Management** via `@smithery.server()` decorator with API key configuration

## Quick Start Commands

```bash
# Run development server (streamable HTTP on port 8081)
uv run dev

# Run production server (optimized for deployment)
uv run start

# Test with interactive playground
uv run playground
```

## Development Workflow

Based on the [Model Context Protocol architecture](https://modelcontextprotocol.io/docs/learn/architecture.md), this MCP server provides financial data tools:

### Financial Tools Examples

```python
@server.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
    ctx: Context = None,
) -> str:
    """Get income statements for a company."""
    # Implementation details...
    return json.dumps(income_statements, indent=2)

@server.tool()
async def get_current_stock_price(ticker: str, ctx: Context = None) -> str:
    """Get the current / latest price of a company."""
    # Implementation details...
    return json.dumps(snapshot, indent=2)
```

### API Key Configuration

The server accepts an API key through session configuration:

```python
class ConfigSchema(BaseModel):
    api_key: str = Field("", description="Your Financial Datasets API key (optional)")
    pirate_mode: bool = Field(False, description="Speak like a pirate (for fun)")

@smithery.server(config_schema=ConfigSchema)
def create_server():
    # Server implementation...
```

### Project Structure

```
financial-datasets-mcp/
├── pyproject.toml         # Project config with [tool.smithery] section
├── smithery.yaml          # Runtime specification (runtime: python)
├── src/
│   └── hello_server/      # Server module (consider renaming)
│       ├── __init__.py
│       └── server.py      # Main server implementation
└── README.md
```

## Testing Your Server

### Method 1: Smithery Playground
```bash
uv run playground
```
This opens the Smithery Playground in your browser with your local server tunneled through ngrok.

### Method 2: Direct MCP Protocol Testing
```bash
# Start development server (with optional reload)
uv run dev
uv run dev --reload       # Auto-reload on code changes
```

## Deployment

### Local Deployment
```bash
# Python server deployment prep
uv build                   # Creates wheel in dist/
git add . && git commit -m "Deploy ready"
git push origin main
```

### Production Deployment
1. Push code to GitHub repository
2. Deploy via [smithery.ai/new](https://smithery.ai/new)
3. Smithery handles containerization and hosting

## Resources

- **Documentation**: [smithery.ai/docs](https://smithery.ai/docs)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Python Quickstart**: [smithery.ai/docs/getting_started/quickstart_build_python.md](https://smithery.ai/docs/getting_started/quickstart_build_python.md)
- **GitHub**: [github.com/smithery-ai/sdk](https://github.com/smithery-ai/sdk)
- **Registry**: [smithery.ai](https://smithery.ai) for discovering and deploying MCP servers

## Community & Support

- **Discord**: Join our community for help and discussions: [discord.gg/Afd38S5p9A](https://discord.gg/Afd38S5p9A)
- **Bug Reports**: Found an issue? Report it on GitHub: [github.com/smithery-ai/sdk/issues](https://github.com/smithery-ai/sdk/issues)
- **Feature Requests**: Suggest new features on our GitHub discussions: [github.com/smithery-ai/sdk/discussions](https://github.com/smithery-ai/sdk/discussions)