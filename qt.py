import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QApplication,QWidget, QMessageBox
# from PyQt5.QtCore import pyqtSignature
import sys
import os
os.system(r'pyuic5 -o uiclass.py ui\test.ui')
from uiclass import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot


def Read_Ini(file):
    submits = []
    with open(file,'r') as f:
        jss = f.readlines()
        # print(jss)
        for js in jss:
            submit = json.loads(js)
            submits.append(submit)
            # print(submit)
    if len(submits) >= 1:
        return submits[-1]
    else:
        return []

def Write_Ini(file,content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)

def Add_New_Offer(Alliance,New_Offers):
    '''
    Alliance= 'Finaff'
    New_Offers = ['Cam4,'Stripchat]
    '''
    file_Offer_config = r'ini\Offer.ini'
    Alliance_Offer_Config = Read_Ini(file_Offer_config)
    type_dict = type({})
    if type(Alliance_Offer_Config) != type_dict:
        Alliance_Offer_Config = {}
    keys = []
    for item in Alliance_Offer_Config:
        keys.append(item)
    if Alliance in keys:
        for offer in New_Offers:
            if offer not in Alliance_Offer_Config[Alliance]:
                Alliance_Offer_Config[Alliance].append(offer)
    else:
        Alliance_Offer_Config[Alliance] = New_Offers
    Write_Ini(file_Offer_config,Alliance_Offer_Config)

def Add_New_Config(Offer_name,Offer_config_new):
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = Read_Ini(file_Offer_config) 
    Offer_config[Offer_name] = Offer_config_new
    Write_Ini(file_Offer_config,Offer_config)

def translate_offer_tonum(Offer_list):
    return 

def Add_New_Link(new_offer):
    file_Offer_link = r'ini\Offer_link.ini'    
    type_dict = type({})
    new_offer['Offer']=new_offer['Offer'].split('.')[1]
    Offer_link = Read_Ini(file_Offer_link)  
    if type(Offer_link)!= type_dict:
        Offer_link = {}
    Offer_link[str(len(Offer_link))] = new_offer
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = Read_Ini(file_Offer_config)  
    keys = []
    for item in Offer_config:
        keys.append(item)
    # print(keys)
    # print(new_offer['Offer'])
    if new_offer['Offer'] in keys:
        Offer_link[str(len(Offer_link)-1)] = dict(Offer_link[str(len(Offer_link)-1)],**Offer_config[new_offer['Offer']])    
        Write_Ini(file_Offer_link,Offer_link)            
    return

def Delete_Link(key):
    file_Offer_link = r'ini\Offer_link.ini' 
    Offer_link = Read_Ini(file_Offer_link)
    if len(Offer_link) == 0:
        return
    Offer_link.pop(str(key))
    num_link = len(Offer_link)
    for i in range(num_link):
        if i >= key:
            Offer_link[str(i)] = Offer_link.pop(str(i+1))
    Write_Ini(file_Offer_link,Offer_link)

class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self) 
        file_Offer = r'ini\Offer.ini'
        _translate = QtCore.QCoreApplication.translate
        self.offer = Read_Ini(file_Offer)
        i = 0
        end = len(self.offer)
        text = 'Already in config links\n'
        for item in self.offer:
            if i >= end:
                break
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, _translate("MainWindow", item))
            i+=1
        self.set_comboBox2()
        self.set_text()
        self.set_comboBox3()

    def set_comboBox2(self):
        _translate = QtCore.QCoreApplication.translate
        j = 0
        self.comboBox_2.clear()
        print('========')
        item = self.comboBox.currentText()
        if item != '':
            for offer_ in self.offer[item]:
                if j >= len(self.offer[item]):
                    break                
                self.comboBox_2.addItem("")
                self.comboBox_2.setItemText(j, _translate("MainWindow", str(j+1)+'.'+offer_))            
                j+=1
    def set_comboBox3(self):
        _translate = QtCore.QCoreApplication.translate      
        j = 0
        print('set_comboBox3')
        self.comboBox_3.clear()
        self.offer_link = Read_Ini(self.file_Offer_link)
        for item in self.offer_link:
            if j >= len(self.offer_link):
                break                
            self.comboBox_3.addItem("")
            self.comboBox_3.setItemText(j, _translate("MainWindow", str(int(item)+1)))            
            j+=1

    def set_text(self):
        self.file_Offer_link = r'ini\Offer_link.ini'
        self.offer_link = Read_Ini(self.file_Offer_link)
        text = 'Already in config links\n'
        for item in self.offer_link:
            text += str(int(item)+1)+' : '+self.offer_link[item]['Alliance']+' '+self.offer_link[item]['Offer']+' '+self.offer_link[item]['url_link']+'\n'
        self.textBrowser.setText(text)        

    # @pyqtSlot()
    def on_comboBox_currentIndexChanged(self):
        print('----------')
        self.set_comboBox2()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        # print(self.comboBox.currentText())
        # print(self.comboBox_2.currentText())
        # print(self.lineEdit.text())
        # print(type(self))
        # print('=========')
        # self.lineEdit.setText('')
        new_offer = {}
        new_offer['Alliance'] = self.comboBox.currentText()
        new_offer['Offer'] = self.comboBox_2.currentText()
        new_offer['url_link'] = self.lineEdit.text()
        if 'http' not in new_offer['url_link']:
            print('++++')
            return
        print('1111')
        Add_New_Link(new_offer)
        self.set_text()
        self.set_comboBox3()
        # self.lineEdit.setText('')


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        # print(self.comboBox.currentText())
        # print(self.comboBox_2.currentText())
        key = self.comboBox_3.currentText()
        if key == '':
            return
        key = int(key) - 1 
        Delete_Link(key)
        self.set_text()
        self.set_comboBox3()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        file_Offer = r'ini\Offer.ini'
        self.offer = Read_Ini(file_Offer)        
        print(self.comboBox_3.currentText())
        key = self.comboBox_3.currentText()
        if key == '':
            return
        key = int(key) - 1 
        Delete_Link(key)
        self.set_text()
        self.set_comboBox3()

    # def on_lineEdit_selectionChanged(self):
    #     self.lineEdit.setText('')

    # def on_lineEdit_editingFinished(self):
    #     self.lineEdit.setText('')

def main():
    print('111')
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)
    ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())

def Add_new_module_test():
    Offer_name = 'Best Obama Care - US(Done)'
    Offer_config_new = {"Mission_Id": "10007", "Excel": ["Auto", "Email"], "Country": "US"}
    Add_New_Config(Offer_name,Offer_config_new)
    Alliance = 'Adgeam'
    New_Offers = [Offer_name]
    Add_New_Offer(Alliance,New_Offers)

if __name__ == '__main__':
    main()
    # Add_new_module_test()




