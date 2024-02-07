from flask import Flask, request
from encryption import initialize_cipher_suite, decrypt_data

app = Flask(__name__)

sender_chat_history = []

def decrypt_message(encrypted_message, key):
    cipher_suite = initialize_cipher_suite(key)
    decrypted_message = decrypt_data(cipher_suite, encrypted_message).decode()
    return decrypted_message

@app.route('/send', methods=['POST'])
def send_message():
    text_message = request.form.get('text_message')
    key = request.form.get('key')

    encrypted_message = encrypt_message(text_message, key)

    sender_chat_history.append({'message': encrypted_message})

    return "Message sent successfully", 200

@app.route('/receive', methods=['POST'])
def receive_message():
    encrypted_message = sender_chat_history[-1]['message']
    key = request.form.get('key')

    decrypted_message = decrypt_message(encrypted_message, key)

    return {"decrypted_message": decrypted_message}, 200

def encrypt_message(message, key):
    cipher_suite = initialize_cipher_suite(key)
    encrypted_message = encrypt_data(cipher_suite, message.encode())
    return encrypted_message

if __name__ == '__main__':
    app.run(debug=True)
