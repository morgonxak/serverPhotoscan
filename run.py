import socket
from threading import Thread
import json
import os
from workWithDataBase import DBManager

class socketServer(Thread):

    def __init__(self, addr):
        '''
        Коструктор
        :param addr: адресс сервера и порт для прослушки
        :param dictParameters: словарь со всеми параметрами принетые из формы
        '''
        Thread.__init__(self)
        self.addr = addr

    def closeServer(self):
        self.sock.close()

    def sendMessage(self, conn, message):
        '''
        метод отправки сообщения польщлвателю
        :param conn:
        :param message:
        :return:
        '''
        message = json.dumps(message)
        conn.send(bytes(message, encoding='utf-8'))

    def startProcess(self, dictParameters):
        '''
        Отправляет команду фотоскану на обработку и пишет этпы которые выполнил
        :dictParameters: {'':,'':}
        :return:
        '''
        self.dictParameters = dictParameters
        self.sendMessage(self.connPhotoscan, self.dictParameters)
        while True:
            data = self.connPhotoscan.recv(1024)
            if data == b'vse':
                break
            print("data = ", data.decode('utf-8'))
        print("процесс обработки закончился")
        return 1
    def run(self):
        self.runServer()
        a = input()
        self.startProcess()

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
        return self.connPhotoscan

if __name__ == "__main__":
    quryTest = {'ID_User': 1, 'pachProject': r'kkkk'}

    pachDB = r'C:\projectTree\database.db'
    SettingsPC = 'PC1'
    host = 'localhost'
    port = 777
    addr = (host, port)

    photoscanOBJ = socketServer(addr)
    photoscanOBJ.start()
    print("Сервер запущен")
    startPhotoscan(pachDB, SettingsPC)