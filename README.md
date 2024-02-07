Encoder-Decoder App
The Encoder-Decoder app is a Python application that enables users to encrypt and decrypt messages and images using cryptography techniques. It consists of two main components: the sender and receiver modules.

Sender Module
The sender module allows users to encrypt messages and images before sending them to a receiver. Users can input plaintext messages or select an image file to encrypt. The app encrypts the data using a generated key and sends it to the receiver via HTTP POST requests.

Receiver Module
The receiver module receives encrypted messages and images from the sender and decrypts them using the shared key. It saves decrypted images to a designated folder and maintains a chat history of received messages. The receiver responds with the decrypted message or confirmation upon successful reception.

Features
Encrypt plaintext messages and images
Decrypt received messages and images
Store chat history of sender and receiver
Simple HTTP endpoints for sending and receiving encrypted data
Usage
Run the sender module (sender.py) to encrypt and send messages or images.
Run the receiver module (receiver.py) to receive and decrypt messages or images.
Dependencies
requests library for handling HTTP requests
Flask library for building web applications
cryptography library for encryption and decryption
How to Run
Install dependencies: pip install requests flask cryptography
Run sender module: python sender.py
Run receiver module: python receiver.py
