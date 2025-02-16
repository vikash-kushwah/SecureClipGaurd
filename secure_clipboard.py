import threading
import sys
from clipboard_monitor import ClipboardMonitor
from system_tray import SystemTrayIcon
from key_manager import KeyManager
from main_window import MainWindow

def main():
    # Initialize key manager and ensure a key exists
    key_manager = KeyManager()
    if not key_manager.get_encryption_key():
        key_manager.generate_new_key()

    # Initialize main window first (without clipboard monitor)
    main_window = MainWindow()

    # Initialize clipboard monitor
    clipboard_monitor = ClipboardMonitor()
    clipboard_monitor.set_main_window(main_window)  # Set the main window using the new method
    main_window.set_clipboard_monitor(clipboard_monitor)  # Set the monitor using the new method

    # Start clipboard monitor in a separate thread
    monitor_thread = threading.Thread(target=clipboard_monitor.start_monitoring, daemon=True)
    monitor_thread.start()

    # Initialize and start system tray
    tray_icon = SystemTrayIcon(clipboard_monitor, main_window)

    # Create a thread for the system tray
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()

    # Run the main window (this will block until the window is closed)
    main_window.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)