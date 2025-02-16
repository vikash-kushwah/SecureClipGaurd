import threading
import time
import pyperclip
import keyboard
import logging
import sys
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
        if sys.platform == 'win32':  # Only setup shortcut on Windows
            self._setup_shortcut()
        logging.info("ClipboardMonitor initialized")

    def _setup_shortcut(self):
        """Setup keyboard shortcut for instant encryption (Windows only)"""
        try:
            keyboard.add_hotkey('ctrl+alt+e', self.encrypt_and_paste)
            logging.info("Encryption shortcut (Ctrl+Alt+E) registered on Windows")
        except Exception as e:
            logging.error(f"Failed to register Windows shortcut: {e}")

    def encrypt_and_paste(self):
        """Handle the encrypt-and-paste shortcut"""
        try:
            # Store current clipboard content
            original_content = self._safe_clipboard_operation("paste")

            # Simulate Ctrl+C to get selected text
            keyboard.send('ctrl+c')
            time.sleep(0.1)  # Small delay to ensure clipboard is updated

            # Get the selected text
            selected_text = self._safe_clipboard_operation("paste")

            if selected_text and selected_text != original_content:
                # Encrypt the selected text
                encrypted = self.encryption.encrypt(selected_text)
                if encrypted:
                    # Copy encrypted text to clipboard
                    self._safe_clipboard_operation("copy", encrypted)
                    # Simulate Ctrl+V to paste
                    keyboard.send('ctrl+v')
                    # Show encryption notification
                    self.notification.show_notification("encrypt", selected_text)
                    logging.info("Text encrypted and pasted via shortcut")
                else:
                    logging.error("Failed to encrypt text")
                    self.notification.show_notification("error")

                # Restore original clipboard content after a small delay
                def restore_clipboard():
                    time.sleep(0.5)  # Wait for paste to complete
                    if original_content:
                        self._safe_clipboard_operation("copy", original_content)

                # Start restoration in a separate thread
                threading.Thread(target=restore_clipboard, daemon=True).start()
            else:
                logging.warning("No new text selected or clipboard unchanged")

        except Exception as e:
            logging.error(f"Error in encrypt-and-paste shortcut: {e}")
            self.notification.show_notification("error")

    def set_main_window(self, main_window):
        """Set the main window reference"""
        self.main_window = main_window
        logging.info("Main window reference set in ClipboardMonitor")

    def _verify_clipboard_access(self):
        """Verify that clipboard access is available on Windows"""
        try:
            pyperclip.paste()
            logging.info("Windows clipboard access verified")
        except Exception as e:
            logging.error(f"Windows clipboard access failed: {e}")
            raise RuntimeError(
                "Could not access Windows clipboard. Please ensure:\n"
                "1. The application has necessary permissions\n"
                "2. No other application is blocking clipboard access\n"
                "3. Windows clipboard service is running"
            )

    def _safe_clipboard_operation(self, operation, *args):
        """Safely perform clipboard operations with Windows-specific handling"""
        max_retries = 3
        retry_delay = 0.1  # Shorter delay for Windows

        for attempt in range(max_retries):
            try:
                if operation == "copy":
                    pyperclip.copy(args[0])
                    return True
                elif operation == "paste":
                    return pyperclip.paste()
            except Exception as e:
                logging.error(f"Windows clipboard {operation} failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return None if operation == "paste" else False

        return None if operation == "paste" else False

    def start_monitoring(self):
        """Start monitoring the clipboard for changes"""
        logging.info("Starting Windows clipboard monitoring")
        consecutive_errors = 0

        while True:
            try:
                current_content = self._safe_clipboard_operation("paste")
                if current_content is None:
                    consecutive_errors += 1
                    if consecutive_errors > 5:
                        logging.error("Multiple consecutive Windows clipboard errors, sleeping...")
                        time.sleep(2)  # Shorter sleep for Windows
                        consecutive_errors = 0
                    continue

                if current_content != self.previous_content:
                    logging.info("Clipboard content changed")
                    self.handle_clipboard_change(current_content)
                    consecutive_errors = 0

                if self.force_decrypt:
                    self.manual_decrypt()

                time.sleep(0.1)  # Reduced delay for better Windows performance
            except Exception as e:
                logging.error(f"Error monitoring Windows clipboard: {e}")
                consecutive_errors += 1

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
                    self._safe_clipboard_operation("copy", content)
            else:
                logging.info("Detected plain text, encrypting")
                encrypted = self.encryption.encrypt(content)
                if encrypted:
                    logging.info("Successfully encrypted content")
                    self._safe_clipboard_operation("copy", encrypted)
                    # Show encryption notification
                    self.notification.show_notification("encrypt", content)
                    # Clear decryption display since we're encrypting
                    self.main_window.update_decrypt_display(None)

            self.start_clear_timer()
        except Exception as e:
            logging.error(f"Error handling clipboard change: {e}")
            # Show error notification
            self.notification.show_notification("error")

    def start_clear_timer(self):
        """Start timer to clear clipboard after 30 seconds"""
        if self.clear_timer:
            self.clear_timer.cancel()

        self.clear_timer = threading.Timer(30.0, self.clear_clipboard)
        self.clear_timer.start()
        logging.info("Started clipboard clear timer")

    def clear_clipboard(self):
        """Clear the clipboard contents"""
        self._safe_clipboard_operation("copy", '')
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
            content = self._safe_clipboard_operation("paste")
            if content and self.encryption.is_encrypted(content):
                logging.info("Manual decryption attempt")
                decrypted = self.encryption.decrypt(content)
                if decrypted:
                    logging.info("Manual decryption successful")
                    self._safe_clipboard_operation("copy", decrypted)
        except Exception as e:
            logging.error(f"Error in manual decryption: {e}")