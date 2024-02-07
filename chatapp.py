from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

app = Flask(__name__)

# Generate a key for encryption and decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

sender_chat_history = []  # Store sender's chat history
receiver_chat_history = []  # Store receiver's chat history

def encrypt_message(message):
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message):
    return cipher_suite.decrypt(encrypted_message).decode()

@app.route('/send', methods=['POST'])
def send_message():
    plaintext_message = request.form.get('plaintext_message', '')
    encrypted_message = encrypt_message(plaintext_message)

    sender_chat_history.append({'type': 'sender', 'message': encrypted_message})

    return jsonify({'status': 'Message sent successfully'}), 200

@app.route('/receive', methods=['POST'])
def receive_message():
    if sender_chat_history:
        encrypted_message = sender_chat_history[-1]['message']
        decrypted_message = decrypt_message(encrypted_message)

        sender_chat_history.append({'type': 'receiver', 'message': encrypted_message})

        return jsonify({'decrypted_message': decrypted_message}), 200

    return jsonify({'status': 'No messages available'}), 404

@app.route('/send_receiver', methods=['POST'])
def send_message_to_receiver():
    plaintext_message = request.form.get('plaintext_message', '')
    encrypted_message = encrypt_message(plaintext_message)

    receiver_chat_history.append({'type': 'receiver', 'message': encrypted_message})

    return jsonify({'status': 'Message sent to receiver successfully'}), 200

@app.route('/receive_receiver', methods=['POST'])
def receive_message_from_receiver():
    if receiver_chat_history:
        encrypted_message = receiver_chat_history[-1]['message']
        decrypted_message = decrypt_message(encrypted_message)

        receiver_chat_history.append({'type': 'sender', 'message': encrypted_message})

        return jsonify({'decrypted_message': decrypted_message}), 200

    return jsonify({'status': 'No messages available from receiver'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
