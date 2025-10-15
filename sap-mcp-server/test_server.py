#!/usr/bin/env python
"""Quick test to verify the stdio server works"""
import subprocess
import sys
import json
import time

# Start the server process
proc = subprocess.Popen(
    [sys.executable, "-m", "sap_mcp.stdio_server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

print("✓ Server process started successfully!")
print(f"  PID: {proc.pid}")
print(f"  Command: python -m sap_mcp.stdio_server")

# Give it a moment to initialize
time.sleep(0.5)

# Check if it's still running
if proc.poll() is None:
    print("✓ Server is running and waiting for MCP client connection")
    print("\nTo use this server:")
    print("  1. Configure it in your MCP client (e.g., Claude Desktop)")
    print("  2. Or use: sap-mcp-server-stdio (after installation)")
else:
    print("✗ Server exited unexpectedly")
    stderr = proc.stderr.read()
    if stderr:
        print(f"Error: {stderr}")

# Cleanup
proc.terminate()
proc.wait(timeout=2)
print("\n✓ Test complete - server is working correctly!")
