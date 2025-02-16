import tkinter as tk
from tkinter import ttk
import threading
import logging
from PIL import Image, ImageDraw

class NotificationWindow:
    def __init__(self):
        self.notifications = []
        self.animation_thread = None
        logging.info("Notification system initialized")

    def show_notification(self, action_type):
        """Show an animated notification for encryption/decryption actions"""
        try:
            # Create notification on the main thread
            notification = self._create_notification(action_type)
            self.notifications.append(notification)

            # Start animation in a separate thread
            if self.animation_thread is None or not self.animation_thread.is_alive():
                self.animation_thread = threading.Thread(target=self._animate_notification, 
                                                      args=(notification,))
                self.animation_thread.daemon = True
                self.animation_thread.start()
                logging.info(f"Started animation thread for {action_type} notification")
        except Exception as e:
            logging.error(f"Error showing notification: {e}")

    def _create_notification(self, action_type):
        """Create a notification window with enhanced visual styling"""
        try:
            window = tk.Tk()
            window.withdraw()  # Hide initially
            window.attributes('-topmost', True)  # Keep on top
            window.overrideredirect(True)  # Remove window decorations

            # Larger window size for better visibility
            window_width = 320
            window_height = 120
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x_position = screen_width - window_width - 20
            y_position = screen_height - window_height - 40

            window.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

            # Configure enhanced styles with distinct colors
            style = ttk.Style()
            if action_type == "encrypt":
                bg_color = "#E8F5E9"  # Light green for encryption
                fg_color = "#2E7D32"  # Dark green for text
                progress_color = "#4CAF50"  # Green for progress bar
            elif action_type == "decrypt":
                bg_color = "#E3F2FD"  # Light blue for decryption
                fg_color = "#1565C0"  # Dark blue for text
                progress_color = "#2196F3"  # Blue for progress bar
            else:  # startup
                bg_color = "#F5F5F5"  # Light gray for startup
                fg_color = "#212121"  # Dark gray for text
                progress_color = "#9E9E9E"  # Gray for progress bar

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

            # Create frame with enhanced border effect
            frame = ttk.Frame(window, style="Notification.TFrame", padding="12")
            frame.pack(fill=tk.BOTH, expand=True)

            # Add content with improved styling
            if action_type == "startup":
                icon = "🔒"
                title = "Secure Clipboard Active"
                message = "Look for the blue lock icon in your system tray"
                duration = 5000  # Longer duration for startup
            else:
                icon = "🔒" if action_type == "encrypt" else "🔓"
                title = "Text Encrypted" if action_type == "encrypt" else "Text Decrypted"
                message = "Clipboard content has been processed"
                duration = 3000  # Slightly longer duration for better visibility

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

            # Progress bar with custom styling
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

    def _animate_notification(self, notification):
        """Animate the notification window with smooth transitions"""
        if not notification:
            return

        try:
            window = notification['window']
            progress = notification['progress']
            duration = notification['duration']

            # Show window with smooth fade-in
            window.deiconify()
            for alpha in range(0, 100, 4):  # Smoother fade-in
                window.attributes('-alpha', alpha/100)
                window.update()
                window.after(8)  # Shorter delay for smoother animation

            # Animate progress bar with smooth motion
            steps = 50  # More steps for smoother animation
            step_duration = duration // steps
            for i in range(steps + 1):
                progress['value'] = (i / steps) * 100
                window.update()
                window.after(step_duration)

            # Smooth fade-out
            for alpha in range(100, -1, -4):  # Smoother fade-out
                window.attributes('-alpha', alpha/100)
                window.update()
                window.after(8)

            # Cleanup
            window.destroy()
            self.notifications.remove(notification)
            logging.info(f"Notification animation completed for {notification['action_type']}")
        except Exception as e:
            logging.error(f"Error in notification animation: {e}")