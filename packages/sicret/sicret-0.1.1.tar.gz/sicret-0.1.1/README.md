# Sicret - What Happens in Secret Stays in Sicret


## Overview
Sicret is a command-line utility tool designed to securely encrypt and decrypt directories. Using robust cryptography, it ensures the confidentiality of your data. 

The tool is user-friendly and operates exclusively through the command line, making it suitable for a variety of users who prefer a quick and secure way to protect their folders.

## Installation

To install Sicret, ensure you have Python installed on your system.

You can install Sicret using pip:

```bash
pip install sicret
```

## Usage
Sicret is straightforward to use with two primary commands: -e for encryption and -d for decryption.

### Encrypting a Directory
To encrypt a directory, use the following command:

```bash
sicret -e /path/to/folder
```

This will encrypt the specified folder, and the resulting encrypted file will have the extension .sicret.enc. 
The original folder will be deleted after encryption to ensure security.

### Encrypting a Directory
To decrypt a previously encrypted directory, use the command:

```bash
sicret -d /path/to/folder
```

Note that you do not need to specify the .sicret.enc extension; the tool automatically appends this to locate the encrypted file. 
The decrypted folder will be restored to its original state.

### Security
Sicret uses the Fernet symmetric encryption standard from the cryptography library, ensuring high security for your encrypted data.


### Disclaimer
While Sicret is designed with security in mind, it's important to remember that no encryption tool can offer absolute security. Users are advised to keep backups of their important data and use strong, unique passwords for encryption.

The developer of Sicret is not responsible for data loss or any potential security breaches.

### Contributing
Contributions to Sicret are welcome. Please feel free to fork the repository, make improvements, and submit pull requests.



