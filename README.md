# 🔐 Secure Clipboard Encryption Tool

A Python-based secure clipboard encryption tool for Windows that provides seamless text encryption and decryption across messaging platforms. This tool runs in the background, automatically encrypting copied text and decrypting encrypted messages when they're copied.

## 🌟 Key Features

- **Automatic Encryption**: Instantly encrypts text when copied
- **Automatic Decryption**: Automatically decrypts encrypted text when copied
- **Quick Encrypt Shortcut**: Use Ctrl+Alt+E to encrypt and paste selected text in-place
- **System Tray Integration**: Easy access to controls via system tray icon
- **Visual Notifications**: Clear feedback for encryption/decryption actions
- **Secure Key Storage**: Uses OS-protected keyring for storing encryption keys
- **Auto-Clear Clipboard**: Automatically clears clipboard after 30 seconds for security

## 🛠️ System Requirements

- Windows Operating System
- Python 3.8 or higher
- Administrative privileges (for clipboard access)

## 📦 Installation

1. Install required Python packages:
```bash
pip install keyring pillow keyboard pyperclip pystray cryptography
```

2. Clone or download the repository:
```bash
git clone https://github.com/vikash-kushwah/SecureClipGaurd.git
cd SecureClipGaurd
```

## 🚀 Usage

1. Run the application:
```bash
python secure_clipboard.py
```

2. Look for the blue lock icon in your system tray (bottom right corner)

3. The application will:
   - Automatically encrypt any text you copy
   - Automatically decrypt any encrypted text you copy
   - Show notifications for encryption/decryption actions

## ⌨️ Shortcuts & Controls

- **Ctrl+Alt+E**: Quick encrypt and paste selected text
- **System Tray Menu**:
  - Open Control Panel: View and manage encryption settings
  - Toggle Decryption Mode: Force decrypt mode for 10 seconds
  - Generate New Key: Create a new encryption key
  - Exit: Close the application

## 🔒 Security Features

- Uses AES-256 encryption for maximum security
- Secure key storage using OS keyring
- Automatic clipboard clearing after 30 seconds
- Visual feedback for all encryption/decryption actions

## 💡 Tips & Troubleshooting

1. **Clipboard Access Issues**:
   - Ensure the application has necessary permissions
   - Check if other applications are blocking clipboard access
   - Verify Windows clipboard service is running

2. **Shortcut Not Working**:
   - Ensure no other application is using the same shortcut
   - Run the application with administrative privileges

3. **Encryption Key Issues**:
   - Use "Generate New Key" from the system tray menu
   - Check Windows Credential Manager access

## 🚨 Important Notes

- Keep your encryption keys secure
- The application must be running for encryption/decryption to work
- Text is automatically encrypted when copied to protect your data
- Encrypted text remains encrypted in the clipboard until copied again

## 🔍 How It Works

1. **Encryption Process**:
   - User copies text
   - Text is automatically encrypted
   - Encrypted version is placed in clipboard
   - Notification shows successful encryption

2. **Decryption Process**:
   - User copies encrypted text
   - Text is automatically decrypted
   - Original text is shown in notification
   - Encrypted version remains in clipboard for security

## 👥 Contributing

Feel free to submit issues and enhancement requests!

## 📜 License

[Insert License Information]

## 🙏 Acknowledgments

- Built with Python and modern encryption libraries
- Uses Windows-native clipboard integration
- Secure key storage with system keyring
