"""
Run Server

Start the host-authoritative Custom UNO Online server.
"""

import sys


def main():
    try:
        from network.server import Server
    except ImportError as error:
        print("Import error:", error)
        print("Please check your folder structure and __init__.py files.")
        sys.exit(1)

    host = "0.0.0.0"
    port = 5000

    server = Server(host=host, port=port)

    print(f"Starting Custom UNO Online server on {host}:{port}")

    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped manually.")
    except Exception as error:
        print("Server error:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()