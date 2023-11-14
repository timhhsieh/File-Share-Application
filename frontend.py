import tkinter as tk
from tkinter import filedialog
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
            else:
                messagebox.showerror("Error", "Failed to upload file")

def show_instructions():
    instructions = (
        "Welcome to the File Sharing Service!\n\n"
        "To upload a file:\n"
        "Click the 'Upload File' button, select the file you want to upload, and it will be sent to the server.\n\n"
        "Ensure the server is running before uploading files.\n"
    )
    messagebox.showinfo("Instructions", instructions)

root = tk.Tk()
root.title("File Sharing Service")

welcome_label = tk.Label(root, text="Welcome to the File Sharing Service", font=("Arial", 16))
welcome_label.pack(pady=20)

upload_button = tk.Button(root, text="Upload File", command=upload, width=20)
upload_button.pack()

instructions_button = tk.Button(root, text="How to Use", command=show_instructions, width=20)
instructions_button.pack(pady=10)

root.mainloop()
