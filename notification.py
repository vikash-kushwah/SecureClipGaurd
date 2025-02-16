import tkinter as tk
from tkinter import ttk
import threading
import logging
from PIL import Image, ImageDraw

class NotificationWindow:
    def __init__(self):
        self.notifications = []
        self.animation_thread = None
        self.root = None
        self.is_initialized = False
        logging.info("Notification system initialized")

    def initialize_root(self):
        """Initialize the root window if not already done"""
        if not self.is_initialized:
            if threading.current_thread() is threading.main_thread():
                if self.root is None:
                    self.root = tk.Tk()
                    self.root.withdraw()
                self.is_initialized = True
                logging.info("Notification root window initialized")
            else:
                logging.warning("Attempted to initialize root from non-main thread")

    def show_notification(self, action_type):
        """Show an animated notification for encryption/decryption actions"""
        try:
            # Initialize root window if needed
            self.initialize_root()

            # Ensure we're on the main thread for Tkinter operations
            if threading.current_thread() is not threading.main_thread():
                logging.info("Scheduling notification from background thread")
                if self.root:
                    self.root.after(0, lambda: self._show_notification_internal(action_type))
                return

            self._show_notification_internal(action_type)
        except Exception as e:
            logging.error(f"Error showing notification: {e}")

    def _show_notification_internal(self, action_type):
        """Internal method to handle notification creation and display"""
        try:
            # Create notification window
            notification = self._create_notification(action_type)
            if notification:
                self.notifications.append(notification)

                # Start animation in a separate thread
                if self.animation_thread is None or not self.animation_thread.is_alive():
                    self.animation_thread = threading.Thread(
                        target=self._animate_notification,
                        args=(notification,)
                    )
                    self.animation_thread.daemon = True
                    self.animation_thread.start()
                    logging.info(f"Started animation thread for {action_type} notification")
        except Exception as e:
            logging.error(f"Error in _show_notification_internal: {e}")

    def _create_notification(self, action_type):
        """Create a notification window with enhanced visual styling"""
        try:
            window = tk.Toplevel() if self.root else tk.Tk()
            window.withdraw()  # Hide initially
            window.attributes('-topmost', True)  # Keep on top
            window.overrideredirect(True)  # Remove window decorations

            # Set window properties
            window_width = 320
            window_height = 120
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x_position = screen_width - window_width - 20
            y_position = screen_height - window_height - 40

            window.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

            # Configure styles with distinct colors
            style = ttk.Style(window)
            if action_type == "encrypt":
                bg_color = "#E8F5E9"  # Light green
                fg_color = "#2E7D32"  # Dark green
                progress_color = "#4CAF50"
            elif action_type == "decrypt":
                bg_color = "#E3F2FD"  # Light blue
                fg_color = "#1565C0"  # Dark blue
                progress_color = "#2196F3"
            else:
                bg_color = "#F5F5F5"  # Light gray
                fg_color = "#212121"  # Dark gray
                progress_color = "#9E9E9E"

            style.configure("Notification.TFrame",
                          background=bg_color)
            style.configure("Notification.TLabel",
                          font=("Segoe UI", 12, "bold"),
                          background=bg_color,
                          foreground=fg_color)
            style.configure("Message.TLabel",
                          font=("Segoe UI", 10),
                          background=bg_color,
                          foreground=fg_color)
            style.configure("Notification.Horizontal.TProgressbar",
                          background=progress_color,
                          troughcolor=bg_color)

            # Create frame
            frame = ttk.Frame(window, style="Notification.TFrame", padding="12")
            frame.pack(fill=tk.BOTH, expand=True)

            # Add content
            icon = "🔒" if action_type == "encrypt" else "🔓"
            title = self._get_notification_title(action_type)
            message = self._get_notification_message(action_type)
            duration = self._get_notification_duration(action_type)

            # Title with icon
            title_label = ttk.Label(frame,
                                  text=f"{icon} {title}",
                                  style="Notification.TLabel")
            title_label.pack(pady=(0, 8))

            # Message
            message_label = ttk.Label(frame,
                                    text=message,
                                    style="Message.TLabel")
            message_label.pack(pady=(0, 8))

            # Progress bar
            progress = ttk.Progressbar(frame,
                                     style="Notification.Horizontal.TProgressbar",
                                     mode='determinate',
                                     length=280)
            progress.pack(pady=(4, 0))

            window.update_idletasks()
            return {
                'window': window,
                'progress': progress,
                'duration': duration,
                'action_type': action_type
            }
        except Exception as e:
            logging.error(f"Error creating notification window: {e}")
            return None

    def _get_notification_title(self, action_type):
        """Get the appropriate title for the notification"""
        titles = {
            "encrypt": "Text Encrypted",
            "decrypt": "Text Decrypted",
            "force_decrypt": "Force Decrypt Mode",
            "error": "Operation Failed",
            "startup": "Secure Clipboard Active"
        }
        return titles.get(action_type, "Notification")

    def _get_notification_message(self, action_type):
        """Get the appropriate message for the notification"""
        messages = {
            "encrypt": "Text has been encrypted",
            "decrypt": "Text has been decrypted",
            "force_decrypt": "Force decrypt mode activated (10s)",
            "error": "An error occurred during operation",
            "startup": "Look for the blue lock icon in your system tray"
        }
        return messages.get(action_type, "")

    def _get_notification_duration(self, action_type):
        """Get the appropriate duration for the notification"""
        durations = {
            "startup": 5000,  # 5 seconds
            "error": 4000,    # 4 seconds
            "default": 3000   # 3 seconds
        }
        return durations.get(action_type, durations["default"])

    def _animate_notification(self, notification):
        """Animate the notification window with smooth transitions"""
        if not notification:
            return

        try:
            window = notification['window']
            progress = notification['progress']
            duration = notification['duration']

            # Show window with fade-in
            window.deiconify()
            for alpha in range(0, 100, 4):
                window.attributes('-alpha', alpha/100)
                window.update()
                window.after(8)

            # Animate progress bar
            steps = 50
            step_duration = duration // steps
            for i in range(steps + 1):
                progress['value'] = (i / steps) * 100
                window.update()
                window.after(step_duration)

            # Fade-out
            for alpha in range(100, -1, -4):
                window.attributes('-alpha', alpha/100)
                window.update()
                window.after(8)

            # Cleanup
            window.destroy()
            self.notifications.remove(notification)
            logging.info(f"Notification animation completed for {notification['action_type']}")
        except Exception as e:
            logging.error(f"Error in notification animation: {e}")
            try:
                if window and window.winfo_exists():
                    window.destroy()
            except:
                pass