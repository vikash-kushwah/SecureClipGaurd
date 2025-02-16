import pystray
import logging
from PIL import Image, ImageDraw
import threading
import sys
from key_manager import KeyManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationWindow:
    def show_notification(self, message_type):
        if message_type == "startup":
            print("Secure Clipboard is running - Look for the blue lock icon in your system tray (bottom right corner)")

class SystemTrayIcon:
    def __init__(self, clipboard_monitor, main_window):
        self.key_manager = KeyManager()
        self.clipboard_monitor = clipboard_monitor
        self.main_window = main_window
        self.notification = NotificationWindow()
        self.create_icon()
        logging.info("System tray icon initialized")

    def create_icon(self):
        """Create system tray icon and menu"""
        # Create a Windows-friendly icon (32x32 pixels for better visibility)
        icon_size = (32, 32)
        icon_image = Image.new('RGBA', icon_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(icon_image)

        # Draw a more visible lock symbol optimized for Windows
        padding = 4
        body_width = icon_size[0] - 2 * padding
        body_height = int(icon_size[1] * 0.6)

        # Draw lock body (bright blue with white outline for better visibility)
        draw.rectangle(
            (padding, icon_size[1] - body_height - padding,
             icon_size[0] - padding, icon_size[1] - padding),
            fill='#1E90FF', outline='white', width=2
        )

        # Draw lock shackle (thicker for visibility)
        shackle_width = int(body_width * 0.6)
        shackle_x = (icon_size[0] - shackle_width) // 2
        draw.arc(
            (shackle_x, icon_size[1] - body_height - padding - 4,
             shackle_x + shackle_width, icon_size[1] - body_height + padding),
            180, 0, fill='white', width=3
        )

        # Show startup notification
        self.notification.show_notification("startup")

        logging.info("Created system tray icon image (Windows optimized)")

        # Windows-friendly menu with clear instructions
        menu = (
            pystray.MenuItem(
                "Open Control Panel",
                self.show_main_window,
                default=True
            ),
            pystray.MenuItem(
                "Toggle Decryption Mode",
                self.toggle_decrypt
            ),
            pystray.MenuItem(
                "Generate New Key",
                self.generate_new_key
            ),
            pystray.MenuItem(
                "Exit Secure Clipboard",
                self.quit_application
            )
        )

        self.icon = pystray.Icon(
            "SecureClipboard",
            icon_image,
            "Secure Clipboard (Active - Auto Mode)",  # Removed shortcut from tooltip
            menu
        )
        logging.info("System tray menu created with Windows-friendly options")

    def show_main_window(self):
        """Show the main control panel window"""
        self.main_window.show_window()

    def run(self):
        """Run the system tray icon"""
        logging.info("Starting system tray icon")
        try:
            self.icon.run()
        except Exception as e:
            logging.error(f"Error running system tray icon: {e}")
            sys.exit(1)

    def toggle_decrypt(self):
        """Toggle decrypt mode"""
        is_active = self.clipboard_monitor.toggle_force_decrypt()
        status = "Force Decrypt" if is_active else "Auto"
        self.icon.title = f"Secure Clipboard (Active - {status} Mode)"
        logging.info(f"Decryption mode {status}")

    def generate_new_key(self):
        """Generate a new encryption key"""
        try:
            self.key_manager.generate_new_key()
            self.icon.title = "Secure Clipboard (Active - New Key Generated)"
            logging.info("Generated new encryption key")
        except Exception as e:
            self.icon.title = "Secure Clipboard (Active - Key Generation Failed)"
            logging.error(f"Error generating new key: {e}")

    def quit_application(self):
        """Exit the application"""
        logging.info("Application shutdown requested")
        try:
            self.icon.stop()
        except Exception as e:
            logging.error(f"Error stopping system tray icon: {e}")
        finally:
            sys.exit(0)