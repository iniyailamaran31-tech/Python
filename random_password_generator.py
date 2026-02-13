import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")
        return

    char_pool = ""
    password = []

    exclude = exclude_entry.get()

    if lower_var.get():
        chars = ''.join(c for c in string.ascii_lowercase if c not in exclude)
        char_pool += chars
        password.append(random.choice(chars))

    if upper_var.get():
        chars = ''.join(c for c in string.ascii_uppercase if c not in exclude)
        char_pool += chars
        password.append(random.choice(chars))

    if digit_var.get():
        chars = ''.join(c for c in string.digits if c not in exclude)
        char_pool += chars
        password.append(random.choice(chars))

    if symbol_var.get():
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?/|"
        chars = ''.join(c for c in symbols if c not in exclude)
        char_pool += chars
        password.append(random.choice(chars))

    if not char_pool:
        messagebox.showerror("Error", "Select at least one character type")
        return

    while len(password) < length:
        password.append(random.choice(char_pool))

    random.shuffle(password)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, ''.join(password))

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI Setup
root = tk.Tk()
root.title("Advanced Random Password Generator")
root.geometry("420x450")
root.resizable(False, False)

tk.Label(root, text="Password Length").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.pack()

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Lowercase Letters", variable=lower_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Uppercase Letters", variable=upper_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Numbers", variable=digit_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Symbols", variable=symbol_var).pack(anchor='w', padx=20)

tk.Label(root, text="Exclude Characters (optional)").pack(pady=5)
exclude_entry = tk.Entry(root)
exclude_entry.pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=15)

password_entry = tk.Entry(root, font=("Arial", 14), justify="center")
password_entry.pack(pady=10)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack()

root.mainloop()
