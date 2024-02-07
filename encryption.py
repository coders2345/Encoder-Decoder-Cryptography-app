from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def initialize_cipher_suite(key):
    return Fernet(key)

def encrypt_data(cipher_suite, data):
    return cipher_suite.encrypt(data)

def decrypt_data(cipher_suite, encrypted_data):
    return cipher_suite.decrypt(encrypted_data)
