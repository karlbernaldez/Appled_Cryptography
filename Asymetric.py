import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog, QPushButton, QMessageBox
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from PyQt5 import QtWidgets, QtGui, QtCore

class RSAApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("RSA Encryption App")

         # Create the widgets
        self.label = QLabel("Enter text or choose a file to encrypt:", self)
        self.label.move(20, 20)
        self.input = QTextEdit(self)
        self.input.setAcceptRichText(False)
        self.input.setGeometry(20, 50, 460, 200)
        self.file_button = QPushButton("Choose a File", self)
        self.file_button.setGeometry(290, 15, 100, 30)
        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.setGeometry(140, 270, 100, 30)
        self.decrypt_button = QPushButton("Decrypt", self)
        self.decrypt_button.setGeometry(260, 270, 100, 30)
        self.generate_key_btn = QPushButton("Generate Key", self)
        self.generate_key_btn.setGeometry(20, 270, 100, 30)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(380, 270, 100, 30)

        # Connect the buttons to their functions
        self.file_button.clicked.connect(self.choose_file)
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.generate_key_btn.clicked.connect(self.generate_key_pair)
        self.cancel_button.clicked.connect(self.cancel)

        # Show the window
        self.show()

    def choose_file(self):
        # Allow the user to choose a file to encrypt
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose a file", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            with open(file_path, "r") as f:
                self.input.setPlainText(f.read())

    def generate_key_pair(self):
        # Generate an RSA key pair
        key = RSA.generate(2048)

        # Save the public and private keys to files
        with open("public_key.pem", "wb") as f:
            f.write(key.publickey().export_key())
        with open("private_key.pem", "wb") as f:
            f.write(key.export_key())
    
        # Show a message box with the file paths
        msg = QMessageBox()
        msg.setWindowTitle("Key Pair Generated")
        msg.setText(f"The RSA key pair has been generated and saved to public_key.pem and private_key.pem.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        return key
    
    def encrypt_text(self):
        # Get the text to encrypt
        text = self.input.toPlainText().strip()
        
        # Open a file dialog box to select the decryption key
        keypath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a public key file")

        # Load the encryption key
        with open(keypath, 'rb') as key_file:
            key = RSA.import_key(key_file.read())
            
        # Encrypt the text using PKCS1_OAEP
        cipher = PKCS1_OAEP.new(key.publickey())
        encrypted = cipher.encrypt(text.encode())

        # Save the encrypted text to files
        with open("encrypted.txt", "wb") as f:
            f.write(encrypted)

        # Show a message box with the file paths
        msg = QMessageBox()
        msg.setWindowTitle("Encryption Successful")
        msg.setText(f"The text has been encrypted and saved to encrypted.txt.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


    def decrypt_text(self):
        # Get the filename to decrypt
        filename, _ = QFileDialog.getOpenFileName(self, "Choose a file to decrypt", ".", "Text files (*.txt)")

        # Open a file dialog box to select the decryption key
        keypath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a private key file")

        # Load the encryption key
        with open(keypath, 'rb') as key_file:
            private_key = RSA.import_key(key_file.read())

        # Load the encrypted text
        with open(filename, "rb") as f:
            encrypted = f.read()

        # Decrypt the text using PKCS1_OAEP
        cipher = PKCS1_OAEP.new(private_key)
        decrypted = cipher.decrypt(encrypted)

        # Set the decrypted text in the input text box
        self.input.setPlainText(decrypted.decode('utf-8'))

        # Show a message box
        msg = QMessageBox()
        msg.setWindowTitle("Decryption Successful")
        msg.setText(f"The file {filename} has been decrypted and loaded into the input text box.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
    def cancel(self):
        # Close the window
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rsa_app = RSAApp()
    sys.exit(app.exec_())
