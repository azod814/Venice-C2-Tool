import http.server
import socketserver
import os
import sys

# --- Colors for Output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PORT = 8000

# --- Main Logic ---
print(f"{GREEN}[+] Starting Payload Server...{NC}")

# Ensure the script runs from the correct directory
# Get the directory where the script itself is located
script_dir = os.path.dirname(os.path.realpath(__file__))
# Define the path to the 'payloads' directory
payloads_dir = os.path.join(script_dir, 'payloads')

# Check if the 'payloads' directory actually exists
if not os.path.isdir(payloads_dir):
    print(f"{RED}[-] ERROR: 'payloads' directory not found!{NC}")
    print(f"{RED}[-] Please make sure you are running this from the main project folder and the 'payloads' folder exists.{NC}")
    sys.exit(1) # Exit the script with an error code

try:
    # Change the current directory to the 'payloads' directory
    os.chdir(payloads_dir)
    print(f"{GREEN}[+] Serving payloads from: {payloads_dir}{NC}")
    print(f"{GREEN}[+] Server started on http://localhost:{PORT}{NC}")
    print(f"{BLUE}[i] Press CTRL+C to stop the server.{NC}")

    # Create a simple request handler
    Handler = http.server.SimpleHTTPRequestHandler

    # Start the TCP server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

except KeyboardInterrupt:
    print("\n[!] Server stopped by user.")
    sys.exit(0)
except OSError as e:
    print(f"{RED}[-] Error: {e}{NC}")
    print(f"{RED}[-] Is port {PORT} already in use? Try 'sudo netstat -tulpn | grep :{PORT}'{NC}")
    sys.exit(1)
