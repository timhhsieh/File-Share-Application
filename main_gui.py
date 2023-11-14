import tkinter as tk
from tkinter import filedialog
import requests

def upload():
    file_path = filedialog.askopenfilename()
    files = {'file': open(file_path, 'rb')}
    response = requests.post('http://localhost:5000/upload', files=files)
    print(response.text)

root = tk.Tk()
root.title("File Uploader")

upload_button = tk.Button(root, text="Upload File", command=upload)
upload_button.pack()

root.mainloop()
