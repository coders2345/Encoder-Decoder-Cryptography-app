import tkinter as tk
from tkinter import ttk
import requests
import base64
import time

class SenderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sender Application")
        self.geometry("400x500")

        self.message_var = tk.StringVar()
        self.encrypted_message_var = tk.StringVar()
        self.received_message_var = tk.StringVar()
        self.last_received_message = ""  # Variable to store the last received message
        self.create_widgets()

        # Periodically check for new messages
        self.after(1000, self.check_for_messages)

    def create_widgets(self):
        ttk.Label(self, text="Sender").pack(pady=10)

        ttk.Label(self, text="Message:").pack(pady=5)
        ttk.Entry(self, textvariable=self.message_var).pack(pady=5)

        ttk.Button(self, text="Send", command=self.send_message).pack(pady=10)

        ttk.Label(self, text="Encrypted Message:").pack(pady=5)
        ttk.Entry(self, textvariable=self.encrypted_message_var, state='readonly').pack(pady=5)

        ttk.Label(self, text="Received Message from Receiver:").pack(pady=5)
        ttk.Entry(self, textvariable=self.received_message_var, state='readonly').pack(pady=5)

        # Display box for showing sent and received messages
        self.message_display = tk.Text(self, height=10, width=40, state='disabled')
        self.message_display.pack(pady=5)

    def send_message(self):
        plaintext_message = self.message_var.get()
        if plaintext_message:
            encrypted_message = base64.b64encode(plaintext_message.encode()).decode()

            # Sending to Receiver
            response_receiver = requests.post('http://127.0.0.1:5000/send_receiver', data={'plaintext_message': plaintext_message})
            if response_receiver.status_code == 200:
                print("Message Sent to Receiver Successfully")
            else:
                print('Error sending message to Receiver')

            # Sending to own server
            response_sender = requests.post('http://127.0.0.1:5000/send', data={'plaintext_message': plaintext_message})
            if response_sender.status_code == 200:
                print("Message Sent to Own Server Successfully")
                self.encrypted_message_var.set(f"Encrypted: {encrypted_message}")
                self.display_message(f"You (to Receiver): {plaintext_message}")
            else:
                print('Error sending message to Own Server')

    def check_for_messages(self):
        # Periodically check for new messages from the receiver
        response = requests.post('http://127.0.0.1:5000/receive_receiver')
        if response.status_code == 200:
            received_message = response.json().get('decrypted_message', '')

            # Display the message only if it's different from the last received message
            if received_message != self.last_received_message:
                self.received_message_var.set(f"Received: {received_message}")

                # Clear the received message after displaying it
                response = requests.post('http://127.0.0.1:5000/clear_received_message')
                if response.status_code == 200:
                    print("Received message cleared successfully")
                else:
                    print("Error clearing received message")

                # Display the received message in the message display box
                self.display_message(f"Receiver: {received_message}")

                self.last_received_message = received_message  # Update the last received message

        # Continue periodic check
        self.after(1000, self.check_for_messages)

    def display_message(self, message):
        # Insert a new line before displaying each message
        self.message_display.configure(state='normal')
        self.message_display.insert(tk.END, message + '\n')
        self.message_display.configure(state='disabled')
        self.message_display.see(tk.END)  # Scroll to the end to show the latest message

if __name__ == '__main__':
    sender_app = SenderApp()
    sender_app.mainloop()
