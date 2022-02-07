from sys import argv, exit
from os import remove as destroy
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from requests import get as extract


class MapWindow(QMainWindow):
    def __init__(self):
        super(MapWindow, self).__init__()
        uic.loadUi('v1.1.ui', self)
        self.center = '37.530117,55.805377'
        self.size = '0.00035,0.00035'
        self.setWindowTitle('Показ карты v1.2')
        self.set_picture()

    def set_picture(self):
        map_generator(self.center, self.size)
        image = Image.open('map.jpg')
        image = image.resize((1070, 850))
        self.MapDisplay.setPixmap(QPixmap.fromImage(ImageQt(image)))

    def keyPressEvent(self, thing):
        if thing.key() == Qt.Key_PageUp and float(self.size.split(',')[0]) < 50:
            self.size = ','.join(list(map(lambda x: str(float(x) * 2), self.size.split(','))))
            self.set_picture()
        if thing.key() == Qt.Key_PageDown and float(self.size.split(',')[0]) > 0.00035:
            self.size = ','.join(list(map(lambda x: str(float(x) / 2), self.size.split(','))))
            self.set_picture()
        if thing.key() == Qt.Key_Up and float(self.center.split(',')[1]) < 90:
            self.center = ','.join([self.center.split(',')[0], str(float(self.center.split(',')[1]) + 0.0006)])
            self.set_picture()
        if thing.key() == Qt.Key_Down and -90 < float(self.center.split(',')[1]):
            self.center = ','.join([self.center.split(',')[0], str(float(self.center.split(',')[1]) - 0.0006)])
            self.set_picture()
        if thing.key() == Qt.Key_Right and float(self.center.split(',')[0]) < 180:
            self.center = ','.join([str(float(self.center.split(',')[0]) + 0.0006), self.center.split(',')[1]])
            self.set_picture()
        if thing.key() == Qt.Key_Left and -180 < float(self.center.split(',')[0]):
            self.center = ','.join([str(float(self.center.split(',')[0]) - 0.0006), self.center.split(',')[1]])
            self.set_picture()


def map_generator(center, size):
    map_params = {'ll': center, 'spn': size, 'l': 'map'}
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = extract(map_api_server, params=map_params)
    map_file = 'map.jpg'
    with open(map_file, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    app = QApplication(argv)
    window = MapWindow()
    window.show()
    destroy('map.jpg')
    exit(app.exec())
