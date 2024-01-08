import tkinter as tk
from tkinter import ttk, filedialog
from bson.binary import Binary
from pymongo import MongoClient
from dotenv import load_dotenv
import os


class MongoDBUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manager")

        # Load environment variables from .env file
        load_dotenv()

        # MongoDB connection
        username = os.getenv("MONGO_USERNAME", '')
        password = os.getenv("MONGO_PASSWORD", '')
        hostname = os.getenv("MONGO_HOSTNAME", 'localhost')
        port = int(os.getenv("MONGO_PORT", 27017))
        database = os.getenv("MONGO_DATABASE", 'face_recognition')
        collection = os.getenv("MONGO_COLLECTION", 'faces')

        if username and password:
            uri = f"mongodb://{username}:{password}@{hostname}:{port}/{database}"
        else:
            uri = f"mongodb://{hostname}:{port}/{database}"

        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection = self.db[collection]

        # Entry widgets
        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0, pady=(10, 0))
        self.name_entry = tk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, pady=(10, 0))

        self.fname_label = tk.Label(master, text="Family Name:")
        self.fname_label.grid(row=1, column=0, pady=(0, 0))
        self.fname_entry = tk.Entry(master, width=30)
        self.fname_entry.grid(row=1, column=1, pady=(0, 0))

        self.age_label = tk.Label(master, text="Age:")
        self.age_label.grid(row=2, column=0, pady=(0, 0))
        self.age_entry = tk.Entry(master, width=30)
        self.age_entry.grid(row=2, column=1, pady=(0, 0))

        self.image_path_label = tk.Label(master, text="Image Path:")
        self.image_path_label.grid(row=3, column=0, pady=(0, 0))
        self.image_path_entry = tk.Entry(master, width=30, state=tk.DISABLED)
        self.image_path_entry.grid(row=3, column=1, pady=(0, 0))

        self.browse_button = tk.Button(master, text="Browse Image", command=self.browse_image)
        self.browse_button.grid(row=4, column=0, columnspan=2, pady=(5, 0))

        # Insert Button
        self.insert_button = tk.Button(master, text="Insert", command=self.insert_data)
        self.insert_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Separator line
        separator = ttk.Separator(master, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Listbox to display data
        self.listbox = tk.Listbox(master, width=45, selectmode=tk.SINGLE)
        self.listbox.grid(row=8, column=0, columnspan=2, padx=(10, 10), pady=(10, 0))
        self.populate_listbox()

        # Delete button
        self.delete_button = tk.Button(master, text="Delete Selected", command=self.delete_selected)
        self.delete_button.grid(row=9, column=0, columnspan=2, pady=(10, 0))

        # Separator line
        separator = ttk.Separator(master, orient="horizontal")
        separator.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # Text widget for logging
        self.log_text = tk.Text(master, width=45, height=10, wrap=tk.WORD)
        self.log_text.grid(row=11, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.log_text.config(state=tk.DISABLED)

        # Bind Enter key to insert_data method
        self.name_entry.bind("<Return>", lambda event: self.insert_data())
        self.fname_entry.bind("<Return>", lambda event: self.insert_data())
        self.age_entry.bind("<Return>", lambda event: self.insert_data())

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)  # Scroll to the bottom

    def populate_listbox(self):
        # Clear existing items
        self.listbox.delete(0, tk.END)

        # Fetch data from MongoDB and populate listbox
        for document in self.collection.find():
            self.listbox.insert(tk.END, f"{document['name']} - {document['fname']}")

    def browse_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path_entry.config(state=tk.NORMAL)
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)
            self.image_path_entry.config(state=tk.DISABLED)

    def insert_data(self):
        name = self.name_entry.get()
        fname = self.fname_entry.get()
        age = self.age_entry.get()
        image_path = self.image_path_entry.get()

        if name and fname and age and image_path:
            with open(image_path, 'rb') as file:
                image_binary = file.read()

            data = {
                'name': name,
                'fname': fname,
                'age': int(age),
                'image_binary': Binary(image_binary),
            }

            self.collection.insert_one(data)
            log_message = f"Data inserted: {data['name']} {data['fname']}"
            self.log(log_message)
            self.populate_listbox()  # Refresh listbox after insertion
            self.name_entry.delete(0, tk.END)
            self.fname_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.image_path_entry.config(state=tk.NORMAL)
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.config(state=tk.DISABLED)
        else:
            log_message = "Please enter all required information."
            self.log(log_message)

    def delete_selected(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index[0])
            name, fname = selected_item.split(" - ")
            result = self.collection.delete_one({'name': name, 'fname': fname})
            if result.deleted_count > 0:
                log_message = f"Data deleted: {name} {fname}"
                self.log(log_message)
                self.populate_listbox()
            else:
                log_message = f"Data not found: {name} {fname}"
                self.log(log_message)
        else:
            log_message = "Please select an item to delete."
            self.log(log_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBUI(root)
    root.mainloop()
