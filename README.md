pip install keyboard pillow pyperclip pystray cryptography keyrings.alt keyring
```

2. Clone or download the repository:
```bash
git clone https://github.com/yourusername/secure-clipboard.git
cd secure-clipboard
```

3. Run the application:
```bash
python secure_clipboard.py
```

## 📝 Usage

1. After running the application, look for the blue lock icon in your system tray (bottom right corner)
2. Copy any text to automatically encrypt it
3. Copy encrypted text to automatically see the decrypted version
4. Use Ctrl+Alt+E to quickly encrypt and paste selected text

## ⌨️ Keyboard Shortcuts

- `Ctrl+Alt+E`: Quick encrypt and paste selected text
- Right-click system tray icon for additional options

## 🔧 Troubleshooting

If you encounter any issues:

1. Missing packages:
   ```bash
   pip install --upgrade keyboard pillow pyperclip pystray cryptography keyrings.alt keyring