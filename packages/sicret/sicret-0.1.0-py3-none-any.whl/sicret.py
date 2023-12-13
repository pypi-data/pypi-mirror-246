import os
import shutil
import sys
import tarfile
from base64 import urlsafe_b64encode
from getpass import getpass

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def compress_folder(folder_path, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))


def decompress_folder(file_path, output_path):
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(path=output_path)


def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted = file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted)


def generate_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode())
    return urlsafe_b64encode(key)


def main():
    if len(sys.argv) != 3:
        print("Usage: sicret -e|-d <folder_path>")
        sys.exit(1)

    option = sys.argv[1]
    path = sys.argv[2]

    password = getpass("Enter password: ")

    salt = b"sicret"

    key = generate_key_from_password(password, salt)

    if option == "-e":
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("Error: Passwords do not match.")
            sys.exit(1)

        compressed_file = path + ".tar.gz"
        compress_folder(path, compressed_file)
        encrypt_file(compressed_file, key)

        encrypted_file = path + ".sicret.enc"
        os.rename(compressed_file, encrypted_file)
        shutil.rmtree(path)

        print(f"Encrypted folder as {encrypted_file}")
    elif option == "-d":
        encrypted_file = path + ".sicret.enc"

        decrypt_file(encrypted_file, key)

        output_path = os.path.dirname(path) if os.path.dirname(path) else "."

        decompress_folder(encrypted_file, output_path)
        os.remove(encrypted_file)
        print(f"Decrypted folder to {path}")

    else:
        print("Invalid option. Use -e to encrypt or -d to decrypt.")
        sys.exit(1)


if __name__ == "__main__":
    main()
