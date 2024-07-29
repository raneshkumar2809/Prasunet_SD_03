import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import re

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()
        self.create_gui()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def validate_phone(self, phone):
        if re.match(r'^[\d+]+$', phone):
            return True
        return False

    def contact_exists(self, name, phone, email):
        for contact in self.contacts:
            if contact['name'] == name or contact['phone'] == phone or contact['email'] == email:
                return True
        return False

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Input", "Enter phone number:")
        if phone and not self.validate_phone(phone):
            messagebox.showwarning("Warning", "Invalid phone number. Only + and digits are allowed.")
            return
        email = simpledialog.askstring("Input", "Enter email:")

        if not phone and not email:
            messagebox.showwarning("Warning", "You must provide either a phone number or an email address.")
            return

        if self.contact_exists(name, phone, email):
            messagebox.showwarning("Warning", "Contact already exists.")
            return

        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save_contacts()
        self.refresh_contact_list()
        messagebox.showinfo("Success", "Contact added successfully!")

    def edit_contact(self):
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No contact selected.")
            return
        idx = self.contact_tree.index(selected_item[0])
        contact = self.contacts[idx]
        new_name = simpledialog.askstring("Input", f"Enter new name ({contact['name']}):") or contact['name']
        new_phone = simpledialog.askstring("Input", f"Enter new phone number ({contact['phone']}):") or contact['phone']
        if new_phone and not self.validate_phone(new_phone):
            messagebox.showwarning("Warning", "Invalid phone number. Only + and digits are allowed.")
            return
        new_email = simpledialog.askstring("Input", f"Enter new email ({contact['email']}):") or contact['email']
        self.contacts[idx] = {"name": new_name, "phone": new_phone, "email": new_email}
        self.save_contacts()
        self.refresh_contact_list()
        messagebox.showinfo("Success", "Contact updated successfully!")

    def delete_contact(self):
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No contact selected.")
            return
        idx = self.contact_tree.index(selected_item[0])
        del self.contacts[idx]
        self.save_contacts()
        self.refresh_contact_list()
        messagebox.showinfo("Success", "Contact deleted successfully!")

    def refresh_contact_list(self):
        for i in self.contact_tree.get_children():
            self.contact_tree.delete(i)
        for contact in self.contacts:
            self.contact_tree.insert("", tk.END, values=(contact['name'], contact['phone'], contact['email']))

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Contact Manager")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')

        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(pady=20)

        self.contact_tree = ttk.Treeview(frame, columns=("Name", "Phone", "Email"), show='headings')
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone", text="Mobile Number")
        self.contact_tree.heading("Email", text="Email ID")
        self.contact_tree.column("Name", anchor=tk.W, width=150)
        self.contact_tree.column("Phone", anchor=tk.W, width=150)
        self.contact_tree.column("Email", anchor=tk.W, width=200)
        self.contact_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.contact_tree.yview)
        self.contact_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_contact_list()

        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Contact", command=self.add_contact, bg='#4CAF50', fg='white', padx=20, pady=5)
        add_button.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(button_frame, text="Edit Contact", command=self.edit_contact, bg='#FF9800', fg='white', padx=20, pady=5)
        edit_button.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(button_frame, text="Delete Contact", command=self.delete_contact, bg='#F44336', fg='white', padx=20, pady=5)
        delete_button.pack(side=tk.LEFT, padx=10)

        self.root.mainloop()

if __name__ == "__main__":
    ContactManager()
