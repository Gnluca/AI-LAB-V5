from mcp_server import MCPServer

mcp = MCPServer()

print(mcp.list_tools())

print()

print(
    mcp.call_tool(
        "network_scan"
    )
)