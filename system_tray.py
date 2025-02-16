import pystray
import logging
from PIL import Image, ImageDraw
import threading
import sys
from key_manager import KeyManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemTrayIcon:
    def __init__(self, clipboard_monitor):
        self.key_manager = KeyManager()
        self.clipboard_monitor = clipboard_monitor
        self.create_icon()
        logging.info("System tray icon initialized")

    def create_icon(self):
        """Create system tray icon and menu"""
        # Create a meaningful icon (32x32 pixels)
        icon_size = (32, 32)
        icon_image = Image.new('RGBA', icon_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(icon_image)

        # Draw a lock symbol
        padding = 4
        body_width = icon_size[0] - 2 * padding
        body_height = int(icon_size[1] * 0.6)
        shackle_height = int(icon_size[1] * 0.3)

        # Draw lock body
        draw.rectangle(
            (padding, icon_size[1] - body_height - padding,
             icon_size[0] - padding, icon_size[1] - padding),
            fill='white', outline='white'
        )

        # Draw lock shackle
        shackle_width = int(body_width * 0.6)
        shackle_x = (icon_size[0] - shackle_width) // 2
        draw.arc(
            (shackle_x, icon_size[1] - body_height - shackle_height - padding,
             shackle_x + shackle_width, icon_size[1] - body_height + padding),
            180, 0, fill='white', width=2
        )

        logging.info("Created system tray icon image")

        menu = (
            pystray.MenuItem(
                "Toggle Decrypt Mode (Right Click)",
                self.toggle_decrypt,
                default=True
            ),
            pystray.MenuItem(
                "Generate New Encryption Key",
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
            "Secure Clipboard (Running)\nRight-click to toggle decrypt mode",
            menu
        )
        logging.info("System tray menu created")

    def run(self):
        """Run the system tray icon"""
        logging.info("Starting system tray icon")
        self.icon.run()

    def toggle_decrypt(self):
        """Toggle decrypt mode"""
        is_active = self.clipboard_monitor.toggle_force_decrypt()
        status = "enabled" if is_active else "disabled"
        self.icon.title = f"Secure Clipboard (Decrypt Mode: {status})"
        logging.info(f"Decrypt mode {status}")

    def generate_new_key(self):
        """Generate a new encryption key"""
        try:
            self.key_manager.generate_new_key()
            self.icon.title = "Secure Clipboard (New Key Generated)"
            logging.info("Generated new encryption key")
        except Exception as e:
            self.icon.title = "Secure Clipboard (Key Generation Failed)"
            logging.error(f"Error generating new key: {e}")

    def quit_application(self):
        """Exit the application"""
        logging.info("Application shutdown requested")
        self.icon.stop()
        sys.exit(0)