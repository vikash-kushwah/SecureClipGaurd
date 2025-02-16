import tkinter as tk
from tkinter import ttk
import logging
from PIL import Image, ImageDraw
import sys

class MainWindow:
    def __init__(self, clipboard_monitor=None):
        self.root = tk.Tk()
        self.root.title("Secure Clipboard")
        self.clipboard_monitor = clipboard_monitor
        self.setup_window()
        self.create_widgets()
        logging.info("Main window initialized")
        self.update_timer_id = None
        # Don't start updates until clipboard monitor is set
        if clipboard_monitor:
            self._start_status_updates()

    def set_clipboard_monitor(self, monitor):
        """Set the clipboard monitor and start status updates"""
        self.clipboard_monitor = monitor
        self._start_status_updates()

    def setup_window(self):
        # Set window size and position
        window_width = 400
        window_height = 450  # Increased height for decryption display
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Keep window on top

        # Configure styles with modern look
        style = ttk.Style()
        style.configure("Mode.TButton", padding=10, font=('Segoe UI', 10, 'bold'))
        style.configure("Status.TLabel", font=('Segoe UI', 9))
        style.configure("Header.TLabel", font=('Segoe UI', 16, 'bold'))
        style.configure("Active.TLabel", foreground='green', font=('Segoe UI', 9, 'bold'))
        style.configure("Inactive.TLabel", foreground='gray', font=('Segoe UI', 9))
        style.configure("Decrypted.TLabel", font=('Segoe UI', 10), foreground='#1565C0')

    def create_widgets(self):
        # Header with status indicator
        header_frame = ttk.Frame(self.root, padding="20 20 20 10")
        header_frame.pack(fill=tk.X)

        header_label = ttk.Label(
            header_frame,
            text="🔐 Secure Clipboard",
            style="Header.TLabel"
        )
        header_label.pack(side=tk.LEFT)

        self.status_dot = ttk.Label(
            header_frame,
            text="●",
            style="Active.TLabel"
        )
        self.status_dot.pack(side=tk.RIGHT)

        # Mode selection with clear visual feedback
        mode_frame = ttk.LabelFrame(self.root, text="Encryption Mode", padding="20")
        mode_frame.pack(fill=tk.X, padx=20, pady=10)

        self.mode_var = tk.StringVar(value="auto")

        # Auto mode with icon
        ttk.Radiobutton(
            mode_frame,
            text="🔄 Auto (Encrypt outgoing, Decrypt incoming)",
            variable=self.mode_var,
            value="auto",
            command=self.update_mode
        ).pack(anchor=tk.W, pady=5)

        # Decrypt mode with icon
        ttk.Radiobutton(
            mode_frame,
            text="🔓 Force Decrypt Mode (10s timeout)",
            variable=self.mode_var,
            value="decrypt",
            command=self.update_mode
        ).pack(anchor=tk.W, pady=5)

        # Live decryption display
        decrypt_frame = ttk.LabelFrame(self.root, text="Live Decryption", padding="20")
        decrypt_frame.pack(fill=tk.X, padx=20, pady=10)

        self.decrypt_label = ttk.Label(
            decrypt_frame,
            text="Decrypted text will appear here",
            style="Decrypted.TLabel",
            wraplength=320
        )
        self.decrypt_label.pack(anchor=tk.W, pady=5)

        # Status with more detailed information
        status_frame = ttk.LabelFrame(self.root, text="Current Status", padding="20")
        status_frame.pack(fill=tk.X, padx=20, pady=10)

        self.status_label = ttk.Label(
            status_frame,
            text="🟢 Monitoring clipboard...",
            style="Status.TLabel"
        )
        self.status_label.pack(anchor=tk.W, pady=5)

        self.mode_label = ttk.Label(
            status_frame,
            text="Mode: Auto (Encrypt & Decrypt)",
            style="Status.TLabel"
        )
        self.mode_label.pack(anchor=tk.W)

        # Only show shortcuts frame on Windows
        if sys.platform == 'win32':
            shortcut_frame = ttk.LabelFrame(self.root, text="Additional Options", padding="20")
            shortcut_frame.pack(fill=tk.X, padx=20, pady=10)

            self.shortcut_label = ttk.Label(
                shortcut_frame,
                text="Right-click the system tray icon for more options",
                style="Status.TLabel",
                wraplength=320
            )
            self.shortcut_label.pack(anchor=tk.W, pady=5)

        # Actions with improved visual feedback
        action_frame = ttk.Frame(self.root, padding="20")
        action_frame.pack(fill=tk.X)

        ttk.Button(
            action_frame,
            text="🔑 Generate New Key",
            command=self.generate_new_key,
            style="Mode.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="⚙️ Hide Window",
            command=self.hide_window,
            style="Mode.TButton"
        ).pack(side=tk.RIGHT, padx=5)

    def update_decrypt_display(self, text):
        """Update the live decryption display"""
        if text:
            self.decrypt_label.configure(text=text)
        else:
            self.decrypt_label.configure(text="Decrypted text will appear here")

    def _start_status_updates(self):
        """Start periodic status updates"""
        def update_status():
            if self.clipboard_monitor and self.clipboard_monitor.force_decrypt:
                self.status_dot.configure(style="Active.TLabel", text="●")
                self.status_label.configure(text="🔓 Force Decrypt Mode Active")
                self.mode_label.configure(text="Mode: Force Decrypt (10s)")
            else:
                self.status_dot.configure(style="Active.TLabel", text="●")
                self.status_label.configure(text="🟢 Monitoring clipboard...")
                self.mode_label.configure(text="Mode: Auto (Encrypt & Decrypt)")

            self.update_timer_id = self.root.after(1000, update_status)

        update_status()

    def update_mode(self):
        """Update encryption/decryption mode"""
        if not self.clipboard_monitor:
            return

        mode = self.mode_var.get()
        if mode == "decrypt":
            self.clipboard_monitor.force_decrypt = True
            self.status_label.configure(text="🔓 Force Decrypt Mode Active")
            self.mode_label.configure(text="Mode: Force Decrypt (10s)")
        else:
            self.clipboard_monitor.force_decrypt = False
            self.status_label.configure(text="🟢 Monitoring clipboard...")
            self.mode_label.configure(text="Mode: Auto (Encrypt & Decrypt)")

    def generate_new_key(self):
        """Generate a new encryption key with visual feedback"""
        if self.clipboard_monitor:
            self.clipboard_monitor.key_manager.generate_new_key()
            self.status_label.configure(text="🔑 New encryption key generated")
            self.root.after(3000, lambda: self.update_mode())  # Reset status after 3 seconds

    def hide_window(self):
        """Hide the main window"""
        if self.update_timer_id:
            self.root.after_cancel(self.update_timer_id)
        self.root.withdraw()

    def show_window(self):
        """Show and focus the main window"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self._start_status_updates()

    def run(self):
        """Run the main window"""
        self.root.mainloop()