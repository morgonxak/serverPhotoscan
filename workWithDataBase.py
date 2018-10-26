import sqlite3

dictProcessingPhotoscan = {'Server': {1: 'DowloadPhoto', 2: 'CreatDirProject'},
                         'Photoscan':{1: 'CreatProject', 2: 'AddPhoto', 3: 'alingPhotos', 4: 'CoordinateSystem', 5: 'buildDenseCloud', 6: 'Manual processing'}}

class DBManager:
    def __init__(self, pachDB, SettingsPC):

        self.SettingsPC = SettingsPC
        self.conn = sqlite3.connect(pachDB, check_same_thread=False)  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()
        self.dictProcessingPhotoscan = dictProcessingPhotoscan
        self.killed = False

    def getSettings(self):
        wallet = self.cursor.execute(
            "SELECT pachImageTemp, pachProject, UserID FROM main.settings WHERE workplace = ?", (self.SettingsPC,))
        return wallet.fetchall()

    def pullData(self, DBtable, data):
        '''
        Вставка данных в таблицу принимаетт имя таблицы и [('Exodus', 'Andy Hunter')]
        [(UserID, 'Photoscan', 'CreatProject', False)]
        :param DBtable:
        :param data:
        :return:
        '''

        wallet = self.cursor.execute("SELECT STATE FROM treatment WHERE CATEGORY = 'Photoscan' AND PROCESS = ? AND ID = ?", (data[0][2], data[0][0]))

        try:
            if wallet.fetchall()[0][0] == 1:
                return True
        except IndexError:
            query = 'INSERT INTO ' + DBtable + ' VALUES (' + '?,' * (len(data[0]) - 1) + '?)'
            self.cursor.executemany(query, data)
            self.conn.commit()


    def editDataTreatment(self, data):
        wallet = self.cursor.execute("UPDATE treatment SET STATE = ? WHERE ID = ? AND CATEGORY = ? AND PROCESS = ?", (data[3], data[0], data[1], data[2]))
        self.conn.commit()
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

    def getAllUserID(self):
        wallet = self.cursor.execute("SELECT ID FROM treatment")
        return wallet.fetchall()

    def getListIDServer(self, process):
        wallet = self.cursor.execute("SELECT ID FROM treatment WHERE CATEGORY = 'Server' AND PROCESS = ? AND STATE = 1",(process,))
        return wallet.fetchone()

    def getNeedProcessing(self, UserID, process):
        '''
        True - Такой процесс уже быполнялся и он закончился успешно
        False - Такого процесса небыло либо он выполнелся неудачно
        :param UserID:
        :param process:
        :return:
        '''
        wallet = self.cursor.execute("SELECT STATE FROM treatment WHERE CATEGORY = 'Photoscan' AND PROCESS = ? AND  ID = ?",(process, UserID))
        try:
            if wallet.fetchall()[0][0] == 1:
                return True
            else:
                return False
        except IndexError:
            return 'NoData'

    def getAllIDForProcessing(self):
        itog = self.getListKey(self.getAllUserID())
        '''
        listAllUsetId = []
        for testList in dictProcessingPhotoscan['Server']:
            #listAllUsetId.append(self.getListKey(self.getListIDServer(dictProcessingPhotoscan['Server'][testList])))
            listAllUsetId.append(self.getListIDServer(dictProcessingPhotoscan['Server'][testList]))
            #print('ортировка по ',dictProcessingPhotoscan['Server'][testList],listAllUsetId)

        itog = set
        for res in listAllUsetId:
            itog = res.intersection(listAllUsetId[0])
        '''
        return itog


if __name__ == "__main__":
    test = DBManager(r'C:\projectTree\database.db', 'PC1')

    UserID = 10
    #print(test.dictProcessingPhotoscan['Photoscan'][5])
    #b = test.getNeedProcessing(UserID, test.dictProcessingPhotoscan['Photoscan'][5])
    #print(b)
    #d = test.getAllIDForProcessing()
    #print(type(d))
    #print(d)

    c = test.pullData('treatment', [(UserID, 'Photoscan', 'CreatProject', False)])
    print(c)
