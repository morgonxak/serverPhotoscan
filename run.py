import socket
from threading import Thread
import json
import os
from workWithDataBase import DBManager
import comandPhotoscan

PACH_DB = r'C:\projectTree\database.db'
SETTING_PC = 'PC1'

class PhotoscanProcessing(Thread):

    def __init__(self, pachDB, settingPC):
        Thread.__init__(self)
        self.db = self.OpenDB(pachDB, settingPC)
        #[('C:\\Users\\admin\\PycharmProjects\\photoscan\\app\\static\\images', 'C:\\projectTree', 12)]
        self.settings = self.db.getSettings()

    def run(self):
        #while True:
            self.listIDProcessing = self.db.getAllIDForProcessing()
            try:
                UserIDProcessingPhotoscan = list(self.listIDProcessing[0])[0]
                print("Начало обработки для ID", UserIDProcessingPhotoscan)
                self.processingPhotoscan(UserIDProcessingPhotoscan)
            except IndexError:
                pass
                print("Данных для обработки нет")
            try:
                UserIDProcessingExport = list(self.listIDProcessing[1])[0]
                print("Начало экспорта для ID", UserIDProcessingExport)
                self.processingExport(UserIDProcessingExport)
            except IndexError:
                pass
                print("Данных для экспорта нет")

    def processingPhotoscan(self, UserID):
        '''
        апуск обработки
        :return:
        '''

        print("Начало создания проекта", UserID)
        self.db.pullData('treatment', [(UserID, 'Photoscan', 'CreatProject', False)])
        self.chunk, self.doc = comandPhotoscan.creatProject(self.settings[0][1] + r'\ID_' + str(UserID) + r'\'', 'project')
        self.db.editDataTreatment((UserID, 'Photoscan', 'CreatProject', True))
        print("Окончание создания проекта")

        print("Начало добовления фото")
        self.db.pullData('treatment', [(UserID, 'Photoscan', 'AddPhoto', False)])
        comandPhotoscan.AddPhoto(self.chunk, self.settings[0][1] + '\/ID_' + str(UserID) + '\/' + 'photo')
        self.db.editDataTreatment((UserID, 'Photoscan', 'AddPhoto', True))
        print("Конец добовления фото")

        print("начало выравнивание фотографий")
        self.db.pullData('treatment', [(UserID, 'Photoscan', 'alingPhotos', False)])
        comandPhotoscan.alingPhotos(self.chunk, self.doc)
        self.db.editDataTreatment((UserID, 'Photoscan', 'alingPhotos', True))
        print("Конец выравнивание фотографий")

        print("начало выставления системы координат")
        self.db.pullData('treatment', [(UserID, 'Photoscan', 'CoordinateSystem', False)])
        comandPhotoscan.setCoordinateSystem(self.chunk, self.doc)
        self.db.editDataTreatment((UserID, 'Photoscan', 'CoordinateSystem', True))
        print("Конец выставления системы координат")


        try:
            print("начало построения плотного облака точек")
            self.db.pullData('treatment', [(UserID, 'Photoscan', 'buildDenseCloud', False)])
            comandPhotoscan.buildDenseCloud(self.chunk, self.doc)
            self.db.editDataTreatment((UserID, 'Photoscan', 'buildDenseCloud', True))
            print("Конец построения плотного облака точек")
        except RuntimeError:
            print("шибка мало данных для построения плотного облака")


    def processingExport(self, UserID):
        '''
        Экспортирует данные в нужные папки
        :return:
        '''
        pass

    def OpenDB(self, pachDB, settingPC):
        return DBManager(pachDB, settingPC)

if __name__ == "__main__":
    test = PhotoscanProcessing(PACH_DB, SETTING_PC)
    print("ЗАпускаем поток")
    id = test.start()
    print("ID потока", id)
