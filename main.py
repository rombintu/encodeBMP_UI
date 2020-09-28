import os

import EnDeCode
import form
import sys

from PyQt5 import QtWidgets


class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)

        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("4")
        self.comboBox.addItem("8")

        self.btn1.clicked.connect(self.chooseSecret)
        self.btn2.clicked.connect(self.chooseImage)
        self.btn3.clicked.connect(self.choosePath)


        self.pushButton.clicked.connect(self.hider)
        self.pushButton_2.clicked.connect(self.finder)

    def chooseSecret(self):
        secretFile = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбери файл')[0]
        self.lineEdit.setText(secretFile)
    def chooseImage(self):
        imageFile = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбери картинку', os.path.abspath(os.curdir), '*.bmp')[0]
        self.lineEdit_2.setText(imageFile)
    def choosePath(self):
        pathDir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Куда сохранить', os.path.abspath(os.curdir))
        self.lineEdit_3.setText(pathDir)

    def hider(self):
        secretFile = self.lineEdit.text()
        imageFile = self.lineEdit_2.text()
        pathDir = self.lineEdit_3.text()
        level = int(self.comboBox.currentText())

        try:
            secret_size = os.stat(secretFile).st_size
            img_size = os.stat(imageFile).st_size
        except:
            warningWindow = QtWidgets.QErrorMessage(self)
            warningWindow.showMessage('Файлы не выбраны')
            return False

        warningWindow = QtWidgets.QErrorMessage(self)
        warningWindow.showMessage(f'Размер секрета {round(secret_size/1024)} Kб.\nРазмер картинки {round(img_size/1024)} Kб.\n Будет занято {round(secret_size*100/img_size)}% картики')


        if secret_size > img_size * level / 8 - 54:
            warningWindow = QtWidgets.QErrorMessage(self)
            warningWindow.showMessage('Секрет слишком большой')
            return False

        # Open all files
        secret = open(secretFile, 'r')
        origin_img = open(imageFile, 'rb')
        encode_img = open(pathDir + '/encode.bmp', 'wb')

        # Читаем первые 54 байта, где хранятся мета-данные и заголовки
        first54byte = origin_img.read(54)
        # Записываем в новую картинку
        encode_img.write(first54byte)

        # Get MASKs
        secretMask, imgMask = EnDeCode.createMask(level)

        while True:
            # Читаем по одному байту секрета
            symbol = secret.read(1)
            # Если секрет закончен, то выходим из цикла
            if not symbol:
                break

            # Преобразование символов в цифры
            symbol = ord(symbol)

            # Для каждой пары битов (если уровень СРЕДНИЙ)
            # В каждом байте размерности от 0 до 8
            # с промежутком выбранного уровня шифрования
            for bytes in range(0, 8, level):
                # use MASK
                imgByte = int.from_bytes(origin_img.read(1), sys.byteorder) & imgMask

                # Получаем количество бит из символа
                # Пример [10][11][01[00] -> [10]110100
                bits = symbol & secretMask
                # Сдвигаем их в конец
                # Пример [10][11][01[00] -> [00][00][00][10] (то есть получаем итоговую маску)
                bits >>= (8 - level)


                # С помощью маски записываем биты в байты изображения
                # Пример:
                # байт изображения - [10][01][11][11]
                # полученая маска секрета [00][00][00][10]
                # Получаем: [10][01][11].[10]
                imgByte |= bits


                # Записываем полученный байт в новую картинку (В байтовом виде)
                encode_img.write(imgByte.to_bytes(1, sys.byteorder))
                # Сдвигаем символ на уровень сжатия, чтобы цеплять оставшиеся биты.
                # Пример: [01][11][10][00] -> [-][11][10][00] -> [11][10][00][00]
                symbol <<= level

        self.lineEdit_4.setText(str(origin_img.tell()))

        # Записываем что осталось
        encode_img.write(origin_img.read())

        ########################
        # Close all files
        secret.close()
        origin_img.close()
        encode_img.close()


    def finder(self):

        imageFile = self.lineEdit_2.text()
        pathDir = self.lineEdit_3.text()
        level = int(self.comboBox.currentText())
        to_read = int(self.lineEdit_4.text())

        # Счетчик просчитанных символов
        countRead = 0

        # Open all Files
        secret = open(pathDir + '/decodeSecret.txt', 'w')
        img_encoded = open(imageFile, 'rb')

        # Пропускаем первые 54 бита
        img_encoded.seek(54)

        # Get MASK for img bytes
        maskList = EnDeCode.createMask(level)
        # Делаем обратную маску, чтобы считывать последние биты
        # Пример: [11][11][11][11] -> [00][00][00][11]
        imgMask = ~maskList[1]

        while countRead < to_read:
            # Начинаем с первого символа
            symbol = 0
            for bits in range(0, 8, level):
                # Также берем последние (нужные) биты
                imgByte = int.from_bytes(img_encoded.read(1), sys.byteorder) & imgMask
                # Сдвигаем влево
                symbol <<= level
                # Помещаем биты на нужную позицию
                symbol |= imgByte


            # Следующий символ
            countRead += 1
            # Записываем символ
            secret.write(chr(symbol))

        # Close all Files
        secret.close()
        img_encoded.close()

        warningWindow = QtWidgets.QErrorMessage(self)
        warningWindow.showMessage('Секрет найден')

# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()
