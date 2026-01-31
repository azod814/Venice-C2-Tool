#!/bin/bash

# --- Colors for Output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# --- Helper Functions ---
print_status() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[-]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# --- Main Installation Logic ---
clear
echo -e "${GREEN}"
cat << "EOF"
 _   _            _    _      _   _               _     
| | | |          | |  | |    | | | |             | |    
| |_| | __ _  ___| | _| | ___| |_| |     ___   __| | ___
|  _  |/ _` |/ __| |/ / |/ _ \ __| |    / _ \ / _` |/ _ \
| | | | (_| | (__|   <| |  __/ |_| |_  | (_) | (_| |  __/
\_| |_/\__,_|\___|_|\_\_|\___|\__|_(_)  \___/ \__,_|\___|
                                                      
                --- C2 Payload Builder ---
EOF
echo -e "${NC}"

print_status "Starting installation process..."
sleep 2

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root!"
   print_error "Please run it as a regular user."
   exit 1
fi

# Update package lists
print_status "Updating package lists..."
sudo apt update > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Package lists updated successfully."
else
    print_error "Failed to update package lists. Check your internet connection."
    exit 1
fi

# Install Python3 and Tkinter
print_status "Installing Python3 and Tkinter..."
sudo apt install -y python3 python3-tk > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Python3 and Tkinter installed."
else
    print_error "Failed to install Python3/Tkinter."
    exit 1
fi

# Install Python dependencies
print_status "Installing Python dependencies from requirements.txt..."
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Python dependencies installed."
else
    print_warning "pip3 install failed. This might be okay if requirements.txt is empty."
fi

# Create the simple HTTP server script
print_status "Creating helper script for payload hosting..."
cat > serve_payloads.py << 'EOF'
import http.server
import socketserver
import os
import sys

# --- Colors for Output ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

PORT = 8000
# Ensure the script runs from the payloads directory
script_dir = os.path.dirname(os.path.realpath(__file__))
payloads_dir = os.path.join(script_dir, 'payloads')

if not os.path.isdir(payloads_dir):
    print(f"Error: 'payloads' directory not found at {payloads_dir}")
    sys.exit(1)

try:
    os.chdir(payloads_dir)
    print(f"{GREEN}[+]{NC} Serving payloads from: {payloads_dir}")
    print(f"{GREEN}[+]{NC} Server started on http://localhost:{PORT}")
    print(f"{BLUE}[i]{NC} Press CTRL+C to stop the server.")

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[!] Server stopped by user.")
    sys.exit(0)
except OSError as e:
    print(f"Error: {e}. Is port {PORT} already in use?")
    sys.exit(1)
EOF

# Make the scripts executable
print_status "Making scripts executable..."
chmod +x serve_payloads.py
chmod +x listener.py
chmod +x builder.py

# Final message
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Installation Complete! ✅${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}To start the tool, follow these steps:${NC}"
echo ""
echo -e "${YELLOW}1. Start the C2 Listener (in a new terminal):${NC}"
echo -e "   ${GREEN}python3 listener.py -i <YOUR_KALI_IP> -p <PORT>${NC}"
echo -e "   Example: python3 listener.py -i 192.168.1.10 -p 4444"
echo ""
echo -e "${YELLOW}2. Start the Payload Web Server (in another new terminal):${NC}"
echo -e "   ${GREEN}python3 serve_payloads.py${NC}"
echo ""
echo -e "${YELLOW}3. Launch the GUI Builder (in a third terminal):${NC}"
echo -e "   ${GREEN}python3 builder.py${NC}"
echo ""
echo -e "${RED}NOTE: Replace <YOUR_KALI_IP> with your actual IP address.${NC}"
echo -e "${RED}Use 'ifconfig' or 'ip a' to find your IP.${NC}"
echo ""
