from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QLabel, QDialog, QSlider, \
    QPushButton, QWidget
from PyQt5.QtGui import QFont, QIcon, QImage, QPainter, QPen, QBrush, QPixmap, QPaintDevice, QBitmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image
import sys
import sqlite3
from PyQt5.QtGui import QPixmap


class PhotoRedact(QMainWindow, QtWidgets.QLabel, QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # title = "Paint Application"
        self.index = 0
        top = 400
        left = 400
        width = 800
        height = 600
        self.foto_name = "nach.jpg"
        self.image = Image.open(self.foto_name)
        self.connection = sqlite3.connect("placement_data.db")
        x, y = self.image.size
        self.setWindowTitle('фото_редактор')
        self.pix_map = QtGui.QPixmap()
        self.ab = About(self)
        self.filtrs = regulatorFiltr(self)
        self.regColor = regulatorColor(self)
        self.setGeometry(top, left, width, height)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("Файл")
        brushSize = mainMenu.addMenu("Размер кисти")
        brushColor = mainMenu.addMenu("Цвет кисти")
        editMenu = mainMenu.addMenu("Редактировать изображение")
        AboutMenu = mainMenu.addMenu("Справка")
        # ---Все мини менюшки---#

        openAction = QAction('Открыть', self)
        openAction.triggered.connect(self.openImage)
        fileMenu.addAction(openAction)

        backAction = QAction("Вернуть", self)
        backAction.triggered.connect(self.back)
        fileMenu.addAction(backAction)

        closeAction = QAction('Выход', self)
        closeAction.triggered.connect(self.close)
        fileMenu.addAction(closeAction)
        self.label = QLabel()
        self.setCentralWidget(self.label)

        saveAction = QAction(QIcon("icons/save.png"), "Сохранить", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("icons/clear.png"), "Очистить", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        threepxAction = QAction(QIcon("icons/threepx.png"), "3px", self)
        brushSize.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePixel)

        fivepxAction = QAction(QIcon("icons/fivepx.png"), "5px", self)
        brushSize.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePixel)

        sevenpxAction = QAction(QIcon("icons/sevenpx.png"), "7px", self)
        brushSize.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPixel)

        ninepxAction = QAction(QIcon("icons/ninepx.png"), "9px", self)
        brushSize.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePixel)

        blackAction = QAction(QIcon("icons/black.png"), "Чёрный", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor)

        whitekAction = QAction(QIcon("icons/white.png"), "Белый", self)
        whitekAction.setShortcut("Ctrl+W")
        brushColor.addAction(whitekAction)
        whitekAction.triggered.connect(self.whiteColor)

        redAction = QAction(QIcon("icons/red.png"), "Красный", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.redColor)

        greenAction = QAction(QIcon("icons/green.png"), "Зелёный", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)

        yellowAction = QAction(QIcon("icons/yellow.png"), "Жёлтый", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor)

        # #---Редактирование изображения---#
        # contrastAction = QAction("Контрастность")
        # contrastAction.setShortcut("Ctrl+K")
        # editMenu.addAction(contrastAction)
        # contrastAction.triggered.connect(useFilter)
        #
        # lightAction = QAction("Яркость")
        # contrastAction.setShortcut("Ctrl+I")
        # editMenu.addAction(contrastAction)
        # contrastAction.triggered.connect(useFilter)
        #
        # sharpnessAction = QAction("Резкость")
        # contrastAction.setShortcut("Ctrl+X")
        # editMenu.addAction(contrastAction)
        # contrastAction.triggered.connect(useFiltr)

        contrastAction = QAction("Параметры изображения", self)
        contrastAction.setShortcut("Ctrl+P")
        editMenu.addAction(contrastAction)
        # contrastAction.triggered.connect(self.filtrs.show())

        colorAction = QAction("Настройка цветов", self)
        colorAction.setShortcut("Ctrl+L")
        editMenu.addAction(colorAction)
        colorAction.triggered.connect(lambda: self.ColorsRed())

        aboutAll = QAction("О программе", self)
        colorAction.setShortcut("Ctrl + I")
        AboutMenu.addAction(aboutAll)
        aboutAll.triggered.connect(self.getAbout)

    def getAbout(self):
        self.ab.show()


    def ColorsRed(self):
        self.saveMotion()
        self.regColor.exec()
        self.regColor.prim()
        self.image = Image.open(self.foto_name)
        self.image.save('rezult.jpg')
        pixels = self.image.load()
        x, y = self.image.size
        # for i in range(x):
        #     for j in range(y):
        #         r, g, b = pixels[i, j]
        #         if fl == 1:
        #             pixels[i, j] = r + value - 50, g, b
        #         elif fl == 2:
        #             pixels[i, j] = r, g + value - 50, b
        #         elif fl == 3:
        #             pixels[i, j] = r, g, b + value - 50
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                pixels[i, j] = r + self.regColor.value1 - 50, g + self.regColor.value2 - 50, b + self.regColor.value3 - 50
        self.image.save('rezult_2.jpg')
        self.foto_name = 'rezult_2.jpg'
        self.pix_map = QPixmap.fromImage(QImage('rezult_2.jpg'))
        self.image = Image.open('rezult_2.jpg')
        self.image.save('rezult.jpg')
        self.foto_name = "rezult_2.jpg"
        self.pix_map = QPixmap(self.foto_name)
        self.scale_image()

        scaled = self.pix_map.scaled(self.size(), Qt.KeepAspectRatio)
        self.pix_map = QtGui.QPixmap.fromImage(QtGui.QImage(self.foto_name))

    def openImage(self):
        imagePath, _ = QFileDialog.getOpenFileName()
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)
        self.adjustSize()
        self.foto_name = imagePath

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            # print(self.lastPoint)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # self.saveAction()
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.index += 1

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)

    def back(self):
        pass
        # query = f"""SELECT place.name from place WHERE place.id =={self.index} """
        # res = self.connection.cursor().execute(query).fetchall()

    def clear(self):
        # self.saveAction()
        self.image.fill(Qt.white)
        self.update()
        

    def threePixel(self):
        self.brushSize = 3

    def fivePixel(self):
        self.brushSize = 5

    def sevenPixel(self):
        self.brushSize = 7

    def ninePixel(self):
        self.brushSize = 9

    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def redColor(self):
        self.brushColor = Qt.red

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def scale_image(self):
        if self.pix_map.isNull():
            return
        scaled = self.pix_map.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaled)

    def saveMotion(self):
        pass
        # self.index += 1
        # sname = "tamplates" + str(self.index)
        # query = f"""INSERT INTO place name {sname}"""
        # cur = self.connection.cursor
        # self.image.save(sname)
        # cur.execute(query)


class regulatorFiltr(QDialog):
    def __init__(self, root, **kwargs):
        super().__init__()
        self.main = root
        self.setGeometry(300, 300, 200, 500)
        self.setWindowTitle('регулировка параметров')
        # здесь пишешь слайдер для контраста и тп
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(10, 200, 150, 20)
        self.sld.setValue(50)


class regulatorColor(QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.value1 = 50
        self.value2 = 50
        self.value3 = 50
        self.main = root
        self.setWindowTitle('фото_редактор')
        self.setGeometry(300, 300, 200, 500)
        self.setWindowTitle('регулировка цветов')
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(10, 200, 150, 20)
        self.sld.setValue(50)
        self.sld.valueChanged[int].connect(self.changeValue)

        # -----------------

        self.sld_2 = QSlider(Qt.Horizontal, self)
        self.sld_2.setFocusPolicy(Qt.NoFocus)
        self.sld_2.setGeometry(10, 290, 150, 20)
        self.sld_2.setValue(50)
        self.sld_2.valueChanged[int].connect(self.changeValue_2)

        # -----------------

        self.sld_3 = QSlider(Qt.Horizontal, self)
        self.sld_3.setFocusPolicy(Qt.NoFocus)
        self.sld_3.setGeometry(10, 380, 150, 20)
        self.sld_3.setValue(50)
        self.sld_3.valueChanged[int].connect(self.changeValue_3)

        self.btn_prim_3 = QPushButton('применить', self)
        self.btn_prim_3.resize(150, 50)
        self.btn_prim_3.move(10, 410)
        self.btn_prim_3.clicked.connect(self.prim)

        # -----------------

    def changeValue(self, valuer):
        # im = Image.open(self.foto_name)
        # im.save('rezult.jpg')
        # im = Image.open(self.foto_name)
        # pixels = im.load()
        # x, y = im.size
        # for i in range(x):
        #     for j in range(y):
        #         r, g, b = pixels[i, j]
        #         pixels[i, j] = r + value - 50, g, b
        # im.save('rezult_2.jpg')
        # self.foto_name = 'rezult.jpg'
        # self.pix_map = QPixmap.fromImage(QImage('rezult_2.jpg'))
        # self.scale_image()
        self.value1 = valuer

    def changeValue_2(self, valuer):
        # im = Image.open(self.foto_name)
        # im.save('rezult.jpg')
        # im = Image.open(self.foto_name)
        # pixels = im.load()
        # x, y = im.size
        # for i in range(x):
        #     for j in range(y):
        #         r, g, b = pixels[i, j]
        #         pixels[i, j] = r, g + value - 50, b
        #
        # im.save('rezult_2.jpg')
        # self.foto_name = 'rezult.jpg'
        # self.pix_map = QPixmap.fromImage(QImage('rezult_2.jpg'))
        # self.scale_image()
        self.value2 = valuer
 

    def changeValue_3(self, valuer):
        # im = Image.open(self.foto_name)
        # im.save('rezult.jpg')
        # im = Image.open(self.foto_name)
        # pixels = im.load()
        # x, y = im.size
        # for i in range(x):
        #     for j in range(y):
        #         r, g, b = pixels[i, j]
        #         pixels[i, j] = r, g, b + value - 50
        self.value3 = valuer
 

        # im.save('rezult_2.jpg')
        # self.foto_name = 'rezult.jpg'
        # self.pix_map = QPixmap.fromImage(QImage('rezult_2.jpg'))
        # self.scale_image()

    def prim(self):
        # im = Image.open('rezult_2.jpg')
        # im.save('rezult.jpg')
        # scaled = self.pix_map.scaled(self.size(), Qt.KeepAspectRatio)
        # self.setPixmap(scaled)
        # print(self.value, self.f)
        # print("In {0} years you will be {1} years old!".format(self.value, self.f))
        # regulatorColor.close()
        self.close()

class About(QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.setWindowTitle('О программе')
        self.setGeometry(300, 800, 800, 500)
        self.lbl = QLabel("", self)
        self.lbl.setFont(QFont("Arial", 10))
        self.lbl.setText("Файл - это вкладка функций  в котором вы сможете: \n1)Открыть - открыть свою фотографию для начала редактирования \n \
            2)отменить своё последнее действие \n3)Выход - выход из приложения. Так же вы его можете закрыть нажав на крестик в правом верхнем углу\n \
            4)Сохранить - сохранение фотографии которую вы отредактировали/нарисовали \n\
            5)Очистить - вы очищаете рабочее место, фотографию которую вы открыли \n \
            Размер кисти - вкладка функций которые вы можете выбрать размер кисти: \n\
            Размеры кистей: 3px; 5px; 7px; 9px; \n\
            Цвет кисти - вкладка выбора цвета своей кисти которой вы рисуте. \n\
            Цвета: Чёрный; Белый; Красный; Зелёный; Жёлтый; \n\
            ")
        self.lbl.resize(650, 500)
        self.lbl.move(0, 0)
        self.all = QPushButton('закрыть', self)
        self.all.resize(150, 50)
        self.all.move(20, 410)
        self.all.clicked.connect(lambda : self.close())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    PhotoRedact = PhotoRedact()
    PhotoRedact.show()
    app.exec()
