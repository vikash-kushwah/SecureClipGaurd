pip install pillow pyperclip pystray cryptography keyrings.alt keyring
```

3. Clone or download this repository:
```bash
git clone https://github.com/yourusername/secure-clipboard.git
cd secure-clipboard
```

4. Run the application:
```bash
python secure_clipboard.py
```

## 📝 Usage

### Basic Operation

1. **Start the Application**
   - Run `secure_clipboard.py`
   - Look for the blue lock icon in your system tray (bottom right corner)

2. **Encrypting Messages**
   - Simply copy any text
   - The text is automatically encrypted
   - A notification confirms successful encryption

3. **Decrypting Messages**
   - Copy an encrypted message
   - The decrypted text appears automatically
   - View the decrypted content in the notification

### System Tray Features

Right-click the blue lock icon to access:
- 🔄 **Toggle Force Decrypt Mode**: Temporarily force decryption for 10 seconds
- 🔑 **Generate New Key**: Create a new encryption key
- ⚙️ **Open Control Panel**: Access additional settings
- 🚪 **Exit**: Close the application

### Control Panel

Access advanced features through the control panel:
- Monitor encryption status
- View live decryption display
- Generate new encryption keys
- Toggle between auto and force decrypt modes

## 🛡️ Security Features

1. **Encryption Standard**
   - AES-256 encryption (military-grade)
   - Secure key generation and storage
   - OS-protected key storage

2. **Data Protection**
   - Automatic clipboard clearing (30-second timeout)
   - Encrypted storage of sensitive data
   - Secure key management

3. **Visual Security**
   - Clear status indicators
   - Operation confirmations
   - Encryption/decryption notifications

## 💻 System Requirements

- Windows Operating System
- Python 3.7 or higher
- Required Python packages:
  - pillow
  - pyperclip
  - pystray
  - cryptography
  - keyrings.alt
  - keyring

## 🔍 Troubleshooting

### Common Issues

1. **Installation Problems**
   ```bash
   pip install --upgrade pillow pyperclip pystray cryptography keyrings.alt keyring