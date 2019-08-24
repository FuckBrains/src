import json
import sys
sys.path.append("..")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QApplication,QWidget, QMessageBox
# from PyQt5.QtCore import pyqtSignature
import sys
import os
os.system(r'pyuic5 -o uiclass.py ui\test.ui')
from uiclass import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import Update_config as up
import db





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

# def Add_New_Offer(Alliance,New_Offers):
#     '''
#     Alliance= 'Finaff'
#     New_Offers = ['Cam4,'Stripchat]
#     '''
#     file_Offer_config = r'ini\Offer.ini'
#     Alliance_Offer_Config = Read_Ini(file_Offer_config)
#     type_dict = type({})
#     if type(Alliance_Offer_Config) != type_dict:
#         Alliance_Offer_Config = {}
#     keys = []
#     for item in Alliance_Offer_Config:
#         keys.append(item)
#     if Alliance in keys:
#         for offer in New_Offers:
#             if offer not in Alliance_Offer_Config[Alliance]:
#                 Alliance_Offer_Config[Alliance].append(offer)
#     else:
#         Alliance_Offer_Config[Alliance] = New_Offers
#     Write_Ini(file_Offer_config,Alliance_Offer_Config)

# def Add_New_Config(Offer_name,Offer_config_new):
#     file_Offer_config = r'ini\Offer_config.ini'
#     Offer_config = Read_Ini(file_Offer_config) 
#     Offer_config[Offer_name] = Offer_config_new
#     Write_Ini(file_Offer_config,Offer_config)

def translate_offer_tonum(Offer_list):
    return 

def Add_New_Link(new_offer,all_links = 0):
    if all_links == 0 :
        file_Offer_link = r'..\res\Offer_link.ini'    
    else:
        file_Offer_link = r'..\res\Offer_all_links.ini'
    type_dict = type({})
    if '.' in new_offer['Offer']:
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
    print(keys)
    print(new_offer['Offer'])
    if new_offer['Offer'] in keys:
        Offer_link[str(len(Offer_link)-1)] = dict(Offer_link[str(len(Offer_link)-1)],**Offer_config[new_offer['Offer']])    
        Write_Ini(file_Offer_link,Offer_link)            
    return

def Delete_Link(key,all_links = 0):
    if all_links == 0 :
        file_Offer_link = r'..\res\Offer_link.ini'    
    else:
        file_Offer_link = r'..\res\Offer_all_links.ini'    
    # file_Offer_link = r'ini\Offer_link.ini' 
    Offer_link = Read_Ini(file_Offer_link)
    if len(Offer_link) == 0:
        return
    target_link = Offer_link.pop(str(key))
    num_link = len(Offer_link)
    # target_link = num_link[key]
    for i in range(num_link):
        if i >= key:
            Offer_link[str(i)] = Offer_link.pop(str(i+1))
    Write_Ini(file_Offer_link,Offer_link)
    return target_link

class Mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        self.excels,self.emails,self.Missions = db.read_all_info()
        print(self.emails)
        QMainWindow.__init__(self,parent)
        self.setupUi(self) 
        file_Offer = r'ini\Offer.ini'
        _translate = QtCore.QCoreApplication.translate
        self.offer = Read_Ini(file_Offer)
        file_Offer_config = r'ini\Offer_config.ini'
        self.Offer_config = Read_Ini(file_Offer_config)         
        i = 0
        end = len(self.offer)
        # text = 'Already in config links\n'
        for item in self.offer:
            if i >= end:
                break
            self.comboBox1.addItem("")
            self.comboBox1.setItemText(i, _translate("MainWindow", item))
            i+=1
        self.set_comboBox2()
        self.set_text_woring_links()
        self.set_text_all_links()
        self.set_comboBox3()
        self.set_comboBox4()
        self.setWindowTitle('EMU_MultiMission')
        # self.resize(500,300)   
        excel_list = ['Mission_Id','Offer'] 
        for excel in self.excels:
            excel = excel+'('+str(self.excels[excel])+')'
            excel_list.append(excel)  
        excel_list.append('Email'+'('+str(self.emails['Email'])+str(')'))
        self.model=QtGui.QStandardItemModel(50,10)
        self.model.setHorizontalHeaderLabels(excel_list)
        keys = []
        for item in self.Missions:
            keys.append(item)
        keys.sort()
        print('keys of Missions')
        print(keys)
        # print(self.Missions[keys[row]])
        for row in range(len(self.Missions)):
            print(str(keys[row]))
            item=QtGui.QStandardItem(str(keys[row]))
            #设置每个位置的文本值
            self.model.setItem(row,0,item)          
            # print('+++++++++++++')
            # print(self.Offer_config)
            for offer in self.Offer_config:
                if offer == 'Delay' or offer == 'Email_list':
                    continue
                if str(self.Offer_config[offer]['Mission_Id']) == str(keys[row]):
                    Excel_used_ = self.Offer_config[offer]['Excel']
                    Offer_name = offer
            item=QtGui.QStandardItem(Offer_name)
            #设置每个位置的文本值
            self.model.setItem(row,1,item)                      
            # Excel_used_ = self.Offer_config[int(item)]['Excel']
            key_list = ['Mission_Id','Offer']
            # for name in excel_list:
            excel_list = [excel.split('(')[0] for excel in excel_list if excel not in key_list]
            print(self.Missions)
            for index_excel in Excel_used_:
                # print(index_excel)
                if index_excel == '':
                    continue
                if index_excel in key_list:
                    continue
                col = excel_list.index(index_excel)+2
                # print(col)
                # print(self.Missions[int(keys[row])])
                if index_excel !='Email':
                    print('total:',self.excels[index_excel])
                    print('Used:',self.Missions[int(keys[row])])
                    num_left = self.excels[index_excel] - self.Missions[int(keys[row])]
                else:
                    num_left = self.emails['Email'] - self.Missions[int(keys[row])]                    
                item_=QtGui.QStandardItem(str(num_left))
                self.model.setItem(row,col,item_)

        #实例化表格视图，设置模型为自定义的模型
        # self.tableView=QtWidgets.QTableView()
        self.tableView.setModel(self.model)   
        print(self.excels,self.emails,self.Missions)
        #设置布局
        # layout=QtWidgets.QVBoxLayout()
        # layout.addWidget(self.tableView)
        # self.setLayout(layout)  
        print('===========++++')      

    def set_comboBox2(self):
        _translate = QtCore.QCoreApplication.translate
        j = 0
        self.comboBox2.clear()
        print('========')
        item = self.comboBox1.currentText()
        if item != '':
            for offer_ in self.offer[item]:
                if j >= len(self.offer[item]):
                    break                
                self.comboBox2.addItem("")
                self.comboBox2.setItemText(j, _translate("MainWindow", str(j+1)+'.'+offer_))            
                j+=1
    
    def set_comboBox3(self):
        _translate = QtCore.QCoreApplication.translate      
        j = 0
        print('set_comboBox3')
        self.comboBox3.clear()
        self.offer_link = Read_Ini(self.file_Offer_link_all)
        for item in self.offer_link:
            if j >= len(self.offer_link):
                break                
            self.comboBox3.addItem("")
            self.comboBox3.setItemText(j, _translate("MainWindow", str(int(item)+1)))            
            j+=1

    def set_comboBox4(self):
        _translate = QtCore.QCoreApplication.translate      
        j = 0
        print('set_comboBox4')
        self.comboBox4.clear()
        self.offer_link_all = Read_Ini(self.file_Offer_link)
        for item in self.offer_link_all:
            if j >= len(self.offer_link_all):
                break                
            self.comboBox4.addItem("")
            self.comboBox4.setItemText(j, _translate("MainWindow", str(int(item)+1)))            
            j+=1

    def set_text_woring_links(self):
        self.file_Offer_link = r'..\res\Offer_link.ini'
        self.offer_link = Read_Ini(self.file_Offer_link)
        text = 'Already in config links\n'
        for item in self.offer_link:
            text += str(int(item)+1)+' : '+self.offer_link[item]['Alliance']+'-->> '+self.offer_link[item]['Offer']+'-->>    '+self.offer_link[item]['Country']+'\n     '+self.offer_link[item]['url_link']+'\n'
        self.textBrowser2.setText(text)        

    def set_text_all_links(self):
        self.file_Offer_link_all = r'..\res\Offer_all_links.ini'
        self.offer_link_all = Read_Ini(self.file_Offer_link_all)
        text = 'Already in config links\n'
        for item in self.offer_link_all:
            text += str(int(item)+1)+' : '+self.offer_link_all[item]['Alliance']+'-->> '+self.offer_link_all[item]['Offer']+'-->>    '+self.offer_link_all[item]['Country']+'\n     '+self.offer_link_all[item]['url_link']+'\n'
        self.textBrowser1.setText(text) 

    # @pyqtSlot()
    def on_comboBox1_currentIndexChanged(self):
        # print('----------')
        self.set_comboBox2()
        print(self.comboBox2.currentText())
        if self.comboBox2.currentText() == '':
            return
        # offer_chosen = self.comboBox2.currentText().split('.')[1]
        # print(self.Offer_config[offer_chosen])
        # Mission_Id = self.Offer_config[offer_chosen]['Mission_Id']
        # print(Mission_Id)
        # Excel_used = self.Offer_config[offer_chosen]['Excel']
        # text = Excel_used[0]+Excel_used[1]
        # Mission_list = [str(Mission_Id)]
        # Email_list_dict = self.Offer_config['Email_list']
        # Email_list = []
        # print(Email_list_dict)
        # for item in Email_list_dict:
        #     if str(Email_list_dict[item]) == '1':
        #         Email_list.append(item)
        # print(Mission_list,Excel_used,Email_list)
        # rest = db.read_rest(Mission_list,Excel_used,Email_list)
        # print(rest)
        # text_rest = Excel_used[0]+':'+str(rest[0])+','+Excel_used[1]+':'+str(rest[1])        
        # self.lineEdit_5.setText(text)
        # self.lineEdit_6.setText(Mission_Id)
        # self.lineEdit_7.setText(text_rest)        


    def get_config_info(self):
        BasicInfo_dict,Email_dict,Mission_dict = read_rest(Mission_list,Excel_name,Email_list)
        for offer_chosen in self.Offer_config:
            Mission_Id = self.Offer_config[offer_chosen]['Mission_Id']
            print(Mission_Id)
            Excel_used = self.Offer_config[offer_chosen]['Excel']
            text = Excel_used[0]+Excel_used[1]
            Mission_list = [str(Mission_Id)]
            Email_list = self.Offer_config['Email_list']
            # offer = {}
            # offer['Mission_Id'] = Mission_Id
            # offer['Excel'] = Excel
            # offer['Email_list'] = Email_list
            rest = db.read_rest(offer)        


    # @pyqtSlot()
    # def on_comboBox2_currentIndexChanged(self):
    #     # print('----------')
    #     print(self.comboBox2.currentText())
    #     if self.comboBox2.currentText() == '':
    #         return
    #     offer_chosen = self.comboBox2.currentText().split('.')[1]
    #     print(self.Offer_config[offer_chosen])
    #     Mission_Id = self.Offer_config[offer_chosen]['Mission_Id']
    #     print(Mission_Id)
    #     Excel_used = self.Offer_config[offer_chosen]['Excel']
    #     text = Excel_used[0]+Excel_used[1]
    #     Mission_list = [str(Mission_Id)]
    #     Email_list_dict = self.Offer_config['Email_list']
    #     Email_list = []
    #     print(Email_list_dict)
    #     for item in Email_list_dict:
    #         if str(Email_list_dict[item]) == '1':
    #             Email_list.append(item)
    #     print(Mission_list,Excel_used,Email_list)
    #     rest = db.read_rest(Mission_list,Excel_used,Email_list)
    #     print(rest)
    #     text_rest = Excel_used[0]+':'+str(rest[0])+','+Excel_used[1]+':'+str(rest[1])        
    #     self.lineEdit_5.setText(text)
    #     self.lineEdit_6.setText(Mission_Id)
    #     self.lineEdit_7.setText(text_rest)

    @pyqtSlot()
    def on_pushButton1_clicked(self):
        # print(self.comboBox.currentText())
        # print(self.comboBox_2.currentText())
        # print(self.lineEdit.text())
        # print(type(self))
        # print('=========')
        # self.lineEdit.setText('')
        new_offer = {}
        new_offer['Alliance'] = self.comboBox1.currentText()
        new_offer['Offer'] = self.comboBox2.currentText()
        new_offer['url_link'] = self.lineEdit.text()
        new_offer['Country'] = self.comboBox5.currentText()
        if 'http' not in new_offer['url_link']:
            print('++++')
            return
        print(new_offer)
        Add_New_Link(new_offer,1)
        self.set_text_all_links()
        self.set_comboBox3()
        self.lineEdit.setText('')


    @pyqtSlot()
    def on_pushButton2_clicked(self):
        # print(self.comboBox.currentText())
        # print(self.comboBox_2.currentText())
        key = self.comboBox3.currentText()
        if key == '':
            return
        key = int(key) - 1 
        print(key)
        file_Offer_link = r'..\res\Offer_all_links.ini'    
        # file_Offer_link = r'ini\Offer_link.ini' 
        Offer_link = Read_Ini(file_Offer_link)
        if len(Offer_link) == 0:
            return
        new_offer = Offer_link[str(key)]        
        # new_offer = Delete_Link(key,1)
        print(new_offer)
        Add_New_Link(new_offer)
        self.set_text_all_links()
        self.set_comboBox3()
        self.set_text_woring_links()
        self.set_comboBox4()

    @pyqtSlot()
    def on_pushButton3_clicked(self):
        key = self.comboBox3.currentText()
        if key == '':
            return
        key = int(key) - 1 
        Delete_Link(key,1)
        self.set_text_all_links()
        self.set_comboBox3()
        self.set_text_woring_links()
        self.set_comboBox4()


    @pyqtSlot()
    def on_pushButton4_clicked(self):
        key = self.comboBox4.currentText()
        if key == '':
            return
        key = int(key) - 1 
        Delete_Link(key)
        self.set_text_woring_links()
        self.set_comboBox4()


    @pyqtSlot()
    def on_pushButton5_clicked(self):
        up = self.lineEdit_2.text()
        down = self.lineEdit_3.text()
        threads = self.lineEdit_4.text()
        change__delay_config(up,down,threads)
        print('Set sleep time success')



    # def on_lineEdit_selectionChanged(self):
    #     self.lineEdit.setText('')

    # def on_lineEdit_editingFinished(self):
    #     self.lineEdit.setText('')

def main():
    up.main()
    print('111')
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)
    ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())

# def Add_new_module_test():
#     Offer_name = 'Health(Done)'
#     Offer_config_new = {"Mission_Id": "10010", "Excel": ["Auto", ""]}
#     Add_New_Config(Offer_name,Offer_config_new)
#     Alliance = 'Adsmain'
#     New_Offers = [Offer_name]
#     Add_New_Offer(Alliance,New_Offers)

def Update_Offer_config():
    pass



def change__delay_config(up,down,threads):
    try:
        up = int(up)
    except:
        up=0
    try:
        down = int(down)
    except:
        down = 0
    try:
        threads = int(threads)
    except:
        threads = 5
    file_Offer_config = r'ini\Offer_config.ini'
    Offer_config = Read_Ini(file_Offer_config)
    Offer_config['Delay'] = {}
    Offer_config['Delay']['up'] = up
    Offer_config['Delay']['down'] = down
    Offer_config['Delay']['threads']= threads
    Offer_config['Email_list'] = {}
    Offer_config['Email_list']['hotmail.com'] = 1
    Offer_config['Email_list']['outlook.com'] = 1
    Offer_config['Email_list']['yahoo.com'] = 1
    Offer_config['Email_list']['aol.com'] = 1
    Write_Ini(file_Offer_config,Offer_config)



if __name__ == '__main__':
    main()
    # Write_Offer_config()


    # Add_new_module_test()
    # Alliance = 'Offer18'
    # New_Offers = ['Stripchat(Done)']
    # Add_New_Offer(Alliance,New_Offers)    

    # new_link = {'Offer':'1.Stripchat(Done)'}
    # new_link['Alliance'] = 'Finaff'
    # new_link['url_link'] = 'http'
    # Add_New_Link(new_link,0)




