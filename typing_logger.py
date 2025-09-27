# typing_logger.py
# Safe: logs keys typed inside this tkinter window only.
# Usage: python typing_logger.py

import tkinter as tk
from datetime import datetime
import os

LOG_FILE = "typing_log.txt"

def log_key(event):
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    if event.char and event.char != '\r':
        key_descr = event.char
    else:
        key_descr = event.keysym
    if key_descr == '\n':
        key_descr = 'Return'
    line = f"{timestamp}\t{key_descr}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        status_var.set(f"Error writing log: {e}")

def clear_log():
    open(LOG_FILE, "w", encoding="utf-8").close()
    status_var.set("Log cleared.")

def show_last_lines(n=20):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    last = lines[-n:]
    preview = "".join(last) if last else "(log is empty)"
    popup = tk.Toplevel(root)
    popup.title("Last lines of log")
    txt = tk.Text(popup, wrap="none", width=80, height=20)
    txt.pack()
    txt.insert("1.0", preview)
    txt.config(state="disabled")

def on_close():
    root.destroy()

root = tk.Tk()
root.title("Safe Typing Logger (in-app only)")
root.geometry("700x450")

label = tk.Label(root, text="Type below. Only keys pressed inside this window are logged.", pady=10)
label.pack()

text = tk.Text(root, wrap="word", height=18, width=80)
text.pack(padx=10, pady=5)
text.focus_set()

# Bind keypress events on the Text widget only
text.bind("<Key>", log_key)

# Controls frame
frame = tk.Frame(root)
frame.pack(pady=8)

clear_btn = tk.Button(frame, text="Clear Log File", command=clear_log)
clear_btn.grid(row=0, column=0, padx=6)

open_btn = tk.Button(frame, text="Show Last 20 Lines", command=lambda: show_last_lines(20))
open_btn.grid(row=0, column=1, padx=6)

status_var = tk.StringVar(value=f"Logging to {os.path.abspath(LOG_FILE)}")
status_label = tk.Label(root, textvariable=status_var, fg="green")
status_label.pack(pady=6)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
