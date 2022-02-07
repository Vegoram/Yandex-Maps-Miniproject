from sys import argv, exit
from os import remove as destroy
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from requests import get as extract


class MapWindow(QMainWindow):
    def __init__(self, map_name):
        super(MapWindow, self).__init__()
        uic.loadUi('v1.0.ui', self)
        self.setWindowTitle('Показ карты v1.0')
        self.set_picture(map_name)

    def set_picture(self, name):
        image = Image.open(name)
        image = image.resize((1070, 850))
        self.MapDisplay.setPixmap(QPixmap.fromImage(ImageQt(image)))


def map_generator(center, size):
    map_params = {'ll': center, 'spn': size, 'l': 'map'}
    map_api_server = 'http://static-maps.yandex.ru/1.x/'
    response = extract(map_api_server, params=map_params)
    map_file = 'map.jpg'
    with open(map_file, 'wb') as file:
        file.write(response.content)


def display_map(center, size):
    map_generator(center, size)
    app = QApplication(argv)
    window = MapWindow('map.jpg')
    window.show()
    destroy('map.jpg')
    exit(app.exec())


display_map('37.530117,55.805377', '0.00035,0.00035')  # Там "Пятерочка"
