import socket
from threading import Thread
import json
import os

class socketServer(Thread):

    def __init__(self, addr):
        '''
        Коструктор
        :param addr: адресс сервера и порт для прослушки
        :param dictParameters: словарь со всеми параметрами принетые из формы
        '''
        self.addr = addr


    def run(self, dictParameters):

        self.dictParameters = dictParameters
        self.runPhotoscan()

    def runServer(self):
        '''
        Запускает сервер и ждет подключения
        :return:
        '''
        self.sock = socket.socket()
        self.sock.bind(self.addr)
        self.sock.listen(2)

        self.connPhotoscan, addr = self.sock.accept()
        print('Фотоскан подключился: ', addr)
        #self.conArcGis, addr = sock.accept()
        #print('ArcGis подключен: ', addr)

    def sendMessage(self, conn, message):
        '''
        метод отправки сообщения польщлвателю
        :param conn:
        :param message:
        :return:
        '''
        message = json.dumps(message)
        conn.send(bytes(message, encoding='utf-8'))

    def closeServer(self):
        self.sock.close()

    def runPhotoscan(self):
        '''
        Отправляет команду фотоскану на обработку и пишет этпы которые выполнил
        :return:
        '''
        self.sendMessage(self.connPhotoscan, self.dictParameters)
        while True:
            data = self.connPhotoscan.recv(1024)
            if data == b'vse':
                break
            print("data = ", data.decode('utf-8'))

    def runArcGis(self):
        pass

pachPHotoscanProject = r'D:\dimaProject\photoscan\processing_photoscan'


def getID(pach):
    '''
    Сканирует папку на изменения и если в папке они произошли возвращает имя папки
    :param pach:
    :return:
    '''
    listNameOld = os.listdir(pach)
    while True:
        listName = os.listdir(pach)
        for e in listName:
            if not e in listNameOld:

                return e


def startserver():
    host = 'localhost'
    port = 777
    addr = (host, port)

    dictParameters = dict()

    test = socketServer(addr)
    test.runServer()
    dictParameters['ID_User'] = getID(pachPHotoscanProject)
    # Отправляем команду на запуск с параметрами
    test.run(dictParameters)

if __name__ == "__main__":
    startserver()

