import threading
import time
import pyperclip
import logging
from encryption import Encryption
from key_manager import KeyManager
from notification import NotificationWindow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClipboardMonitor:
    def __init__(self):
        self.previous_content = ''
        self.encryption = Encryption()
        self.key_manager = KeyManager()
        self.clear_timer = None
        self.force_decrypt = False
        self.force_decrypt_timer = None
        self.notification = NotificationWindow()
        self.main_window = None
        self._verify_clipboard_access()
        logging.info("ClipboardMonitor initialized")

    def _verify_clipboard_access(self):
        """Verify that clipboard access is available"""
        try:
            pyperclip.paste()
            logging.info("Clipboard access verified")
        except Exception as e:
            logging.error(f"Clipboard access failed: {e}")
            raise RuntimeError(
                "Could not access clipboard. Please ensure:\n"
                "1. The application has necessary permissions\n"
                "2. No other application is blocking clipboard access\n"
                "3. Clipboard service is running"
            )

    def start_monitoring(self):
        """Start monitoring the clipboard for changes"""
        logging.info("Starting clipboard monitoring")
        consecutive_errors = 0

        while True:
            try:
                current_content = pyperclip.paste()

                if current_content != self.previous_content and current_content:
                    logging.info("Clipboard content changed")
                    self.handle_clipboard_change(current_content)
                    consecutive_errors = 0

                if self.force_decrypt:
                    self.manual_decrypt()

                time.sleep(0.1)  # Short delay for better performance
            except Exception as e:
                logging.error(f"Error monitoring clipboard: {e}")
                consecutive_errors += 1
                if consecutive_errors > 5:
                    logging.error("Multiple consecutive clipboard errors, sleeping...")
                    time.sleep(2)
                    consecutive_errors = 0

    def handle_clipboard_change(self, content):
        """Handle clipboard content changes with enhanced visual feedback"""
        if not content:
            return

        self.previous_content = content
        logging.info("Processing clipboard content")

        try:
            if self.encryption.is_encrypted(content):
                logging.info("Detected encrypted content")
                decrypted = self.encryption.decrypt(content)
                if decrypted:
                    logging.info("Successfully decrypted content")
                    # Update main window's decryption display
                    self.main_window.update_decrypt_display(decrypted)
                    # Show decryption notification with the decrypted text
                    self.notification.show_notification("decrypt", decrypted)
                    # Keep the encrypted text in clipboard but show decrypted version
                    pyperclip.copy(content)
            else:
                logging.info("Detected plain text, encrypting")
                encrypted = self.encryption.encrypt(content)
                if encrypted:
                    logging.info("Successfully encrypted content")
                    pyperclip.copy(encrypted)
                    # Show encryption notification
                    self.notification.show_notification("encrypt", content)
                    # Clear decryption display since we're encrypting
                    self.main_window.update_decrypt_display(None)

            self.start_clear_timer()
        except Exception as e:
            logging.error(f"Error handling clipboard change: {e}")
            # Show error notification
            self.notification.show_notification("error")

    def set_main_window(self, main_window):
        """Set the main window reference"""
        self.main_window = main_window
        logging.info("Main window reference set in ClipboardMonitor")

    def start_clear_timer(self):
        """Start timer to clear clipboard after 30 seconds"""
        if self.clear_timer:
            self.clear_timer.cancel()

        self.clear_timer = threading.Timer(30.0, self.clear_clipboard)
        self.clear_timer.start()
        logging.info("Started clipboard clear timer")

    def clear_clipboard(self):
        """Clear the clipboard contents"""
        pyperclip.copy('')
        self.previous_content = ''
        logging.info("Cleared clipboard contents")

    def toggle_force_decrypt(self):
        """Toggle force decrypt mode with visual feedback"""
        self.force_decrypt = not self.force_decrypt
        status = "enabled" if self.force_decrypt else "disabled"
        logging.info(f"Force decrypt mode {status}")

        if self.force_decrypt:
            if self.force_decrypt_timer:
                self.force_decrypt_timer.cancel()
            self.force_decrypt_timer = threading.Timer(10.0, self.disable_force_decrypt)
            self.force_decrypt_timer.start()
            # Show mode change notification
            self.notification.show_notification("force_decrypt")
        else:
            # Clear decryption display when disabling force decrypt
            self.main_window.update_decrypt_display(None)
        return self.force_decrypt

    def disable_force_decrypt(self):
        """Disable force decrypt mode"""
        self.force_decrypt = False
        logging.info("Force decrypt mode auto-disabled")

    def manual_decrypt(self):
        """Manual decryption"""
        try:
            content = pyperclip.paste()
            if content and self.encryption.is_encrypted(content):
                logging.info("Manual decryption attempt")
                decrypted = self.encryption.decrypt(content)
                if decrypted:
                    logging.info("Manual decryption successful")
                    pyperclip.copy(decrypted)
        except Exception as e:
            logging.error(f"Error in manual decryption: {e}")