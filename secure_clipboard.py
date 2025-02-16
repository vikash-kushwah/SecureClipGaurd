import threading
import sys
from clipboard_monitor import ClipboardMonitor
from system_tray import SystemTrayIcon
from key_manager import KeyManager

def main():
    # Initialize key manager and ensure a key exists
    key_manager = KeyManager()
    if not key_manager.get_encryption_key():
        key_manager.generate_new_key()

    # Start clipboard monitor in a separate thread
    clipboard_monitor = ClipboardMonitor()
    monitor_thread = threading.Thread(target=clipboard_monitor.start_monitoring, daemon=True)
    monitor_thread.start()

    # Initialize and start system tray
    tray_icon = SystemTrayIcon(clipboard_monitor)
    tray_icon.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)