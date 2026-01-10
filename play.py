#!/usr/bin/env python3
"""
TicTacToe Memory Challenge - Entry Point
Run this file to start the game!
"""
import subprocess
import webbrowser
import time
import sys
import socket


def find_available_port(start_port=8000, max_attempts=100):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")


def main():
    print("\n" + "=" * 50)
    print("   🧠 TicTacToe Memory Challenge 🧠")
    print("=" * 50)
    print("\nStarting game server...")

    # Find available port
    port = find_available_port()
    url = f"http://127.0.0.1:{port}"

    print(f"Server will run on: {url}")
    print("\nPress Ctrl+C to stop the server\n")

    # Open browser after a short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(url)

    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Start uvicorn server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "127.0.0.1",
            "--port", str(port),
        ], check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped. Thanks for playing! 🎮")
    except subprocess.CalledProcessError as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
