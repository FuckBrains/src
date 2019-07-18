import json
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
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

def write_offer_config(file,content):
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


class Mywindow(Ui_MainWindow):
    def __init__(self,MainWindow):
        super().setupUi(MainWindow)	
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    def on_pushButton_clicked(self):
        print(type(self))
        print('=========')
        MainWindow.close

 
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = mywindow()
#     w.pushButton.clicked.connect(w.gass)
#     w.show()
#     sys.exit(app.exec_())


# def test_sig(self):
# 	print('====')
# 	print(self)


def main():
	app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
	MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
	ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
	# ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
	# ui.pushButton.clicked.connect(test_sig)
	MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
	sys.exit(app.exec_())


def write_empty_config(n):
	file = r'offer.ini' 
	offer_config = {}
	for i in range(n):
		offer_config[str(10000+i)] = ''
	write_offer_config(file,offer_config)


# def 


if __name__ == '__main__':
	offers = get_offer_config()
	print(offers)
