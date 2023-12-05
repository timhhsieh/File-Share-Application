import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import requests
from tkinter import messagebox

def upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        confirmation = messagebox.askokcancel("Confirmation", f"Upload the file '{file_path.split('/')[-1]}'?")
        if confirmation:
            files = {'file': open(file_path, 'rb')}
            response = requests.post('http://localhost:5000/upload', files=files)
            if response.status_code == 200:
                messagebox.showinfo("Success", "File uploaded successfully")
                show_available_files()  # Refresh available files after upload
            else:
                messagebox.showerror("Error", "Failed to upload file")

def show_instructions():
    instructions = (
        "Welcome to the File Sharing Service!\n\n"
        "To upload a file:\n"
        "Click the 'Upload File' button, select the file you want to upload, and it will be sent to the server.\n\n"
        "To download a file:\n"
        "Select the file you would like to download from the dropdown menu, click the 'Download' button, and select your download destination.\n\n"
        "Ensure the server is running before uploading files.\n"
    )
    messagebox.showinfo("Instructions", instructions)

def fetch_available_files():
    response = requests.get('http://localhost:5000/available_files')
    if response.status_code == 200:
        return response.json()
    return []

def fetch_keywords():
    response = requests.get('http://localhost:5000/keywords')
    if response.status_code == 200:
        keywords = response.json()
        # Save fetched keywords to a text file
        with open('keywords.txt', 'w') as file:
            file.write('\n'.join(keywords))
        return keywords
    return []

def download_selected_file():
    selected_file = download_dropdown.get()
    if selected_file:
        response = requests.get(f'http://localhost:5000/download/{selected_file}', stream=True)
        if response.status_code == 200:
            download_path = filedialog.asksaveasfilename(initialfile=selected_file, defaultextension=".txt")
            if download_path:
                with open(download_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                messagebox.showinfo("Download Complete", f"File '{selected_file}' downloaded successfully.")
            else:
                messagebox.showwarning("Download Canceled", "Download canceled by the user.")
        else:
            messagebox.showerror("Download Failed", f"Failed to download '{selected_file}'.")


def show_available_files():
    with open('keywords.txt', 'r') as keyword_file:
        files = keyword_file.read().splitlines()
        download_dropdown['values'] = files

root = tk.Tk()
root.title("File Sharing Service")

welcome_label = tk.Label(root, text="Welcome to the File Sharing Service", font=("Arial", 16))
welcome_label.pack(pady=20)

upload_button = tk.Button(root, text="Upload File", command=upload, width=20)
upload_button.pack()

instructions_button = tk.Button(root, text="How to Use", command=show_instructions, width=20)
instructions_button.pack(pady=10)

download_dropdown = ttk.Combobox(root, width=30)
download_dropdown.pack()

download_button = tk.Button(root, text="Download", command=download_selected_file, width=20)
download_button.pack(pady=10)

show_available_files()

root.mainloop()
