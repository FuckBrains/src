import sys
import os
sys.path.append("..")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QApplication,QWidget, QMessageBox

os.system(r'pyuic5 -o uiclass.py ui\login.ui')
from uiclass import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import db




class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setMaximumSize(800,600)
        self.setMinimumSize(800,600)            
        self.setupUi(self)       
        _translate = QtCore.QCoreApplication.translate        
        self.alliances = self.get_alliances()
        num_ali = len(self.alliances)
        for i in range(num_ali):
            self.comboBox1.addItem("")
            self.comboBox1.setItemText(i, _translate("MainWindow", str(i+1)+'.'+(self.alliances)[i]))        

    def get_alliances(self):
        alliances = db.get_alliances_info()
        return alliances

    @pyqtSlot()
    def on_pushButton1_clicked(self):
        alliance = self.comboBox1.current_text()        
        description = 
        db.updata_alliance_description(alliance,description)



def main():
    # up.main()

    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件

    # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    # MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());  
    ui = Mywindow(MainWindow)       
    ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())    


if __name__ == '__main__':
    main()