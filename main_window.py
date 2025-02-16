import tkinter as tk
from tkinter import ttk
import logging
from PIL import Image, ImageDraw

class MainWindow:
    def __init__(self, clipboard_monitor):
        self.root = tk.Tk()
        self.root.title("Secure Clipboard")
        self.clipboard_monitor = clipboard_monitor
        self.setup_window()
        self.create_widgets()
        logging.info("Main window initialized")

    def setup_window(self):
        # Set window size and position
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
        self.root.resizable(False, False)
        
        # Configure styles
        style = ttk.Style()
        style.configure("Mode.TButton", padding=10, font=('Segoe UI', 10, 'bold'))
        style.configure("Status.TLabel", font=('Segoe UI', 9))
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root, padding="20 20 20 10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame,
            text="Secure Clipboard",
            font=('Segoe UI', 16, 'bold')
        ).pack()
        
        # Mode selection
        mode_frame = ttk.LabelFrame(self.root, text="Encryption Mode", padding="20")
        mode_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.mode_var = tk.StringVar(value="auto")
        
        ttk.Radiobutton(
            mode_frame,
            text="Auto (Encrypt outgoing, Decrypt incoming)",
            variable=self.mode_var,
            value="auto",
            command=self.update_mode
        ).pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(
            mode_frame,
            text="Force Decrypt Mode",
            variable=self.mode_var,
            value="decrypt",
            command=self.update_mode
        ).pack(anchor=tk.W, pady=5)
        
        # Status
        status_frame = ttk.LabelFrame(self.root, text="Status", padding="20")
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Monitoring clipboard...",
            style="Status.TLabel"
        )
        self.status_label.pack(anchor=tk.W)
        
        # Actions
        action_frame = ttk.Frame(self.root, padding="20")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(
            action_frame,
            text="Generate New Key",
            command=self.generate_new_key,
            style="Mode.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Hide Window",
            command=self.hide_window,
            style="Mode.TButton"
        ).pack(side=tk.RIGHT, padx=5)

    def update_mode(self):
        mode = self.mode_var.get()
        if mode == "decrypt":
            self.clipboard_monitor.force_decrypt = True
            self.status_label.config(text="Force Decrypt Mode: ON")
        else:
            self.clipboard_monitor.force_decrypt = False
            self.status_label.config(text="Auto Mode: Monitoring clipboard...")

    def generate_new_key(self):
        self.clipboard_monitor.key_manager.generate_new_key()
        self.status_label.config(text="New encryption key generated")

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def run(self):
        self.root.mainloop()
