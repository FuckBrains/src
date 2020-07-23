import json
import sys
sys.path.append("..")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QApplication,QWidget, QMessageBox
import os
os.system(r'pyuic5 -o uiclass.py ui\de_collector.ui')
from uiclass import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot




class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self) 


    @pyqtSlot()
    def on_pushButton1_clicked(self):
        param = self.comboBox.currentText()
        print('start with %s'%param)
        # db.init()
        # command = '''start cmd /k "python de_gen.pyc %d %s "{$name$:$qcy$}" && exit"'''%(1,param)
        # os.system(command)        
        command = '''start cmd /k "python de_gen_excel.pyc %d %s "{$name$:$qcy$}" && exit"'''%(1,param)
        os.system(command)        

    @pyqtSlot()
    def on_pushButton2_clicked(self):
        # param = self.comboBox.currentText()
        print('start sort')
        # db.init()
        command = '''start cmd /k "python de_gen_excel.pyc %d %s "{$name$:$qcy$}" && exit"'''%(0)
        os.system(command)    


def main(i,message=''):
    # up.main()
    import traceback
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    # MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());  
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)
    if i == 0:
        print('Updating config...')
        try:
            upc.update_config()
        except Exception as e:
            content = traceback.format_exc()  
            print('traceback.format_exc():' ,content)  
            print('Updating config failed')
            return
        print('Updating config success')        
        ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象        
        print('========+++')
        ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
        sys.exit(app.exec_())
    else:
        ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
        if message != '':
            message += '\n'*30+' '*100
            ui.alert(message)
            ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
        sys.exit(app.exec_())



if __name__ == '__main__':
    # paras=sys.argv
    # i = int(paras[1])
    i = 0
    # message = 'test'+'\n'*30+' '*100
    message = ''
    main(i,message)





