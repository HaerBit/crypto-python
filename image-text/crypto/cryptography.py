from tkinter import Tk, Button, Text, filedialog, StringVar, Entry, Label
from PIL import Image, ImageTk
import numpy as np
import cv2
class ImageCrypt:
    def __init__(self, master):
        self.master = master
        self.ref_path = ""
        self.crypt_path = ""
        self.text_path = ""
        self.stepP1_var = StringVar()
        self.stepP1_var.set("454")

        self.load_ref_button = Button(master, text="LOAD REFERENCE IMAGE", command=self.load_ref)
        self.load_ref_button.pack()

        self.load_crypt_text_button = Button(master, text="LOAD TEXT", command=self.load_crypt_text)
        self.load_crypt_text_button.pack()

        self.encrypt_button = Button(master, text="ENCRYPT AND SAVE", command=self.encrypt)
        self.encrypt_button.pack()

        self.load_crypt_button = Button(master, text="LOAD CRYPT IMAGE", command=self.load_crypt)
        self.load_crypt_button.pack()

        self.decrypt_button = Button(master, text="DECRYPT AND DISPLAY", command=self.decrypt)
        self.decrypt_button.pack()

        self.stepP1_entry = Entry(master, textvariable=self.stepP1_var)
        self.stepP1_entry.pack()

        self.decrypt_text = Text(master)
        self.decrypt_text.pack()

        self.decrypt_text_var = StringVar()
        self.decrypt_text_var.trace_add("write", self.update_decrypt_text)
        self.decrypt_text_var.set("")

    def load_ref(self):
        self.ref_path = filedialog.askopenfilename()

    def load_crypt(self):
        self.crypt_path = filedialog.askopenfilename()

    def load_crypt_text(self):
        self.text_path = filedialog.askopenfilename()

    def encrypt(self):
        global PS
        if len(self.ref_path) != 0 and len(self.text_path) != 0:
            imageCrypt = cv2.imread(self.ref_path, cv2.IMREAD_COLOR)
            with open(self.text_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            lines[0]= '-' + lines[0]
            imgSize = imageCrypt.shape[0] * imageCrypt.shape[1]
            textSize = sum(len(line) for line in lines)+1
            if textSize == 0:
                return
            print(lines)
            pixStep = imgSize // textSize
            PS = pixStep
            print(PS)
            thisPix = 1
            imageCrypt[0] += pixStep

            for line in lines:
                for char in line:
                    thisChar = ord(char)
                    if thisChar > 1000:
                        thisChar -= 800
                    if thisChar > pixStep:
                        whole = thisChar // (pixStep - 1)
                        left = thisChar % (pixStep - 1)
                        for k in range(pixStep - 1):
                            row, col = divmod(thisPix + k, imageCrypt.shape[1])
                            imageCrypt[row, col] += whole
                        row, col = divmod(thisPix + pixStep - 1, imageCrypt.shape[1])
                        imageCrypt[row, col] += left
                    else:
                        for k in range(thisChar):
                            row, col = divmod(thisPix + k, imageCrypt.shape[1])
                            imageCrypt[row, col] += 1
                    thisPix += pixStep
                    if thisPix + pixStep > imgSize:
                        break
            cv2.imwrite("crypt_image.bmp", imageCrypt)

            self.decrypt_text_var.set(f"Шаг пикселя: {PS}")
            self.decrypt_text.delete(1.0, "end")
            self.decrypt_text.insert("end", self.decrypt_text_var.get())
        else:
            print("not selected")

    def decrypt(self):
        if len(self.ref_path) != 0 and len(self.crypt_path) != 0:
            imageRef = cv2.imread(self.ref_path, cv2.IMREAD_COLOR)
            imageCrypt = cv2.imread(self.crypt_path, cv2.IMREAD_COLOR)
            imgSize = imageCrypt.shape[0] * imageCrypt.shape[1]
            decryptText = ""
            thisPix = 1
            pixStep = int(self.stepP1_var.get())
            while True:
                thisChar = 0
                for i in range(pixStep):
                    row, col = divmod(thisPix + i, imageCrypt.shape[1])
                    thisChar += imageCrypt[row, col, 0] - imageRef[row, col, 0]
                if thisChar == 0:
                    break
                if thisChar > 200:
                    thisChar += 800
                decryptText += chr(thisChar)
                print('thisPix-de', thisPix)
                thisPix += pixStep
                if thisPix + pixStep > imgSize:
                    break
            self.decrypt_text_var.set(decryptText[1:])
            with open("decrypt_text.txt", "w",encoding='utf-8') as file:
                file.write(decryptText[0:])
        else:
            print("not selected")

    def update_decrypt_text(self, *args):
        self.decrypt_text.delete(1.0, "end")
        self.decrypt_text.insert("end", self.decrypt_text_var.get())

def main():
    root = Tk()
    my_gui = ImageCrypt(root)
    root.mainloop()

if __name__ == "__main__":
    main()