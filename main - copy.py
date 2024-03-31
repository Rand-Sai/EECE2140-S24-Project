import qrcode
import cv2
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import threading

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("QR Code Application")
        
        tk.Label(self.root, text="Welcome to the QR Code Application").pack(pady=20)
        
        tk.Button(self.root, text="Generate QR Code", command=self.generate_qr_code).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="Analyze QR Code", command=self.analyze_qr_code).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="Scan QR Code with Camera", command=self.scan_qr_code).pack(fill=tk.X, padx=50, pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(fill=tk.X, padx=50, pady=5)

    def generate_qr_code(self):
        url = simpledialog.askstring("Content Input", "Enter URL for QR code:")
        if url:
            # Ask for the file name (optional)
            file_name = simpledialog.askstring("File Name", "Enter file name (optional):")
            
            # Ask for the QR code color
            color = simpledialog.askstring("Color", "Enter QR code color (default is black):")
            color = color if color else "black" 

            qr_generator = QRCodeGenerator()
            img_name = qr_generator.generate_qr_code(url, name=file_name, color=color)
            messagebox.showinfo("QR Code Generated", f"QR code generated successfully as {img_name}")

    def analyze_qr_code(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            qr_analyzer = QRCodeAnalyzer()
            data = qr_analyzer.image_decode(file_path)
            messagebox.showinfo("QR Code Analysis", f"Info stored in QR code: \n{data}")

    def scan_qr_code(self):
        threading.Thread(target=self._scan_qr_code_thread, daemon=True).start()

    def _scan_qr_code_thread(self):
        qr_scanner = QRCodeScanner()
        data = qr_scanner.camera_decode()
        if data:
            messagebox.showinfo("QR Code Scan", f"QR code detected: data: {data}")

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
        if name is None:
            img_name = url.replace("://", "_").replace("/", "_") + ".png"
        else:
            img_name = str(name) + ".png"
        img.save(img_name)
        return img_name

class QRCodeAnalyzer:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def image_decode(self, image):
        img = cv2.imread(image)
        data, bbox, _ = self.detector.detectAndDecode(img)
        if bbox is not None and data:
            return data
        return "No QR code found."

class QRCodeScanner(QRCodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        # Check if the camera is opened successfully
        if not self.cap.isOpened():
            self.cap = None

    def camera_decode(self):
        if self.cap is None:
            messagebox.showerror("Camera Error", "Unable to access the camera device.")
            return "Camera not found."
        
        count = 0
        while count < 1:
            _, img = self.cap.read()
            data, bbox, _ = self.detector.detectAndDecode(img)
            if bbox is not None and data:
                self.cap.release()
                cv2.destroyAllWindows()
                return data
        self.cap.release()
        cv2.destroyAllWindows()
        return "No QR code detected."

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.geometry('500x250')
    root.resizable(False, False)
    root.mainloop()
