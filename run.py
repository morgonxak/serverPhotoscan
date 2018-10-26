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
        self.settings = self.db.getSettings()

    def run(self):
        #while True:
            self.listIDProcessing = self.db.getAllIDForProcessing()
            try:
                UserIDProcessingPhotoscan = list(self.listIDProcessing)[0]
                print("Начало обработки для ID", UserIDProcessingPhotoscan)
                self.startProcessingPhotoscan(UserIDProcessingPhotoscan)
            except IndexError:
                pass
                print("Данных для обработки нет")


    def startProcessingPhotoscan(self, UserID):
        '''
        апуск обработки
        :return:
        '''

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][1]):
            print("Начало создания проекта", UserID)
            self.db.pullData('treatment', [(UserID, 'Photoscan', 'CreatProject', False)])
            self.db.editDataTreatment((UserID, 'Photoscan', 'CreatProject', False))
            self.chunk, self.doc = comandPhotoscan.creatProject(self.settings[0][1] + r'\ID_' + str(UserID) + r'\'', 'project')
            self.db.editDataTreatment((UserID, 'Photoscan', 'CreatProject', True))
            print("Окончание создания проекта")
        else:
            print("Проект уже создан: этап открытия проекта")
            self.chunk, self.doc = comandPhotoscan.creatProject(self.settings[0][1] + r'\ID_' + str(UserID) + r'\'', 'project')

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][2]):
            print("Начало добовления фото")
            self.db.pullData('treatment', [(UserID, 'Photoscan', 'AddPhoto', False)])
            self.db.editDataTreatment((UserID, 'Photoscan', 'AddPhoto', False))
            comandPhotoscan.AddPhoto(self.chunk, self.settings[0][1] + '\/ID_' + str(UserID) + '\/' + 'photo')
            self.db.editDataTreatment((UserID, 'Photoscan', 'AddPhoto', True))
            print("Конец добовления фото")
        else:
            print("Уже проделан этот шаг: добовления фото")

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][3]):
            print("начало выравнивание фотографий")
            self.db.pullData('treatment', [(UserID, 'Photoscan', 'alingPhotos', False)])
            self.db.editDataTreatment((UserID, 'Photoscan', 'alingPhotos', False))
            comandPhotoscan.alingPhotos(self.chunk, self.doc)
            self.db.editDataTreatment((UserID, 'Photoscan', 'alingPhotos', True))
            print("Конец выравнивание фотографий")
        else:
            print("Уже проделан этот шаг: выравнивание фотографий")

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][4]):
            print("начало выставления системы координат")
            self.db.pullData('treatment', [(UserID, 'Photoscan', 'CoordinateSystem', False)])
            self.db.editDataTreatment((UserID, 'Photoscan', 'CoordinateSystem', False))
            comandPhotoscan.setCoordinateSystem(self.chunk, self.doc)
            self.db.editDataTreatment((UserID, 'Photoscan', 'CoordinateSystem', True))
            print("Конец выставления системы координат")
        else:
            print("Уже проделан этот шаг: выставления системы координат")

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][5]):
            print("Этап построения облака точек")
            try:
                print("начало построения плотного облака точек")
                self.db.pullData('treatment', [(UserID, 'Photoscan', 'buildDenseCloud', False)])
                self.db.editDataTreatment((UserID, 'Photoscan', 'buildDenseCloud', False))
                comandPhotoscan.buildDenseCloud(self.chunk, self.doc)
                self.db.editDataTreatment((UserID, 'Photoscan', 'buildDenseCloud', True))
                print("Конец построения плотного облака точек")
            except BaseException:
                print("Слишком мало данных для построения плотного облака")
        else:
            print("Уже проделан этот шаг: построения облака точек")

        if not self.db.getNeedProcessing(UserID, self.db.dictProcessingPhotoscan['Photoscan'][6]):
            print("Этап Экспорта данных")

        else:
            print("Этап экспорта точек не требуется")

    def OpenDB(self, pachDB, settingPC):
        return DBManager(pachDB, settingPC)

if __name__ == "__main__":
    test = PhotoscanProcessing(PACH_DB, SETTING_PC)
    print("ЗАпускаем поток")
    id = test.start()
    print("ID потока", id)
