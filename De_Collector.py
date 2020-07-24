import json
import sys
sys.path.append("..")
from PyQt5.QtWidgets import QMainWindow , QApplication
from PyQt5.QtCore import pyqtSlot,QThread,QCoreApplication
import os
# # os.system(r'pyuic5 -o uiclass2.py ui\de_collector.ui')
from uiclass2 import Ui_MainWindow
from de_gen_excel import Collector


class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self) 
        _translate = QCoreApplication.translate

    @pyqtSlot()
    def on_pushButton1_clicked(self):
        param = self.comboBox.currentText()
        self.thread = RunThread(1,param)
        self.thread.start()        
        # print('start with %s'%param)
        # collector = Collector(1,param)   
        # collector.final_yellow_page(QApplication)
        # QApplication.processEvents()
        # db.init()
        # command = '''start cmd /k "python de_gen.pyc %d %s "{$name$:$qcy$}" && exit"'''%(1,param)
        # os.system(command)        
        # command = '''start cmd /k "python de_gen_excel.pyc %d %s "{$name$:$qcy$}" && exit"'''%(1,param)
        # os.system(command)        

    @pyqtSlot()
    def on_pushButton2_clicked(self):
        # param = self.comboBox.currentText()
        print('Collect data')
        # QApplication.processEvents()
        self.thread = RunThread(0,'')
        self.thread.start()


class RunThread(QThread):
    def __init__(self,count,param):
        super().__init__()
        self.count = count
        self.collector = Collector(count,param)

    def run(self):
        if self.count == 0:
            self.collector.collect()
        else:
           self.collector.final_yellow_page()

def main():
    # up.main()
    import traceback
    app = QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    # MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());  
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)

    ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象        
    print('========+++')
    ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()





