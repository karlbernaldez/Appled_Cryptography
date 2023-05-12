import sys, os, hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtWidgets import QMessageBox


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SHA-256 Hash Generator")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Enter a string to hash or choose a file to hash:", self)
        self.label.move(20, 20)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 50)
        self.textbox.resize(180, 40)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.move(210, 50)
        self.browse_button.resize(90, 40)
        self.browse_button.clicked.connect(self.browse_file)

        self.button = QPushButton("Generate Hash", self)
        self.button.move(20, 100)
        self.button.resize(120, 40)
        self.button.clicked.connect(self.generate_hash)

        self.result_label = QLabel("", self)
        self.result_label.move(20, 150)
        self.result_label.resize(500, 40)

    def browse_file(self):
        # Open a file dialog to select a file to hash
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Choose File to Hash", "","All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            self.textbox.setText(file_name)

    def generate_hash(self):
        text = self.textbox.text()
        if text:
            # If the text box contains a file name, hash the contents of the file. Otherwise, hash the entered string.
            if os.path.isfile(text):
                with open(text, "rb") as f:
                    contents = f.read()
                    hash_object = hashlib.sha256(contents)
                    hash_hex = hash_object.hexdigest()
                    output_file = text + "_hash.txt"
                    with open(output_file, "w") as outfile:
                        outfile.write(f"SHA-256 Hash of {os.path.basename(text)}: " + hash_hex)
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Hash Generated")
                    msg_box.setText(f"SHA-256 Hash of {os.path.basename(text)} written to file {os.path.basename(output_file)}.")
                    msg_box.exec_()
            else:
                hash_object = hashlib.sha256(text.encode())
                hash_hex = hash_object.hexdigest()
                self.result_label.setText("SHA-256 Hash: " + hash_hex)
                output_file = "hash_output.txt"
                with open(output_file, "w") as outfile:
                    outfile.write("SHA-256 Hash: " + hash_hex)
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Hash Generated")
                msg_box.setText(f"SHA-256 Hash written to file {output_file}.")
                msg_box.exec_()
        else:
            self.result_label.setText("Please enter a string to hash or choose a file to hash.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
