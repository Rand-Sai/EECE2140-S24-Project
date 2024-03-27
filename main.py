#Semester Project - QR Code generator
import qrcode
import cv2

class QRCodeGenerator:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    def generate_qr_code(self, url, name=None, color = "black"):
        self.qr.clear()
        self.qr.add_data(url)
        self.qr.make(fit=True)

        
        # Create an image from the QR Code instance
        img = self.qr.make_image(fill_color=color, back_color="white")

        # Save the image with a name based on the URL
        if name == None:
            img_name = url.replace("://", "_").replace("/", "_") + ".png"
        else:
            img_name = str(name) + ".png"
        img.save(img_name)
        print(f"QR code generated successfully as {img_name}")

class QRCodeAnalyzer:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def image_decode(self, image):
        img = cv2.imread(image)
        data, bbox, _ = self.detector.detectAndDecode(img)
        if bbox is not None:
                if data:
                    print("Info stored in QR code: \n" + data)

class QRCodeScanner(QRCodeAnalyzer):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        super().__init__()

    def camera_decode(self):
        count = 0
        while count<1:
            _, img = self.cap.read()
            data, bbox, _ = self.detector.detectAndDecode(img)
            if bbox is not None:
                if data:
                    print("[+] QR code detected: data:", data)
                    count += 1

        self.cap.release()
        cv2.destroyAllWindows()
        
#main function
def main():
    QRG = QRCodeGenerator()
    QRS = QRCodeScanner()
    QRA = QRCodeAnalyzer()
    #Greet user
    print('Hello!\n')
    #url1 = input("Enter the url of the website or any text: \n")
    #name1 = input("Enter the name of this QRcode image or leave blank: \n")
    #color1 = input("Enter the color of this QRcode image or leave blank: \n")
    #QRG.generate_qr_code(url1, name1, color1)
    #QRS.camera_decode()
    #QRA.image_decode('git.png')
#----------------------------------------------
main()