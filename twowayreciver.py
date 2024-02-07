import tkinter as tk
from tkinter import ttk
import requests
import base64
import time

class ReceiverApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Receiver Application")
        self.geometry("400x500")

        self.decrypted_message_var = tk.StringVar()
        self.receiver_message_var = tk.StringVar()
        self.last_received_message = ""  # Variable to store the last received message
        self.create_widgets()

        # Periodically check for new messages
        self.after(1000, self.check_for_messages)

    def create_widgets(self):
        ttk.Label(self, text="Receiver").pack(pady=10)

        ttk.Label(self, text="Decrypted Message:").pack(pady=5)
        ttk.Entry(self, textvariable=self.decrypted_message_var, state='readonly').pack(pady=5)

        ttk.Label(self, text="Chat:").pack(pady=5)
        self.chat_display = tk.Text(self, height=10, width=40)
        self.chat_display.pack(pady=5)

        ttk.Label(self, text="Send Message to Sender:").pack(pady=5)
        ttk.Entry(self, textvariable=self.receiver_message_var).pack(pady=5)

        ttk.Button(self, text="Send to Sender", command=self.send_to_sender).pack(pady=10)

    def send_to_sender(self):
        message_to_send = self.receiver_message_var.get()
        if message_to_send:
            response = requests.post('http://127.0.0.1:5000/send_receiver', data={'plaintext_message': message_to_send})
            if response.status_code == 200:
                print("Message Sent to Sender Successfully")
                self.display_message(f"You (to Sender): {message_to_send}")
            else:
                print('Error sending message to Sender')

    def check_for_messages(self):
        # Periodically check for new messages from the sender
        response = requests.post('http://127.0.0.1:5000/receive')
        if response.status_code == 200:
            decrypted_message = response.json().get('decrypted_message', '')

            # Display the message only if it's different from the last received message
            if decrypted_message != self.last_received_message:
                self.decrypted_message_var.set(decrypted_message)
                self.display_message(f"Sender: {decrypted_message}")
                self.last_received_message = decrypted_message

        # Continue periodic check
        self.after(1000, self.check_for_messages)

    def display_message(self, message):
        current_chat = self.chat_display.get(1.0, tk.END)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, current_chat + message + '\n')

if __name__ == '__main__':
    receiver_app = ReceiverApp()
    receiver_app.mainloop()
