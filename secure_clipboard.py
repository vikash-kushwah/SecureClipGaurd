import threading
import sys
import logging
from clipboard_monitor import ClipboardMonitor
from system_tray import SystemTrayIcon
from key_manager import KeyManager
from main_window import MainWindow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Initialize key manager and ensure a key exists
        logging.info("Initializing key manager...")
        key_manager = KeyManager()
        encryption_key = key_manager.get_encryption_key()

        if not encryption_key:
            logging.info("No encryption key found, generating new key...")
            key_manager.generate_new_key()

        # Initialize main window first (without clipboard monitor)
        logging.info("Initializing main window...")
        main_window = MainWindow()

        # Initialize clipboard monitor with error handling
        logging.info("Initializing clipboard monitor...")
        try:
            clipboard_monitor = ClipboardMonitor()
        except Exception as e:
            logging.error(f"Failed to initialize clipboard monitor: {e}")
            raise RuntimeError("Could not access clipboard. Please ensure you have the necessary permissions.")

        clipboard_monitor.set_main_window(main_window)
        main_window.set_clipboard_monitor(clipboard_monitor)

        # Start clipboard monitor in a separate thread
        monitor_thread = threading.Thread(target=clipboard_monitor.start_monitoring, daemon=True)
        monitor_thread.start()

        # Initialize and start system tray
        logging.info("Initializing system tray...")
        tray_icon = SystemTrayIcon(clipboard_monitor, main_window)

        # Create a thread for the system tray
        tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
        tray_thread.start()

        # Run the main window (this will block until the window is closed)
        main_window.run()

    except Exception as e:
        logging.error(f"Application startup failed: {e}")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)