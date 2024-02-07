import os
from flask import Flask, request
from encryption import initialize_cipher_suite, decrypt_data
from PIL import Image
from io import BytesIO

app = Flask(__name__)

received_images_folder = os.path.join(os.getcwd(), "received_images")
os.makedirs(received_images_folder, exist_ok=True)

receiver_chat_history = []

def save_decrypted_image(encrypted_image_data, key):
    cipher_suite = initialize_cipher_suite(key)
    decrypted_image_data = decrypt_data(cipher_suite, encrypted_image_data)

    received_image = Image.open(BytesIO(decrypted_image_data))
    image_filename = f"received_image.png"
    image_path = os.path.join(received_images_folder, image_filename)
    received_image.save(image_path)

    receiver_chat_history.append({'image_path': image_path})

    return "Image received successfully"

@app.route('/receive', methods=['POST'])
def receive_image():
    encrypted_image_data = request.files.get('image_file').read()
    key = request.form.get('key')

    result = save_decrypted_image(encrypted_image_data, key)

    return result, 200

if __name__ == '__main__':
    app.run(debug=True)
