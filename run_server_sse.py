#!/usr/bin/env python3
"""Run the MCP server with SSE (Server-Sent Events) transport."""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mherb_mcp.server import create_server
from mherb_mcp.config import ServerConfig, setup_logging

async def run_sse_server():
    """Run the server with SSE transport."""
    
    # Create configuration for SSE
    config = ServerConfig(
        transport="sse",
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        log_level="INFO",
        database_path="test_data/sample.db",
        metadata_path="resources/metadata.json",
        allow_cors=True  # Enable CORS for browser clients
    )
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    # Create server
    logger.info("Creating MCP server with SSE transport...")
    server = create_server()
    
    # Override config for SSE
    server.config.transport = "sse"
    server.config.host = "0.0.0.0"
    server.config.port = 8000
    server.config.allow_cors = True
    
    logger.info("=" * 60)
    logger.info("Starting MCP Server with SSE Transport")
    logger.info("=" * 60)
    logger.info(f"Server Name: {server.config.server_name}")
    logger.info(f"Transport: SSE (Server-Sent Events)")
    logger.info(f"Host: {server.config.host}")
    logger.info(f"Port: {server.config.port}")
    logger.info(f"Database: {server.config.database_path}")
    logger.info("=" * 60)
    logger.info(f"Server will be accessible at: http://{server.config.host}:{server.config.port}")
    logger.info("SSE endpoint: http://0.0.0.0:8000/sse")
    logger.info("=" * 60)
    logger.info("Press Ctrl+C to stop the server")
    logger.info("")
    
    try:
        # Run the server with SSE transport
        server.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("\n\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.exception("Detailed error:")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(run_sse_server())
    except KeyboardInterrupt:
        print("\nServer shutdown complete")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)