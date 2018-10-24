import sqlite3

dictProcessingPhotoscan = {'Server': {1: 'DowloadPhoto', 2: 'CreatDirProject'},
                         'Photoscan':{1: 'CreatProject', 2: 'AddPhoto', 3: 'alingPhotos', 4: 'CoordinateSystem', 5:'buildDenseCloud'}}

class DBManager:
    def __init__(self, pachDB, SettingsPC):

        self.SettingsPC = SettingsPC
        self.conn = sqlite3.connect(pachDB, check_same_thread=False)  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()

    def getSettings(self):
        wallet = self.cursor.execute(
            "SELECT pachImageTemp, pachProject, UserID FROM main.settings WHERE workplace = ?", (self.SettingsPC,))
        return wallet.fetchall()

    def pullData(self, DBtable, data):
        '''
        Вставка данных в таблицу принимаетт имя таблицы и [('Exodus', 'Andy Hunter')]
        :param DBtable:
        :param data:
        :return:
        '''

        query = 'INSERT INTO ' + DBtable + ' VALUES (' + '?,'*(len(data[0])-1) + '?)'

        self.cursor.executemany(query, data)
        self.conn.commit()

    def editDataTreatment(self, data):
        wallet = self.cursor.execute("UPDATE treatment SET STATE = ? WHERE ID = ? AND CATEGORY = ? AND PROCESS = ?", (data[3], data[0], data[1], data[2]))
        self.conn.commit()
        return wallet.fetchall()

    def getInfoProcess(self, UserID):

        wallet = self.cursor.execute("SELECT CATEGORY, PROCESS, STATE FROM treatment WHERE ID = ?", (UserID,))
        return wallet.fetchall()

    def getAllUserID(self):
        wallet = self.cursor.execute("SELECT ID FROM treatment ")
        return wallet.fetchall()

    def getAllUserIDnoProcessingPhotoscan(self):
        wallet = self.cursor.execute("SELECT ID FROM treatment WHERE CATEGORY = 'Photoscan'")
        return wallet.fetchall()

    def getListKey(self, list):
        '''
        Принимает все ID пользователей возвращает  сет из уникальных пользователей
        :param list:
        :return:
        '''
        self.listKey = set()
        for i in list:
            self.listKey.add(i[0])
        return self.listKey

    def getListIDServer(self, process):
        wallet = self.cursor.execute("SELECT ID FROM treatment WHERE CATEGORY = 'Server' AND PROCESS = ? AND STATE = 1",(process,))
        return wallet.fetchall()

    def getAllIDForProcessing(self):
        listAllUsetId = []
        for testList in dictProcessingPhotoscan['Server']:
            listAllUsetId.append(self.getListKey(self.getListIDServer(dictProcessingPhotoscan['Server'][testList])))
            #print('ортировка по ',dictProcessingPhotoscan['Server'][testList],listAllUsetId)

        itog = set
        for res in listAllUsetId:
            itog = res.intersection(listAllUsetId[0])

        return itog

if __name__ == "__main__":
    test = DBManager(r'C:\projectTree\database.db', 'PC1')
    #a = test.getAllIDForProcessingPhotoscan()
    #b = test.getAllIDForProcessingExportPhotoscan()
    #print('Нужна обработка photoscan', a)
    #print('Нужен экспорт данных', b)

    #c = test.getAllIDForProcessing()
    #print('Пользователи для обработки:', c[0])
    #print('Пользователи для экспорта:', c[1])

    #UserID = 1
    #test.pullData('treatment', [(UserID, 'Photoscan', 'CreatProject', False)])
    #test.editDataTreatment((UserID, 'Photoscan', 'CreatProject', False))

    d = test.test()
    print(d)
