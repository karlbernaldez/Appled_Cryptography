import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Encryption and Hashing'
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)

        # Center the window on the screen
        self.center()

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons
        btn_symmetric = QPushButton('Symmetric Encryption', self)
        btn_symmetric.clicked.connect(lambda: subprocess.call(['python', 'Symmetric.py']))
        layout.addWidget(btn_symmetric)

        btn_asymmetric = QPushButton('Asymmetric Encryption', self)
        btn_asymmetric.clicked.connect(lambda: subprocess.call(['python', 'Asymmetric.py']))
        layout.addWidget(btn_asymmetric)

        btn_hashing = QPushButton('Hashing', self)
        btn_hashing.clicked.connect(lambda: subprocess.call(['python', 'Hashing.py']))
        layout.addWidget(btn_hashing)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
