import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import numpy as np
import os
from PIL import Image 
from matplotlib import pyplot as plt

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        widget = QtWidgets.QWidget()

        v1_box = QtWidgets.QVBoxLayout()
        h1_box = QtWidgets.QHBoxLayout()
        v2_box = QtWidgets.QVBoxLayout()
        v3_box = QtWidgets.QVBoxLayout()

        self.onislem_combo = QtWidgets.QComboBox(self)
        self.onislem_combo.addItem("Önişlem Menüsü",self)
        self.onislem_combo.addItem("Gri Seviye Dönüştürme",self)
        self.onislem_combo.addItem("İstenilen Bölgenin Alınması",self)
        self.onislem_combo.addItem("Histogram Oluşturma",self)
        

        self.filtreleme_combo = QtWidgets.QComboBox(self)
        self.filtreleme_combo.addItem("Filtreleme Menüsü",self)
        self.filtreleme_combo.addItem("Bulanıklaştırma",self)
        self.filtreleme_combo.addItem("Keskinleştirme",self)
        self.filtreleme_combo.addItem("Kenar Bulma",self)      
        

        self.morfolojik_combo = QtWidgets.QComboBox(self)
        self.morfolojik_combo.addItem("Morfolojik İşlemler",self)
        self.morfolojik_combo.addItem("Genişletme",self)
        self.morfolojik_combo.addItem("Erozyon",self)

        self.segmentasyon_combo = QtWidgets.QComboBox(self)
        self.segmentasyon_combo.addItem("Segmentasyon Menüsü",self)
        self.segmentasyon_combo.addItem("4'lü Komşuluk ile Nesne Bulma",self)
        self.segmentasyon_combo.addItem("Gri Seviye Resimde Nesne Bulma",self)
        self.segmentasyon_combo.addItem("Renkli Resimde Nesne Bulma",self)
        

        self.kaydet_combo = QtWidgets.QComboBox(self)
        self.kaydet_combo.addItem("Resim Formatı",self)
        self.kaydet_combo.addItem(".jpg",self)
        self.kaydet_combo.addItem(".bmp",self)
        self.kaydet_combo.addItem(".png",self) 
        
        
        self.imageUploadButton = QtWidgets.QPushButton("Resim Seçin")
        v1_box.addWidget(self.imageUploadButton)
        v1_box.addWidget(self.onislem_combo)
        v1_box.addWidget(self.filtreleme_combo)
        v1_box.addWidget(self.morfolojik_combo)
        v1_box.addWidget(self.segmentasyon_combo) 

        h1_box.addStretch()

        self.label = QtWidgets.QLabel()
        v2_box.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)

        self.imageDownloadButton = QtWidgets.QPushButton("Kaydet")
        v3_box.addStretch()
        v3_box.addWidget(self.kaydet_combo) 
        v3_box.addWidget(self.imageDownloadButton)


        h1_box.addLayout(v1_box)
        h1_box.addLayout(v2_box)
        h1_box.addLayout(v3_box)
        h1_box.addStretch()
        

        self.imageUploadButton.clicked.connect(self.imageUpload)
        self.onislem_combo.currentTextChanged.connect(self.onIsleme)
        self.filtreleme_combo.currentTextChanged.connect(self.filtreleme)
        self.morfolojik_combo.currentTextChanged.connect(self.morfolojik)
        self.kaydet_combo.currentTextChanged.connect(self.kaydet)
        
        widget.setLayout(h1_box)
        self.setCentralWidget(widget)
        self.setGeometry(100,100,200,200)
        self.setWindowTitle('Görüntü İşleme Proje')
        self.show()
        
        self.flag=0
        self.redPix = 0
        self.greenPix = 0
        self.bluePix = 0
        
    def imageUpload(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            'd:\\',"Image files (*.jpg *.gif *.png)")
        self.image = fname[0]
        self.img_deneme = fname[0]
        if len(fname[0]) > 0:
            self.label.setPixmap(QPixmap(fname[0]))


    def onIsleme(self):
        if self.onislem_combo.currentText() == "Gri Seviye Dönüştürme":
            img =cv2.imread(self.image)
            h = img.shape[0]
            w = img.shape[1]
            img2 = np.zeros((h,w,1), np.uint8)
            
            for i in range(h):
                for j in range(w):
                    img2[i,j]= int(((img[i,j][0]*0.2989)+(img[i,j][1]*0.5870)+(img[i,j][2]*0.1140)))
                    
            cv2.imwrite('output.png',img2)
            self.image=img2
            self.label.setPixmap(QPixmap('output.png'))
            self.flag=1

        
        if self.onislem_combo.currentText() == "İstenilen Bölgenin Alınması":
            img = cv2.imread('output.png')
            roi = cv2.selectROI("Alan secip ESC'ye basiniz.",img,False)
            imCrop = img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
            cv2.imshow("Goruntu", imCrop)
            cv2.imwrite("output.png",imCrop)
            img_crop = cv2.imread("output.png")
            self.image=img_crop
            self.label.setPixmap(QPixmap('output.png'))
            self.flag=2

       
        
        if self.onislem_combo.currentText() == "Histogram Oluşturma":
            if self.flag == 0:
                img2 = cv2.imread(self.img_deneme)
            if self.flag == 1:
                img2 = cv2.imread('output.png')
            if self.flag == 2:
                img2 = cv2.imread('output.png')    
            h,w = img2.shape[:2]
            y = np.zeros((256), np.uint8)
            for i in range(0,h):
               for j in range(0,w):
                  y[img2[i,j]] += 1
            x = np.arange(0,256)
            plt.bar(x,y,align="center")
            plt.savefig('histogram.png')
            img2 = cv2.imread("histogram.png")
            self.image=img2
            self.label.setPixmap(QPixmap('histogram.png'))
    
    
    def filtreleme(self):
        def average(img,x,y,blurfactor):
            rtotal = gtotal = btotal = 0
            for x2 in range(x-blurfactor,x+blurfactor+1):
                for y2 in range(y-blurfactor,y+blurfactor+1):
                    r,g,b = img.getpixel((x2,y2))
                    rtotal = rtotal + r
                    gtotal = gtotal + g
                    btotal = btotal + b
            rtotal = rtotal // ((blurfactor * 2 +1)**2)
            gtotal = gtotal // ((blurfactor * 2 +1)**2)
            btotal = btotal // ((blurfactor * 2 +1)**2)
            return (rtotal, gtotal, btotal)
    
        if self.filtreleme_combo.currentText() == "Bulanıklaştırma":
            img = Image.open("output.png")
            w = img.size[0]
            h = img.size[1]
            img2 = Image.new("RGB",(w,h),(0,0,0))
            
            for x in range(3,w-3):
                for y in range(3,h-3):
                    r,g,b = img.getpixel((x,y))
                    r2,g2,b2 = average(img,x,y,3)
                    img2.putpixel((x,y),(r2,g2,b2))
                    
            img2 = img2.save("output.png")
            img2 = cv2.imread("output.png")
            self.image = img2
            self.label.setPixmap(QPixmap('output.png'))
            
    def morfolojik(self):
        if self.morfolojik_combo.currentText() == "Genişletme":
             img1= cv2.imread('output.png',0)
            m,n= img1.shape
            k=5
            SE= np.ones((k,k), dtype=np.uint8)
            constant= (k-1)//2
            imgErode= np.zeros((m,n), dtype=np.uint8)
            for i in range(constant, m-constant):
              for j in range(constant,n-constant):
                temp= img1[i-constant:i+constant+1, j-constant:j+constant+1]
                product= temp*SE
                imgErode[i,j]= np.min(product)
            cv2.imwrite("output.png", imgErode)
            img2 = cv2.imread("output.png")
            self.image = img2
            self.label.setPixmap(QPixmap('output.png'))
        
        if self.morfolojik_combo.currentText() == "Erozyon":
            img2= cv2.imread('output.png',0)
            p,q= img2.shape
            imgDilate= np.zeros((p,q), dtype=np.uint8)
            SED= np.array([[0,1,0], [1,1,1],[0,1,0]])
            constant1=1
            for i in range(constant1, p-constant1):
              for j in range(constant1,q-constant1):
                temp= img2[i-constant1:i+constant1+1, j-constant1:j+constant1+1]
                product= temp*SED
                imgDilate[i,j]= np.max(product)
            cv2.imwrite("output.png", imgDilate)
            img2 = cv2.imread("output.png")
            self.image = img2
            self.label.setPixmap(QPixmap('output.png'))

            
    def kaydet(self):
        if self.kaydet_combo.currentText() == ".jpg":
            img = cv2.imread('output.png',0)
            dosyaAdi = "output.jpg"
            cv2.imwrite(dosyaAdi,img)
        
        if self.kaydet_combo.currentText() == ".bmp":
            img = cv2.imread('output.png',0)
            dosyaAdi = "output.bmp"
            cv2.imwrite(dosyaAdi,img)
        
        if self.kaydet_combo.currentText() == ".png":
            img = cv2.imread('output.png',0)
            dosyaAdi = "output.png"
            cv2.imwrite(dosyaAdi,img)

          
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()