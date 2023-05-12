import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget, QLabel, QFileDialog


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Encryption and Hashing'
        self.width = 500
        self.height = 170
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # Center the window on the screen
        self.center()

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons
        btn_symmetric = QPushButton('Symmetric Encryption(Fernet-AES based)', self)
        btn_symmetric.clicked.connect(lambda: subprocess.call(['python', 'Symmetric.py']))
        layout.addWidget(btn_symmetric)

        btn_asymmetric = QPushButton('Asymmetric Encryption(RSA)', self)
        btn_asymmetric.clicked.connect(lambda: subprocess.call(['python', 'Asymmetric.py']))
        layout.addWidget(btn_asymmetric)

        btn_hashing = QPushButton('Hashing(SHA-256)', self)
        btn_hashing.clicked.connect(lambda: subprocess.call(['python', 'Hashing.py']))
        layout.addWidget(btn_hashing)
        
        btn_verify = QPushButton('Verify SHA-256', self)
        btn_verify.clicked.connect(self.verify)
        layout.addWidget(btn_verify)

        # Add a label to display the hash verification result
        self.lbl_result = QLabel()
        layout.addWidget(self.lbl_result)

        # Add the layout to the window
        self.setLayout(layout)

        self.show()

    def center(self):
        # Get the dimensions of the screen
        screen = QDesktopWidget().screenGeometry()
        # Calculate the center of the screen
        center_x = int((screen.width() - self.width) / 2)
        center_y = int((screen.height() - self.height) / 2)
        # Set the position of the window
        self.move(center_x, center_y)

    def verify(self):
        # Get the file paths to the hashed values
        file_path1, _ = QFileDialog.getOpenFileName(self, 'Open Hash File 1', '', 'Hash files (*.txt)')
        file_path2, _ = QFileDialog.getOpenFileName(self, 'Open Hash File 2', '', 'Hash files (*.txt)')

        if not file_path1 or not file_path2:
            # Return if any file path is empty
            return

        # Read the hashed values from the files
        with open(file_path1, 'rb') as file:
            hash1 = file.read()
        with open(file_path2, 'rb') as file:
            hash2 = file.read()

        # Compare the hashed values
        if hash1 == hash2:
            self.lbl_result.setText('Hashes match!')
        else:
            self.lbl_result.setText('Hashes do not match.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
