from cryptography.fernet import Fernet
import json

KEY_FILE = "data/encryption_key.key"

# Generate a key (run this once and save the key securely)
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved.")

# Load the encryption key
def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Encrypt JSON data and save to a file
def encrypt_json(data, output_file):
    key = load_key()
    fernet = Fernet(key)
    json_data = json.dumps(data).encode()
    encrypted_data = fernet.encrypt(json_data)
    with open(output_file, "wb") as file:
        file.write(encrypted_data)
    print(f"Data encrypted and saved to {output_file}.")

# Decrypt JSON file and return data
def decrypt_json(input_file):
    key = load_key()
    fernet = Fernet(key)
    with open(input_file, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())