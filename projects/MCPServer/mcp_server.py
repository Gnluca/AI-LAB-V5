import requests

class MCPServer:

    def list_tools(self):

        return [
            {
                "name": "hardware_status",
                "description": "Hardware status of Node41"
            },
            {
                "name": "network_scan",
                "description": "Scan AI LAB nodes"
            },
            {
                "name": "development_status",
                "description": "DevelopmentAgent status"
            }
        ]

    def call_tool(self, tool_name):

        if tool_name == "hardware_status":

            return requests.get(
                "http://127.0.0.1:8000/agent/hardware/status"
            ).json()

        if tool_name == "network_scan":

            return requests.get(
                "http://127.0.0.1:8000/network/scan"
            ).json()

        if tool_name == "development_status":

            return requests.get(
                "http://127.0.0.1:8000/agent/development/status"
            ).json()

        return {
            "error": "tool not found"
        }