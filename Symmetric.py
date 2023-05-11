import os
from PyQt5 import QtWidgets, QtGui, QtCore
from cryptography.fernet import Fernet

class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Encryption/Decryption Tool")
        self.resize(300, 150)

        self.label = QtWidgets.QLabel("Select an operation to perform:")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.encrypt_button = QtWidgets.QPushButton("Encrypt File", self)
        self.decrypt_button = QtWidgets.QPushButton("Decrypt File", self)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.encrypt_button)
        self.vbox.addWidget(self.decrypt_button)
        self.setLayout(self.vbox)

        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.decrypt_button.clicked.connect(self.decrypt_file)

    def encrypt_file(self):
        # Open a file dialog box to select the file to encrypt
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file to encrypt")

        # Generate a new encryption key
        key = Fernet.generate_key()

        # Write the key to a file named "key.key" in the same directory as the encrypted file
        keypath = os.path.join(os.path.dirname(filepath), "key.key")
        with open(keypath, 'wb') as key_file:
            key_file.write(key)

        # Encrypt the file contents using the key
        with open(filepath, 'rb') as file:
            original = file.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(original)

        # Write the encrypted contents back to the same file
        with open(filepath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        # Display a message to the user indicating the encryption was successful
        QtWidgets.QMessageBox.information(self, "Encryption Complete", "File encrypted successfully!")

    def decrypt_file(self):
        # Open a file dialog box to select the file to decrypt
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select file to decrypt")

        # Open a file dialog box to select the decryption key
        keypath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select a decryption key file")

        # Load the encryption key
        with open(keypath, 'rb') as key_file:
            key = key_file.read()

        # Decrypt the file contents using the key
        with open(filepath, 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted)

        # Write the decrypted contents back to the same file
        with open(filepath, 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        # Display a message to the user indicating the decryption was successful
        QtWidgets.QMessageBox.information(self, "Decryption Complete", "File decrypted successfully!")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = AppWindow()
    window.show()
    app.exec_()
