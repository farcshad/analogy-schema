#!/usr/bin/env python3
"""
CLI entry point to launch the local Analogy Schema Graph Explorer.
Usage:
    python3 run_visualizer.py
    python3 run_visualizer.py --port 8080
"""

import sys
import argparse
from pathlib import Path

# Ensure repo root is on sys.path
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from visualizer.server import run_server


def main():
    parser = argparse.ArgumentParser(description="Launch local graph explorer for Analogy Schema induction outputs.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the visualizer server (default: 8000).")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1).")
    args = parser.parse_args()

    run_server(port=args.port, host=args.host)


if __name__ == "__main__":
    main()
