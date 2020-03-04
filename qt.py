import Chrome_driver
import Dadao
import json
import luminati
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
import Update_config as upc
import db
import email_imap
import Auto_update
import Alliance_login
from time import sleep
import Input_Config
import Submit_handle

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

def replace_links():
    file_Offer_link = r'..\res\Offer_link.ini'    
    file_Offer_link_all = r'..\res\Offer_all_links.ini'
    Offer_link = Read_Ini(file_Offer_link)
    Offer_link_all = Read_Ini(file_Offer_link_all)
    for item in Offer_link:
        if 'Mission_time' not in Offer_link[item]:
            Offer_link[item]['Mission_time'] = 1
            Offer_link[item]['Activate_status'] = 1 
    for item in Offer_link_all:
        if 'Mission_time' not in Offer_link_all[item]:
            Offer_link_all[item]['Mission_time'] = 1
            Offer_link_all[item]['Activate_status'] = 1        
    Write_Ini(file_Offer_link,Offer_link)            
    Write_Ini(file_Offer_link_all,Offer_link_all)            

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
        replace_links()
        account = db.get_account()
        self.vc_range = account['vc_range']
        print(self.vc_range) 
        # self.offer.sort()       
        items = [item for item in self.offer]
        items.sort(key=str.lower)
        for item in items:
            if i >= end:
                break
            self.comboBox1.addItem("")
            self.comboBox1.setItemText(i, _translate("MainWindow", item))
            i+=1
        self.set_comboBox2()
        self.set_text_working_links()
        self.set_text_all_links()
        self.set_comboBox3()
        self.set_comboBox4()
        self.setWindowTitle('EMU_MultiMission')
        self.accounts = Alliance_login.Get_roboform_account()
        self.set_comboBox6()
        self.set_comboBox5()
        # reply = QMessageBox.information(self,
        #           "消息框标题", 
        #           "这是一条消息。", 
        #           QMessageBox.Yes | QMessageBox.No)
        # self.resize(500,300)   
  
    def set_comboBox6(self):
        _translate = QtCore.QCoreApplication.translate    
        num_accounts = len(self.accounts)
        for i in range(num_accounts):
            self.comboBox6.addItem("")
            self.comboBox6.setItemText(i, _translate("MainWindow",str(i+1)))            

    def set_comboBox5(self):
        print('=======')
        countrys_dict = Chrome_driver.get_all_country()
        countrys = [country for country in countrys_dict]
        print(countrys)
        _translate = QtCore.QCoreApplication.translate    
        length_country = len(countrys)
        for i in range(length_country):
            self.comboBox5.addItem("")
            self.comboBox5.setItemText(i, _translate("MainWindow",countrys[i])) 

    def set_comboBox2(self):
        _translate = QtCore.QCoreApplication.translate
        j = 0
        self.comboBox2.clear()
        # print('========')
        item = self.comboBox1.currentText()
        if item != '':
            self.offer[item].sort(key=str.lower)
            for offer_ in self.offer[item]:
                if j >= len(self.offer[item]):
                    break                
                self.comboBox2.addItem("")
                self.comboBox2.setItemText(j, _translate("MainWindow", str(j+1)+'.'+offer_))            
                j+=1
    
    def set_comboBox25(self):
        _translate = QtCore.QCoreApplication.translate
        generate_dict = Input_Config.get_generate_items()
        items = [item for item in generate_dict]
        print(items)
        self.comboBox25.clear()
        self.comboBox25.addItem("")
        self.comboBox25.setItemText(0, _translate("MainWindow", 'False'))
        for j in range(len(items)):
            self.comboBox25.addItem("")
            self.comboBox25.setItemText(j+1, _translate("MainWindow", items[j]))

    def set_comboBox3(self):
        _translate = QtCore.QCoreApplication.translate      
        j = 0
        # print('set_comboBox3')
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
        # print('set_comboBox4')
        self.comboBox4.clear()
        self.offer_link_all = Read_Ini(self.file_Offer_link)
        for item in self.offer_link_all:
            if j >= len(self.offer_link_all):
                break                
            self.comboBox4.addItem("")
            self.comboBox4.setItemText(j, _translate("MainWindow", str(int(item)+1)))            
            j+=1

    def set_comboBox21(self):
        import Input_Config        
        _translate = QtCore.QCoreApplication.translate
        key = self.comboBox20.currentText()
        if key == 'False':
            key = self.comboBox25.currentText()
            if key == 'False':
                return
            else:
                methods = Input_Config.get_generate_config(key)

        else:
            methods = Input_Config.get_input_config(key)
        self.comboBox21.clear()
        self.comboBox21.addItem("")
        self.comboBox21.setItemText(0, _translate("MainWindow", 'False'))
        for j in range(len(methods)):
            self.comboBox21.addItem("")
            self.comboBox21.setItemText(j+1, _translate("MainWindow", methods[j]))

    def set_comboBox24(self):
        import Input_Config
        _translate = QtCore.QCoreApplication.translate
        key = self.comboBox19.currentText()
        methods = Input_Config.get_select_config(key)
        self.comboBox24.clear()
        self.comboBox24.addItem("")
        self.comboBox24.setItemText(0, _translate("MainWindow", 'False'))
        for j in range(len(methods)):
            self.comboBox24.addItem("")
            self.comboBox24.setItemText(j+1, _translate("MainWindow", methods[j]))


    def set_text_working_links(self):
        self.file_Offer_link = r'..\res\Offer_link.ini'
        self.offer_link = Read_Ini(self.file_Offer_link)
        text = 'Already in config links\n'
        for item in self.offer_link:
            if 'Account' not in self.offer_link[item]:
                self.offer_link[item]['Account'] = 'Not set'
            if 'Record' not in self.offer_link[item]:
                self.offer_link[item]['Record'] = '0'                
            text += str(int(item)+1)+' : '+self.offer_link[item]['Alliance']+'-->> '+'Account'+self.offer_link[item]['Account']+'-->>'+self.offer_link[item]['Offer']+'-->>'+self.offer_link[item]['Country']+'-->>run'+str(self.offer_link[item]['Mission_time'])+'times-->>Activate_status:'+str(self.offer_link[item]['Activate_status'])+'--->Record type:'+str(self.offer_link[item]['Record'])+'\n     '+str(self.offer_link[item]['url_link'])+'\n'            
        self.textBrowser2.setText(text)        

    def set_text_all_links(self):
        self.file_Offer_link_all = r'..\res\Offer_all_links.ini'
        self.offer_link_all = Read_Ini(self.file_Offer_link_all)
        text = 'Already in config links\n'
        for item in self.offer_link_all:
            if 'Account' not in self.offer_link_all[item]:
                self.offer_link_all[item]['Account'] = 'Not set'  
            if 'Record' not in self.offer_link_all[item]:
                self.offer_link_all[item]['Record'] = '0'                 
            text += str(int(item)+1)+' : '+self.offer_link_all[item]['Alliance']+'-->> '+'Account'+self.offer_link_all[item]['Account']+'-->>'+self.offer_link_all[item]['Offer']+'-->>'+self.offer_link_all[item]['Country']+'-->>run'+str(self.offer_link_all[item]['Mission_time'])+'times-->>Activate_status:'+str(self.offer_link_all[item]['Activate_status'])+'--->Record type:'+str(self.offer_link_all[item]['Record'])+'\n     '+self.offer_link_all[item]['url_link']+'\n'
        self.textBrowser1.setText(text) 

    # @pyqtSlot()
    def on_comboBox1_currentIndexChanged(self):
        # print('----------')
        self.set_comboBox2()
        print(self.comboBox2.currentText())
        self.set_lineEdit13()
        alliance_name = self.comboBox1.currentText()
        self.lineEdit37.setText(alliance_name)
        if self.comboBox2.currentText() == '':
            return 

    def on_comboBox2_currentIndexChanged(self):
        self.set_lineEdit13()

    def set_lineEdit13(self):
        # print('----------')
        Mission_Id = ''
        offer_ = self.comboBox2.currentText()
        if offer_ != '':
            print(offer_)
            offer = offer_.split('.')[1]
            Mission_Id = self.Offer_config[offer]['Mission_Id']        
        self.lineEdit13.setText(str(Mission_Id))


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
        new_offer['Account'] = self.comboBox9.currentText()
        new_offer['Mission_time'] = self.comboBox12.currentText()
        new_offer['zone'] = self.comboBox15.currentText()        
        # new_offer['Record'] = self.comboBox23.currentText()                
        new_offer['traffic_method'] = self.comboBox34.currentText()                        
        if new_offer['traffic_method'] == 'Web':
            Mission_Id = self.lineEdit13.text()
            country = new_offer['Country']
            traffic_key = db.get_traffic_key(Mission_Id,country) 
            if traffic_key == '':
                self.alert('No web traffic_key in database')
                return             
            new_offer['traffic_key'] = traffic_key          
        if self.comboBox13.currentText() == 'Yes':
            new_offer['Activate_status'] = 1
        else:
            new_offer['Activate_status'] = 0
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
        self.set_text_working_links()
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
        self.set_text_working_links()
        self.set_comboBox4()


    @pyqtSlot()
    def on_pushButton4_clicked(self):
        key = self.comboBox4.currentText()
        if key == '':
            return
        key = int(key) - 1 
        Delete_Link(key)
        self.set_text_working_links()
        self.set_comboBox4()


    @pyqtSlot()
    def on_pushButton5_clicked(self):
        up = self.lineEdit_2.text()
        down = self.lineEdit_3.text()
        threads = self.lineEdit_4.text()
        change__delay_config(up,down,threads)
        print('Set sleep time success')


    @pyqtSlot()
    def on_pushButton6_clicked(self):
        print('start init db')
        # db.init()
        command = '''start cmd /k "python db.pyc "{$name$:$qcy$}" && exit"'''
        os.system(command)        
        command = '''start cmd /k "python db.py "{$name$:$qcy$}" && exit"'''
        os.system(command)        


    @pyqtSlot()
    def on_pushButton7_clicked(self):
        print('start delete bad email ')
        command = '''start cmd /k "python email_imap.py "{$name$:$qcy$}" && exit"'''
        os.system(command)        
        command = '''start cmd /k "python email_imap.pyc "{$name$:$qcy$}" && exit"'''        
        os.system(command)
        # (?# f = os.popen(r'python email_imap.py','r'))
        # self.textBrowser1.setText(f.read()) 
        # f.close()

    @pyqtSlot()
    def on_pushButton8_clicked(self):
        self.excels,self.emails,self.Missions = db.read_all_info()
        print(self.emails)        
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
        keys.sort(key=str.lower)
        print('keys of Missions')
        print(keys)
        # print(self.Missions[keys[row]])
        for row in range(len(self.Missions)):
            print(str(keys[row]))
            item=QtGui.QStandardItem(str(keys[row]))
            #设置每个位置的文本值
            self.model.setItem(row,0,item)          
            # print('+++++++++++++')
            print(self.Offer_config)
            for offer in self.Offer_config:
                if offer == 'Delay' or offer == 'Email_list':
                    continue
                print(offer,self.Offer_config[offer]['Mission_Id'],str(keys[row]))                    
                if str(self.Offer_config[offer]['Mission_Id']) == str(keys[row]):
                    # print('===========')
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
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 
        print(self.excels,self.emails,self.Missions)
        #设置布局
        # layout=QtWidgets.QVBoxLayout()
        # layout.addWidget(self.tableView)
        # self.setLayout(layout)  
        # print('===========++++')    


    def set_table2(self):
        Alliance,site,Alliance_dict = Alliance_login.Get_Alliance_name()
        excel_list = ['Alliance','site']
        self.model=QtGui.QStandardItemModel(200,4)
        self.model.setHorizontalHeaderLabels(excel_list)
        for row in range(len(Alliance)):
            item=QtGui.QStandardItem(Alliance[row])
            #设置每个位置的文本值
            self.model.setItem(row,0,item)         
            item=QtGui.QStandardItem(site[row])
            #设置每个位置的文本值
            self.model.setItem(row,1,item) 
        self.tableView_2.setModel(self.model) 
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  


    # def set_table3(self):
    #     Alliance,site,Alliance_dict = Alliance_login.Get_Alliance_name()
    #     excel_list = ['Excel','Num','In use',]
    #     self.model=QtGui.QStandardItemModel(200,4)
    #     self.model.setHorizontalHeaderLabels(excel_list)
    #     for row in range(len(Alliance)):
    #         item=QtGui.QStandardItem(Alliance[row])
    #         #设置每个位置的文本值
    #         self.model.setItem(row,0,item)         
    #         item=QtGui.QStandardItem(site[row])
    #         #设置每个位置的文本值
    #         self.model.setItem(row,1,item) 
    #     self.tableView_2.setModel(self.model) 
    #     self.tableView_2.horizontalHeader().setStretchLastSection(True)
    #     self.tableView_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    @pyqtSlot()
    def on_pushButton9_clicked(self):
        i = self.comboBox6.currentText()
        print('Select accounts',i)
        print('start open 10 Alliance once,push next to go on ')
        command = '''start cmd /k "python Alliance_login.py %s "{$name$:$qcy$}" && exit"'''%(str(i))
        os.system(command)
        command = '''start cmd /k "python Alliance_login.pyc %s "{$name$:$qcy$}" && exit"'''%(str(i))
        os.system(command)

    @pyqtSlot()
    def on_pushButton11_clicked(self):
        if self.lineEdit11.text() != '':
            plan_id = int(self.lineEdit11.text())
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return
        self.file_Offer_link = r'..\res\Offer_link.ini'
        self.offer_link = Read_Ini(self.file_Offer_link)
        # print(Offer_links)
        try:
            plans = luminati.create_plan_data(plan_id,self.offer_link)
        except Exception as e:
            self.alert(str(e))
        print(plans)
        print('=============')
        db.upload_plans(plans)                    
        print('Uploading finished')

    @pyqtSlot()
    def on_pushButton12_clicked(self):
        if self.lineEdit8.text() != '':
            plan_id = int(self.lineEdit8.text())
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return
        plans = db.read_plans(plan_id)
        print('read plan finished')
        ports = [plan['port_lpm'] for plan in plans]
        print('start delete ports')
        luminati.delete_port(ports)
        db.clean_table(plan_id)

    @pyqtSlot()
    def on_pushButton13_clicked(self):
        i = self.comboBox6.currentText()
        print('start open test link ')
        command = '''start cmd /k "python luminati_main.py  %s "{$name$:$qcy$}" && exit"'''%(str(i))
        os.system(command)        
        command = '''start cmd /k "python luminati_main.pyc  %s "{$name$:$qcy$}" && exit"'''%(str(i))
        os.system(command)

    @pyqtSlot()
    def on_pushButton14_clicked(self):
        if self.lineEdit8.text() !='':
            plan_id = int(self.lineEdit8.text())
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return
        # plans = db.read_plans(plan_id)
        # ports = [plan['port_lpm'] for plan in plans]
        luminati.delete_port()
        for i in range(30):
            db.clean_table(i)

    # def on_lineEdit_selectionChanged(self):
    #     self.lineEdit.setText('')

    # def on_lineEdit_editingFinished(self):
    #     self.lineEdit.setText('')
    def on_comboBox6_currentIndexChanged(self):
        # print('----------')
        i = self.comboBox6.currentText()  
        if i == '':
            i = 1      
        self.set_table2()
        self.lineEdit_5.setText(self.accounts[int(i)-1]['name_roboform'])
        self.lineEdit_6.setText(self.accounts[int(i)-1]['pwd_roboform'])
        self.lineEdit_7.setText(self.accounts[int(i)-1]['Country'])

    @pyqtSlot()
    def on_pushButton15_clicked(self):
        plan_id = int(self.comboBox10.currentText())
        if plan_id != '':
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return
        print('start open test link ')
        command = '''start cmd /k "python hotupdate.py  %s "{$name$:$qcy$}" && exit"'''%(str(plan_id))
        os.system(command)
        command = '''start cmd /k "python hotupdate.pyc %s "{$name$:$qcy$}" && exit"'''%(str(plan_id))
        os.system(command)

    @pyqtSlot()
    def on_pushButton16_clicked(self):
        plan_id = int(self.lineEdit9.text())
        if plan_id != '':
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return
        print('start open test link ')
        command = '''start cmd /k "python traffic.py  %s "{$name$:$qcy$}" && exit"'''%(str(plan_id))
        os.system(command)
        command = '''start cmd /k "python traffic.pyc  %s "{$name$:$qcy$}" && exit"'''%(str(plan_id))
        os.system(command)        

    @pyqtSlot()
    def on_pushButton17_clicked(self):
        plan_id = int(self.lineEdit10.text())
        if plan_id != '':
            if plan_id < int(self.vc_range[0]) or plan_id > int(self.vc_range[1]):
                print("plan_id not in vc_range")
                return
        else:
            return  
        print('start activate plan',str(plan_id))
        command = '''start cmd /k "python Activate.py %s "{$name$:$qcy$}" && exit"'''%(str(plan_id))
        os.system(command)
        command = '''start cmd /k "python Activate.pyc %s "{$name$:$qcy$}" && exit"'''  %(str(plan_id))      
        os.system(command)

    @pyqtSlot()
    def on_pushButton18_clicked(self):
        # plans = db.read_plans(plan_id)
        # ports = [plan['port_lpm'] for plan in plans]
        luminati.delete_port()

    @pyqtSlot()
    def on_pushButton19_clicked(self):
        Mission_Id = int(self.lineEdit12.text())
        db.read_pic(Mission_Id)
        db.read_txt_traceback(Mission_Id)
        os.system('explorer.exe /n, C:\EMU\log\pics\\'+str(Mission_Id))

    @pyqtSlot()
    def on_pushButton20_clicked(self):
        print('start Dadao')
        chrome_driver = Alliance_login.get_chrome('',None,1)
        QApplication.processEvents()               
        sleep(5000)  

    @pyqtSlot()
    def on_pushButton21_clicked(self):
        db.update_flag_use_all()
        reply = QMessageBox.information(self,
                  "Message", 
                  "Flag clean finished", 
                  QMessageBox.Yes | QMessageBox.No)        
        print(reply)

    def alert(self,info):
            reply = QMessageBox.information(self,
                  "Message", 
                  str(info), 
                  QMessageBox.Ok)

    def get_general_config(self,flag):
        flag['Mission_Id'] = str(self.lineEdit13.text())        
        flag['Page'] = self.comboBox7.currentText()
        if self.lineEdit18.text() == '':
            flag['Step'] = self.comboBox17.currentText()
        else:
            flag['Step'] = self.lineEdit18.text()
        flag['Action'] = self.comboBox8.currentText()
        flag['General'] = {}
        flag['General']['scroll'] = self.comboBox11.currentText() 
        flag['General']['try'] = self.comboBox16.currentText() 
        # flag['General']['xpath'] = self.lineEdit17.text()
        flag['General']['father_type'] = self.comboBox30.currentText()        
        flag['General']['father_content'] = self.lineEdit31.text()
        flag['General']['child_type'] = self.comboBox31.currentText()        
        flag['General']['child_content'] = self.lineEdit32.text()        

        # flag['General']['class_name'] = self.lineEdit27.text()        
        # flag['General']['hidden_xpath'] = self.lineEdit25.text()        
        # flag['General']['tagname'] = self.lineEdit26.text()                
        flag['General']['iframe'] = self.lineEdit23.text()
        flag['General']['detect'] = self.comboBox29.currentText()
        return flag
 
    @pyqtSlot()
    def on_pushButton22_clicked(self):
        '''
        Recorder_Click
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Action'] = 'Click'
        flag['Step_config'] = {}
        flag['Step_config']['click'] = self.comboBox33.currentText()
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add click config success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton23_clicked(self):
        flag = {}
        flag['Page'] = self.comboBox7.currentText()
        flag['Flag_text'] = self.lineEdit14.text()
        flag['Flag_xpath'] = self.lineEdit15.text()
        flag['Iframe'] = self.lineEdit28.text()        
        flag['Status'] = self.comboBox22.currentText()
        flag['Country'] = self.comboBox5.currentText()        
        flag['Quotes'] = self.comboBox32.currentText()        
        print(flag)
        Mission_Id = str(self.lineEdit13.text())
        try:
            db.upload_pageflag(Mission_Id,flag)
            self.alert("Add page flag success")
        except Exception as e:
            self.alert(str(e))
         
    @pyqtSlot()
    def on_pushButton24_clicked(self):
        Page = self.comboBox7.currentText()
        print(Page)
        Mission_Id = str(self.lineEdit13.text())
        try:
            db.delete_page_flag(Mission_Id,Page)
            self.alert("Delete page flag success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton25_clicked(self):
        Page = self.comboBox7.currentText()
        print(Page)
        Mission_Id = str(self.lineEdit13.text())
        try:
            db.delete_page(Mission_Id,Page)
            self.alert("Delete page success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton26_clicked(self):
        Page = self.comboBox7.currentText()
        print(Page)
        Mission_Id = str(self.lineEdit13.text())
        if self.lineEdit18.text() == '':
            Step = self.comboBox17.currentText()
        else:
            Step = self.lineEdit18.text()        
        try:
            flag = db.delete_step(Mission_Id,Page,Step)
            if flag == -1:
                self.alert('Duplicated step found,please try again')
            else:
                self.alert("Delete step success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton27_clicked(self):
        '''
        Recorder_Select
        '''
        text = self.textEdit.toPlainText() 
        print(text)
        inputs = text.split('\n')
        print(inputs)
        flag = {}
        try:        
            data = self.get_general_config(flag)
            data['Action'] = 'Select'
            data['Step_config'] = {}    
            data['Step_config']['select_index'] = self.lineEdit19.text()
            data['Step_config']['select_index_rand'] = self.comboBox18.currentText()
            data['Step_config']['select_value'] = self.comboBox19.currentText()
            data['Step_config']['select_func'] = self.comboBox24.currentText()            
            data['Step_config']['select_value_range'] = ['','']
            data['Step_config']['select_value_range'][0] = self.lineEdit20.text()
            data['Step_config']['select_value_range'][1] = self.lineEdit21.text()   
            data['Step_config']['select_value_content'] = inputs 
            print('data',data)     
            flag_upload = db.upload_pageconfig(data)
            if flag_upload == -1:
                self.alert("Duplicated step")  
            else:              
                self.alert("Add Select config success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton29_clicked(self):
        _translate = QtCore.QCoreApplication.translate
        j = 0
        self.comboBox19.clear()
        self.comboBox20.clear()        
        # print('========')
        Mission_Id = self.lineEdit13.text()
        print(Mission_Id)
        keys = []
        configs = self.Offer_config
        for item in configs:
            if 'Mission_Id' in configs[item]:
                print(item)
                if str(configs[item]['Mission_Id']) == str(Mission_Id):
                    if configs[item]['Excel'][0] == 'Dadao':
                        path = r'..\res\Dadao.xlsx' 
                        sheet,workbook = Dadao.get_excel(path)   
                        submit_ = Dadao.get_one_data(sheet,Mission_Id)
                        print(submit_)
                        submit_['Mission_Id'] = Mission_Id 
                        submit = {}
                        submit['Dadao'] = submit_
                    else:
                        Mission_list = [100]
                        Excel_name = configs[item]['Excel']
                        Email_list = ['hotmail.com','outlook.com','yahoo.com','aol.com','gmail.com']
                        submit = db.read_one_excel(Mission_list,Excel_name,Email_list)                        
                    for excel in submit:
                        keys = [item_ for item_ in submit[excel] if submit[excel][item_]!=None and submit[excel][item_] !='']
            else:
                # print('Mission_Id'+str(Mission_Id)+' not in item')
                pass
        if keys != []:
            keys.sort(key=str.lower)
            for j in range(len(keys)):
                self.comboBox19.addItem("")
                self.comboBox19.setItemText(j, _translate("MainWindow", keys[j]))                    
                self.comboBox20.addItem("")
                self.comboBox20.setItemText(j, _translate("MainWindow", keys[j]))                         
            self.comboBox19.addItem("")
            self.comboBox19.setItemText(j+1, _translate("MainWindow", 'False'))                    
            self.comboBox20.addItem("")
            self.comboBox20.setItemText(j+1, _translate("MainWindow", 'False'))  
        self.set_comboBox25()                  

    @pyqtSlot()
    def on_pushButton28_clicked(self):
        '''
        Recorder_Select
        '''
        flag = {}
        try:        
            data = self.get_general_config(flag)
            data['Action'] = 'Input'
            data['Step_config'] = {}    
            data['Step_config']['input_key'] = self.comboBox20.currentText()
            data['Step_config']['input_generate'] = self.comboBox25.currentText()
            data['Step_config']['input_func'] = self.comboBox21.currentText()
            data['Step_config']['input_content'] = self.lineEdit22.text()
            flag_check = 0
            print(data)
            for item in data['Step_config']:
                if data['Step_config'][item] != '' and data['Step_config'][item] != 'False':
                    flag_check = 1
                    break
            print(flag_check)
            if flag_check == 0:
                content = 'Bad config,all false or empty are not allowed! '
                self.alert(content)
                return
            # data['Step_config']['select_index_rand'] = self.comboBox18.currentText()
            # data['Step_config']['select_value'] = self.comboBox19.currentText()
            # data['Step_config']['select_value_range'] = ['','']
            # data['Step_config']['select_value_range'][0] = self.lineEdit20.text()
            # data['Step_config']['select_value_range'][1] = self.lineEdit21.text()   
            # print('data',data)     
            flag_upload = db.upload_pageconfig(data)
            if flag_upload == -1:
                self.alert("Duplicated Step")  
            else:              
                self.alert("Add Input config success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton31_clicked(self):
        '''
        set status
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add setstatus config success")
        except Exception as e:
            self.alert(str(e))        

    @pyqtSlot()
    def on_pushButton32_clicked(self):
        '''
        add set sleep
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        print('str(self.lineEdit24.text):')
        print(self.lineEdit24.text())
        flag['Step_config']['sleep'] = str(self.lineEdit24.text())
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add set sleep config success")
        except Exception as e:
            self.alert(str(e))   

    @pyqtSlot()
    def on_pushButton33_clicked(self):
        '''
        add set sleep
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add set cookie config success")
        except Exception as e:
            self.alert(str(e))   

    @pyqtSlot()
    def on_pushButton34_clicked(self):
        '''
        add set sleep
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add set refresh config success")
        except Exception as e:
            self.alert(str(e))     

    @pyqtSlot()
    def on_pushButton35_clicked(self):
        '''
        add set Alert
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add set Alert config success")
        except Exception as e:
            self.alert(str(e))                     

    @pyqtSlot()
    def on_pushButton30_clicked(self):
        account = luminati.get_account()
        ip = account['IP_lpm']        
        ports_used = luminati.ports_get(ip)        
        self.alert('Total %d ports using.'%int(len(ports_used)))

    def on_comboBox20_currentIndexChanged(self):
        # print('----------')
        self.set_comboBox21()

    def on_comboBox25_currentIndexChanged(self):
        # print('----------')
        self.set_comboBox21()

    def on_comboBox19_currentIndexChanged(self):
        # print('----------')
        self.set_comboBox24()


    def on_comboBox21_currentIndexChanged(self):
        # print('----------')
        method = self.comboBox21.currentText()
        if method != 'False' and method != '':
            doc = eval('Submit_handle.' + method + '.__doc__')
            text = 'Rules:\n'+doc
            self.textBrowser3.setText(text)
        else:
            text = 'Rules:\n'
            self.textBrowser3.setText(text)

    def on_comboBox24_currentIndexChanged(self):
        # print('----------')
        method = self.comboBox24.currentText()
        if method != 'False' and method != '':
            doc = eval('Submit_handle.' + method + '.__doc__')
            text = 'Rules:\n'+doc
            self.textBrowser4.setText(text)
        else:
            text = 'Rules:\n'
            self.textBrowser4.setText(text)


    @pyqtSlot()
    def on_pushButton36_clicked(self):
        country = self.comboBox5.currentText()
        submit = {}
        submit['Country'] = country
        submit['Mission_Id'] = 10000
        chrome_driver = Chrome_driver.get_chrome(submit,1)
        url = self.lineEdit.text()
        chrome_driver.get(url)
        sleep(3000)

    @pyqtSlot()
    def on_pushButton37_clicked(self):
        '''
        Recorder_Js
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        elem_id = self.lineEdit29.text()
        js_remove = 'document.getElementById("%s").removeAttribute("readonly")'%elem_id
        js_set_value = 'document.getElementById("%s").value="'%(elem_id)
        flag['Step_config']['js_remove'] = js_remove
        flag['Step_config']['js_set_value'] = js_set_value
        flag['Step_config']['content'] = self.comboBox35.currentText()        
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add click config success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton38_clicked(self):
        '''
        Recorder_Js
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add change page success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton39_clicked(self):
        '''
        Recorder_Js
        '''
        Mission_Id = str(self.lineEdit13.text()) 
        states = self.lineEdit30.text().split(',')
        submit = {}
        submit['Mission_Id'] = Mission_Id
        submit['states'] = states
        configs = self.Offer_config
        for item in configs:
            if 'Mission_Id' in configs[item]:
                if str(configs[item]['Mission_Id']) == str(Mission_Id):
                    Mission_list = [100]
                    Excel_name = configs[item]['Excel']   
                    break     
        print('==========')
        if Excel_name[0] == '':
            self.alert('No excel for this Mission')
            return
        submit['Excel_name'] = Excel_name[0]       
        print('Find target excel:',submit['Excel_name'])
        infos = db.unchosse_states(submit)
        # print(infos)

    @pyqtSlot()
    def on_pushButton40_clicked(self):
        '''
        Recorder_Js
        '''
        flag = {}
        flag = self.get_general_config(flag)
        flag['Step_config'] = {}
        try:
            flag = db.upload_pageconfig(flag)
            self.alert("Add change page success")
        except Exception as e:
            self.alert(str(e))

    @pyqtSlot()
    def on_pushButton41_clicked(self):
        Mission_Id = self.lineEdit13.text()
        country = self.comboBox5.currentText()
        key = self.lineEdit33.text()
        if Mission_Id == '' or country == '' or key == '':
            self.alert('Check country,Mission_Id and key content')
            return        
        try:
            flag = db.upload_traffic_keys(Mission_Id,country,key)
            self.alert("Add traffic_key success")
        except Exception as e:
            self.alert(str(e))        

    @pyqtSlot()
    def on_pushButton42_clicked(self):
        Mission_Id = self.lineEdit34.text().replace('\n','')
        Mission_name = self.lineEdit35.text().replace('\n','')
        bad_alpha = ['.','"',"'"]
        for item in bad_alpha:
            if item in Mission_name:
                self.alert(item+' not allowed in Offer name') 
                return
        Excel = ['','']
        excel = self.comboBox36.currentText()
        if excel != 'Email':
            Excel[1] = excel
        try:
            db.upload_offer(Mission_name,Mission_Id,Excel)
            # db.update_version()
            self.alert("Add Offer Info success")
        except Exception as e:
            self.alert(str(e)) 

    @pyqtSlot()
    def on_pushButton43_clicked(self):
        Mission_Id = self.lineEdit34.text().replace('\n','')
        try:
            db.delete_offer_config(Mission_Id)
            # db.update_version()
            self.alert("DELETE Offer Info success")
        except Exception as e:
            self.alert(str(e))             

    @pyqtSlot()
    def on_pushButton44_clicked(self):
        Mission_Id = self.lineEdit36.text().replace('\n','')
        Alliance_name = self.lineEdit37.text().replace('\n','')
        if Mission_Id == '' or Alliance_name == '':
            self.alert('Mission_Id and Alliance_name needed')
            return        
        try:
            db.upload_alliance(Alliance_name,Mission_Id)
            # db.update_version()
            self.alert("Add Alliance Info success")
        except Exception as e:
            self.alert(str(e)) 

    @pyqtSlot()
    def on_pushButton45_clicked(self):
        Mission_Id = self.lineEdit36.text().replace('\n','')
        Alliance_name = self.lineEdit37.text().replace('\n','')
        if Mission_Id == '' or Alliance_name == '':
            self.alert('Mission_Id and Alliance_name needed')
            return
        try:
            res = db.delete_alliance_config(Alliance_name,Mission_Id)
            print(res)
            # if len(res[0]) == 0:
            #     self.alert("No target Mission_Id or Alliance_name found")
            # else:
            # db.update_version()
            self.alert("DELETE Alliance Info success")                
        except Exception as e:
            self.alert(str(e))   

    @pyqtSlot()
    def on_pushButton46_clicked(self):
        print('start init db')
        # db.init()
        Mission_Id = self.lineEdit13.text()
        if Mission_Id == '':
            self.alert('Choose Mission_Id')
            return
        command = '''start cmd /k "python test.py 3 %s "{$name$:$qcy$}" "'''%(str(Mission_Id))
        os.system(command)        
        command = '''start cmd /k "python test.pyc 3 %s "{$name$:$qcy$}" "'''%(str(Mission_Id))
        os.system(command)  

def test_k():
    file = r'ini\Offer_num.ini'
    with open(file,'a+') as f:
        offers = f.readlines()
        print(offers)
        nums = []
        for line in offers:
            num_ = line.split(',')
            if len(num_) >= 3:
                num_mission = num_[0]
                nums.append(num_mission)
        print(nums)

def main(i,message=''):
    # up.main()
    print('Updating config...')
    try:
        upc.update_config()
    except Exception as e:
        print(str(e))
        print('Updating config failed')
        return
    print('Updating config success')
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    # MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    # MainWindow.setFixedSize(MainWindow.width(), MainWindow.height());  
    ui = Mywindow(MainWindow)                          # ui是你创建的ui类的实例化对象
    # ui.setupUi(MainWindow)   # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # ui.pushButton.clicked.connect(test_sig)
    if i == 0:
        ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
        sys.exit(app.exec_())
    else:
        if message != '':
            message += '\n'*30+' '*100
            ui.alert(message)
            ui.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
        sys.exit(app.exec_())

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
    i = 0
    # message = 'test'+'\n'*30+' '*100
    message = ''
    main(i,message)





