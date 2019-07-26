import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QApplication,QWidget, QMessageBox
# from PyQt5.QtCore import pyqtSignature
import sys
import os
os.system(r'pyuic5 -o uiclass.py ui\test.ui')
from uiclass import Ui_MainWindow


def get_offer_config():
    file = r'offer.ini'
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

def write_offer_config(content):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    file = r'offer.ini'
    content = json.dumps(content) 
    with open(file,'w') as f:
        # content += '\n'
        f.write(content)



class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self) 
        _translate = QtCore.QCoreApplication.translate
        self.offer = get_offer_config()
        i = 0
        end = len(self.offer)
        for item in self.offer:
            if i >= end:
                break
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, _translate("MainWindow", item))
            i+=1
    def on_pushButton_clicked(self):
        print(type(self))
        print('=========')
        self.lineEdit.setText('')

    def on_lineEdit_selectionChanged(self):
        self.lineEdit.setText('')

    def on_lineEdit_editingFinished(self):
        self.lineEdit.setText('')


 

def main():
    print('111')
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)
    ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())


def write_empty_config(n):
    offer_config = {}
    for i in range(n):
        offer_config[str(10000+i)] = ''
    write_offer_config(offer_config)




if __name__ == '__main__':
    main()
    # submit_offer = get_offer_config()
    # print(submit_offer)
    # submit_offer['rifu'] = ['liulanqi']
    # write_offer_config(submit_offer)
    # file = 'offer.ini'
    # submit_offer = {'Finaff':['Cam4','Stripchat'],'Adpump':['Star stable']}
    # write_offer_config(file,submit_offer)