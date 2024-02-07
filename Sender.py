import requests
import os
from tkinter import filedialog
from tkinter import Tk
from encryption import generate_key, initialize_cipher_suite, encrypt_data


def choose_image():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return file_path


def send_encrypted_image(image_path, key):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    cipher_suite = initialize_cipher_suite(key)
    encrypted_image_data = encrypt_data(cipher_suite, image_data)

    files = {'image_file': ('encrypted_image.png', encrypted_image_data)}
    data = {'key': key}
    response = requests.post('http://127.0.0.1:5000/receive', files=files, data=data)

    if response.status_code == 200:
        print("Image sent successfully")
    else:
        print('Error sending image to Receiver')


if __name__ == '__main__':
    key = generate_key()
    image_path = choose_image()

    if image_path:
        send_encrypted_image(image_path, key)
