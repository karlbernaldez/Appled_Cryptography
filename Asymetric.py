import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.label = QLabel("Enter text to encrypt:")
        self.text_box = QLineEdit()
        self.generate_button = QPushButton("Generate Key Pair")
        self.encrypt_button = QPushButton("Encrypt")
        self.decrypt_button = QPushButton("Decrypt")

        self.label.setFont(QFont("Arial", 12))
        self.text_box.setPlaceholderText("Enter text to encrypt")
        self.generate_button.clicked.connect(self.generate_key_pair)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_box)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.encrypt_button)
        self.layout.addWidget(self.decrypt_button)

        self.setLayout(self.layout)

    def generate_key_pair(self):
        # Generate an RSA key pair.
        key = RSA.generate(2048)

        # Get the public key.
        public_key = key.publickey()

        # Save the public key to a file.
        with open("public_key.pem", "wb") as f:
            f.write(public_key.export_key("PEM"))

        # Display a message to the user.
        QMessageBox.information(self, "Success", "Key pair generated successfully.")

    def encrypt(self):
        # Get the text to encrypt from the text box.
        text = self.text_box.text()

        # Get the public key from a file.
        with open("public_key.pem", "rb") as f:
            public_key = RSA.import_key(f.read())

        # Encrypt the text using the public key.
        encrypted_text = PKCS1_OAEP.new(public_key).encrypt(text.encode("utf-8"))

        # Decode the encrypted text to a string.
        encrypted_text = b64encode(encrypted_text).decode("utf-8")

        # Display the encrypted text in the label.
        self.label.setText("Encrypted text: " + encrypted_text)

        # Save the encrypted text to a file.
        with open("encrypted_text.txt", "w") as f:
            f.write(encrypted_text)

    def decrypt(self):
        # Get the encrypted text from the text box.
        encrypted_text = self.text_box.text()

        # Get the private key from a file.
        with open("private_key.pem", "rb") as f:
            private_key = RSA.import_key(f.read())

        # Decrypt the text using the private key.
        decrypted_text = PKCS1_OAEP.new(private_key).decrypt(encrypted_text.encode("utf-8"))

        # Decode the decrypted text to a string.
        decrypted_text = b64decode(decrypted_text).decode("utf-8")

        # Display the decrypted text in the label.
        self.label.setText("Decrypted text: " + decrypted_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
