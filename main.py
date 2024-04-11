import sys
import qrcode
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QColorDialog, QFileDialog, QInputDialog, QHBoxLayout, QLineEdit, QDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QClipboard

class QRCodeGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    def generate_qr_code(self, url, name=None, color="black"):
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)

        img = self.qr.make_image(fill_color=color, back_color="white")
        img_name = f"{name}" if name else "qr_code.png"
        img.save(img_name)
        return f"QR code generated successfully as {img_name}"

class QRCodeAnalyzer:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def image_decode(self, image):
        img = cv2.imread(image)
        data, bbox, _ = self.detector.detectAndDecode(img)
        if bbox is not None and data:
            return data
        else:
            return "No QR code detected"

class QRCodeScanner(QRCodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.cap = None

    def camera_decode(self):
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return "ERR"

        _, img = self.cap.read()
        data, bbox, _ = self.detector.detectAndDecode(img)
        if bbox is not None and data:
            result = "[+] QR code detected: data: " + data
        else:
            result = "No QR code detected"
        
        self.cap.release()
        self.cap = None
        cv2.destroyAllWindows()
        return result
    
class ResultDialog(QDialog):
    def __init__(self, parent=None):
        super(ResultDialog, self).__init__(parent)
        self.setWindowTitle('QR Code Analysis Result')
        self.setGeometry(380, 340, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.resultLineEdit = QLineEdit(self)
        self.resultLineEdit.setReadOnly(True) 
        layout.addWidget(self.resultLineEdit)

        self.copyButton = QPushButton('Copy Result', self)
        self.copyButton.clicked.connect(self.copyResult)
        layout.addWidget(self.copyButton)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.close) 
        layout.addWidget(self.exitButton)

        self.setLayout(layout)

    def setResult(self, result):
        self.resultLineEdit.setText(result) 

    def copyResult(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.resultLineEdit.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        #CSS format sheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }

            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                margin: 10px;
            }

            QPushButton:hover {
                background-color: #0053a4;
            }

            QPushButton:pressed {
                background-color: #00397a;
            }

            QLabel {
                color: #2e2e2e;
                font-size: 18px;
            }
        """)

        # Initialize other components...
        self.originalGreeting = 'Welcome to the QR Code APP'
        self.greeting.setText(self.originalGreeting)
        
        self.qr_generator = QRCodeGenerator()
        self.qr_scanner = QRCodeScanner()
        self.qr_analyzer = QRCodeAnalyzer()

    def resetGreeting(self):
        self.greeting.setText(self.originalGreeting)

    def displayMessage(self, message):
        self.greeting.setText(message)
        QTimer.singleShot(3000, self.resetGreeting)

    def initUI(self):
        self.setWindowTitle('QR Code Application')
        self.setGeometry(100, 100, 600, 400)
        
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        mainLayout = QHBoxLayout()

        self.setWindowTitle('QR Code Application')
        self.setGeometry(200, 200, 700, 400)  # Set initial size and position
        
        self.setFixedSize(self.size())
        
        # Text on the left
        self.greeting = QLabel('Welcome to the QR Code Application!', self)
        self.greeting.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.greeting, 1)  # The second argument is the stretch factor
        self.greeting.setWordWrap(True)  # Enable word-wrap for the greeting text
        self.greeting.setFixedWidth(250)
        font = QFont("Arial", 16, QFont.Bold)
        self.greeting.setFont(font)
        
        # Buttons on the right
        buttonsLayout = QVBoxLayout()
        self.generateButton = QPushButton('Generate QR Code(G)', self)
        self.generateButton.clicked.connect(self.generateQR)
        buttonsLayout.addWidget(self.generateButton)
        
        self.scanButton = QPushButton('Scan QR Code(S)', self)
        self.scanButton.clicked.connect(self.scanQR)
        buttonsLayout.addWidget(self.scanButton)
        
        self.analyzeButton = QPushButton('Analyze QR Code(A)', self)
        self.analyzeButton.clicked.connect(self.analyzeQR)
        buttonsLayout.addWidget(self.analyzeButton)
        
        self.exitButton = QPushButton('Exit(E)', self)
        self.exitButton.clicked.connect(self.close)
        buttonsLayout.addWidget(self.exitButton)

        self.generateButton.setFixedSize(300, 75)  # Set fixed size
        self.scanButton.setFixedSize(300, 75)
        self.analyzeButton.setFixedSize(300, 75)
        self.exitButton.setFixedSize(300, 75)

        buttonFont = QFont("Arial", 14) 
        self.generateButton.setFont(buttonFont) 
        self.scanButton.setFont(buttonFont)
        self.analyzeButton.setFont(buttonFont)
        self.exitButton.setFont(buttonFont)

        mainLayout.addLayout(buttonsLayout, 1)  # Adding the buttons layout to the main layout with a stretch factor
        
        self.centralWidget.setLayout(mainLayout)

    def generateQR(self):
        text, ok = QInputDialog.getText(self, 'QR Code Content', 'Enter the content for the QR Code:')
        if ok and text:
            color = QColorDialog.getColor(Qt.black, self).name()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png);;All Files (*)")
            if fileName:
                result = self.qr_generator.generate_qr_code(text, fileName, color)
                self.displayMessage(result)  # Use displayMessage instead

    def scanQR(self):
        result = self.qr_scanner.camera_decode()

        if "ERR" in result:

            self.displayMessage("Camera device not found or cannot be invoked")
        elif"[+] QR code detected: data: " in result:

            self.displayMessage('Analyze completed')
            self.resultDialog = ResultDialog(self) 
            self.resultDialog.setResult(result.replace("[+] QR code detected: data: ", ""))
            self.resultDialog.exec_()
        else:
            self.displayMessage("No QR code detected")

    def analyzeQR(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open QR Code", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)")
        if fileName:
            result = self.qr_analyzer.image_decode(fileName)
            if "No QR code detected" not in result:

                self.displayMessage('Analyze completed')
                self.resultDialog = ResultDialog(self) 
                self.resultDialog.setResult(result)  
                self.resultDialog.exec_() 
            else:
                self.displayMessage("No QR code detected") 

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QDialog {
            font-family: 'Arial';
            font-size: 12px;
        }
        
        QLineEdit {
            border: 1px solid #ccc;
            padding: 5px;
            border-radius: 6px;
        }
        """)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()