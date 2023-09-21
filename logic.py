from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from ui import *
import os
import xlwt
from server import *
import pickle
import base64
import sys
class ui_with_logic_class(Ui_MainWindow):
     
    def __init__(self,mainwindow:QtWidgets.QMainWindow) -> None:
        self.save_path=os.environ['USERPROFILE']+"\\.transcript_sending_tool" 
        self.server=server_class()
        self.setupUi(mainwindow)
        self.set_connect() #绑定按钮事件
        self.show_how_to_use() #展示帮助
        self.set_table_unedit() #使得表格第一列第二列不可编辑
        self.textEdit_3.setText("同学") #信件默认内容
        self.textEdit.setText("以下是您的成绩单，请查收")
        self.textEdit_2.setText("请继续努力")
        self.textEdit_4.setText("班委")
        self.textEdit_title.setText("成绩单")
        self.load() #载入保存的信息（发送者邮箱，授权码等）
        self.now_choose_student="" #当前被操作的学生。
    
    def show_how_to_use(self):
        self.textBrowser_2.setOpenExternalLinks(True)
        word="""
        <p> 本软件由刘德龙(QQ:1589075757)独立完成<p>
        <p> 如有任何疑问、建议，欢迎联系作者 <p>
        <p> 以下为使用说明 <p>
        <h3> 第一步（仅首次使用需要进行） </h3>
        <p> 获取您邮箱的授权码，软件需要得到授权码才能使用您的邮箱发送邮件，方法请点击这个链接： </p>
        <a href="https://jingyan.baidu.com/article/b0b63dbf1b2ef54a49307054.html">https://jingyan.baidu.com/article/b0b63dbf1b2ef54a49307054.html</a>
        <p> 复制得到的授权码 </p>
        <h3> 第二步（仅首次使用需要进行）</h3>
        <p> 在中间“发送者邮箱”处填写自己的邮箱，然后点击"点击粘贴授权码"按钮(前提你刚复制了授权码)，然后点确认。登录成功后信息会自动保存，下次打开将自动登录，无需进行第一步第二步</p>
        <h3> 第三步 </h3>
        <p> 点击"生成成绩单"按钮,会自动打开excel,在excel中编辑成绩单。 </p>
        <p> 然后点击导入成绩单。</p>
        <h3> 第四步 </h3>
        <p> 如果需要，可以在中间处选择计算排名。标题，称呼，开头语，结束语，落款可以自定义，也可不填。</p>
        <h3> 第五步 </h3>
        <p> 点击"发送全部成绩单"按钮即可。</p>
        """
        self.textBrowser_2.setText(word)

    def load(self):
        '''
        本函数会检查save_path中时候有无init.tsti文件数据保存，如果有，则载入保存的数据并更新ui界面。
        '''
        if os.path.isdir(self.save_path):
            with open(self.save_path+"\\init.tsti","rb") as fp:
                message=pickle.load(fp)
                try:
                    self.textEdit_5.setText(message["mail"])
                    self.textEdit_6.setText(message['authcode'])
                    self.textEdit_3.setText(message["call"])
                    self.textEdit.setText(message["begin_word"])
                    self.textEdit_2.setText(message["conclusion"])
                    self.textEdit_4.setText(message["sign"])
                    self.textEdit_title.setText(message["title"])
                    self.click_login()
                except:
                    pass
    def get_mail_saying(self):
        '''此函数用于从ui中获取取标题，称呼，开头语，结束语，落款'''
        title=self.textEdit_title.toPlainText()
        if not title or title=="":
            title=""
        
        call=self.textEdit_3.toPlainText()
        if not call or call=="":
            call=""

        open_word=self.textEdit.toPlainText()
        if not open_word or open_word=="":
            open_word=""
        
        conclusion=self.textEdit_2.toPlainText()
        if not conclusion or conclusion=="":
            conclusion=""
        
        sign=self.textEdit_4.toPlainText()
        if not sign or sign=="":
            sign=""
        
        sender_name=self.textEdit_7.toPlainText()
        if not sender_name or sender_name=="":
            sender_name=""
        return title,call,open_word,conclusion,sign,sender_name
    def save(self):
        '''
        本函数用于从ui中获取标题，称呼，开头语，结束语，落款，发送者邮箱，授权码信息。并把信息保存在save_path中的init.tsti文件中。
        '''
        message={}
        title,call,begin_word,conclusion,sign=self.get_mail_saying()
        mail=self.textEdit_5.toPlainText()
        authcode=self.textEdit_6.toPlainText()
        message["mail"]=mail
        message["authcode"]=authcode
        message["call"]=call
        message["begin_word"]=begin_word
        message["conclusion"]=conclusion
        message["sign"]=sign
        message["title"]=title
        if not os.path.isdir(self.save_path):
            os.makedirs(self.save_path)
        with open(self.save_path+"/init.tsti","wb") as fp:
            pickle.dump(message,fp,0)
    
    def set_connect(self):
        '''
        此方法用来绑定按钮事件
        '''
        self.pushButton.clicked.connect(self.click_create_template_button)
        self.pushButton_2.clicked.connect(self.click_load_school_report_button)
        self.pushButton_8.clicked.connect(self.click_paste_authcode_button)
        self.pushButton_10.clicked.connect(self.click_login)
        self.pushButton_4.clicked.connect(self.click_send_all_button)
        self.pushButton_now.clicked.connect(self.click_preview_button)
        self.pushButton_next.clicked.connect(self.click_preview_next_button)
        self.pushButton_6.clicked.connect(self.click_preview_last_button)
        self.pushButton_5.clicked.connect(self.click_preview_button)
        self.pushButton_9.clicked.connect(self.click_send_one)
        self.pushButton_3.clicked.connect(self.click_send_unsend)
        self.pushButton_7.clicked.connect(self.click_cal_rank_button)

    def uprint(self,text):
        '''
        此方法可以向用户输出反馈信息。
        '''
        self.textBrowser_3.setText(text)

    def set_table_unedit(self):
        '''
        此方法用于设置表格第一列第二列不可编辑
        '''
        for i in range (self.tableWidget.rowCount()):
            item0=self.tableWidget.item(i,0)
            if item0==None:
                item0=QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i,0,item0)
            item1=self.tableWidget.item(i,1)
            if item1==None:
                item1=QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i,1,item1)
            item0.setFlags(QtCore.Qt.ItemFlag(0))
            item0.setFlags(QtCore.Qt.ItemIsEnabled)
            item1.setFlags(QtCore.Qt.ItemFlag(0))
            item1.setFlags(QtCore.Qt.ItemIsEnabled)
    
    def clear_table(self):
        '''此方法用于清空表格内容'''
        for i in range(1000):
            if(self.tableWidget.item(i,0) and self.tableWidget.item(i,1) and self.tableWidget.item(i,2)):
                self.tableWidget.item(i,0).setText("")
                self.tableWidget.item(i,1).setText("")
                self.tableWidget.item(i,2).setText("")
    
    def show_preview_by_name(self,name):
        '''此方法根据名字从服务器中获取预览并显示到ui上。'''
        self.server.set_mail_saying(*self.get_mail_saying())
        preview=self.server.get_preview_by_name(name)
        if preview:
            self.textBrowser.setText(preview)
    
    def get_unsend_student(self,status_dict):
        unsend_student_list=[]
        for student in status_dict.keys():
            if status_dict[student]=="未发送":
                unsend_student_list.append(student)
        return unsend_student_list

    def set_status(self,name,status):
        for i in range(1000):
            if self.tableWidget.item(i,1) and self.tableWidget.item(i,1).text()==name:
                self.tableWidget.item(i,2).setText(status)

    def click_create_template_button(self):
        ui.uprint("")
        work_book=xlwt.Workbook(encoding='utf-8')
        work_sheet=work_book.add_sheet("成绩单发送模板")
        for i in range(2):
            work_sheet.col(i).width=256*30
        for i in range(2,20):
            work_sheet.col(i).width=256*10
        work_sheet.row(0).height_mismatch=True
        work_sheet.row(0).height=20*40
        style=xlwt.XFStyle()
        style.alignment.wrap=1
        work_sheet.write_merge(0,0,0,1,'列名除邮箱和姓名列外,其他的科目列名可增可删可修改,编辑完成后，请保存文件',style)
        work_sheet.write(1,0,'邮箱（必填）')
        work_sheet.write(1,1,'姓名（必填）')

        for i in range(1,20):
            work_sheet.write(1,i+1,'科目'+str(i))
        try:
            if os.path.exists('成绩单发送模板.xlsx'):
                os.remove('成绩单发送模板.xlsx')
            work_book.save('成绩单发送模板.xlsx')
            os.startfile('成绩单发送模板.xlsx')
            ui.uprint("已经为您打开成绩单发送模板，请编辑\n")
        except PermissionError as err:
            ui.uprint("生成失败：另一个程序已经打开成绩单发送模板.xlsx,请关闭后重试\n")
    
    def click_load_school_report_button(self):
        self.clear_table()
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.now_choose_student=""
        if not self.server.read_school_report("成绩单发送模板.xlsx"):
            ui.uprint("找不到成绩单，请先生成成绩单模板")
            return
        sending_status_message_list=self.server.get_sending_status_message_list()
        if len(sending_status_message_list)==0:
            return
        for index, student in enumerate(sending_status_message_list):
            self.tableWidget.setItem(index,0,QTableWidgetItem(student[0]))
            self.tableWidget.setItem(index,1,QTableWidgetItem(student[1]))
            self.tableWidget.setItem(index,2,QTableWidgetItem(student[2]))
        self.comboBox_2.insertItem(0,"不计算排名") #不计算排名选项会占据引索0
        self.comboBox_2.insertItems(1,self.server.get_subject_list())
        self.comboBox_2.setCurrentIndex(0)
        # 使用self.comboBox_2.currentText()返回选择的内容。

        self.comboBox.insertItems(0,self.server.get_student_name_list())
        self.comboBox_2.setCurrentIndex(0)
        self.set_table_unedit()
        self.server.set_mail_saying(*(self.get_mail_saying()))
        preview=self.server.get_preview_by_name(sending_status_message_list[0][1])
        self.now_choose_student=sending_status_message_list[0][1]
        self.textBrowser.setText(preview)
        
    def click_paste_authcode_button(self):
        try:
            clickboard=QApplication.clipboard()
            self.textEdit_6.setText(clickboard.text())
        except:
            self.uprint("粘贴失败，请先复制正确的授权码")
    def click_login(self):
        self.uprint("正在登录，请稍候。。。")
        QApplication.processEvents()
        self.uprint(self.server.login(self.textEdit_5.toPlainText(),self.textEdit_6.toPlainText()))
        self.save()
    
    
    def get_sending_status_message_from_ui_table(self):
        sending_status_message_from_ui_table={}
        for i in range(1000):
            if self.tableWidget.item(i,1) and self.tableWidget.item(i,1).text():
                sending_status_message_from_ui_table[self.tableWidget.item(i,1).text()]=self.tableWidget.item(i,2).text()
        return sending_status_message_from_ui_table

                

    def click_send_all_button(self):
        
        if not self.server.already_login():
            self.uprint("还未确认发送者邮箱以及授权码，请先确认发送者邮箱及授权码")
            return
        self.save()
        self.uprint("开始发送成绩单...")
        QApplication.processEvents()
        title,call,open_word,conclusion,sign,sender_name=self.get_mail_saying()
        self.server.set_mail_saying(title,call,open_word,conclusion,sign,sender_name)
        send_list=self.server.get_student_name_list()
        total_number_of_student=len(send_list)
        success_send_number=0
        fail_list=[]
        for index,student in enumerate( send_list):
            preview_test=self.server.get_preview_by_name(student)
            if preview_test:
                self.textBrowser.setText(preview_test)
            success=self.server.send(student)
            if success:
                self.textBrowser_3.append(student+"成绩单发送成功\n")
                self.tableWidget.item(index,2).setText("已发送")
                success_send_number+=1
                QApplication.processEvents()
            else:
                self.textBrowser_3.append(student+"成绩单发送失败\n")
                self.tableWidget.item(index,2).setText("未发送")
                fail_list.append(student)
                QApplication.processEvents()
        self.textBrowser_3.append("共发送："+str(total_number_of_student)+" 成功："+str(success_send_number)+" 失败："+str(total_number_of_student-success_send_number)+"\n")
        if success_send_number<total_number_of_student:
            self.textBrowser_3.append("以下成绩单发送失败：")
            for student in fail_list:
                self.textBrowser_3.append(student+" ")
            self.textBrowser_3.append("\n")
    
    def click_preview_button(self):
        self.now_choose_student=self.comboBox.currentText()
        self.show_preview_by_name(self.now_choose_student)
    
    def click_preview_next_button(self):
        self.now_choose_student=self.comboBox.currentText()
        self.now_choose_student=self.server.get_next_name(self.now_choose_student)
        self.comboBox.setCurrentText(self.now_choose_student)
        self.show_preview_by_name(self.now_choose_student)

    def click_preview_last_button(self):
        self.now_choose_student=self.comboBox.currentText()
        self.now_choose_student=self.server.get_last_name(self.now_choose_student)
        self.comboBox.setCurrentText(self.now_choose_student)
        self.show_preview_by_name(self.now_choose_student)

    def click_send_one(self):
        if not self.server.already_login():
            self.uprint("还未确认发送者邮箱以及授权码，请先确认发送者邮箱及授权码")
            return
        self.save()
        title,call,open_word,conclusion,sign,sender_name=self.get_mail_saying()
        self.server.set_mail_saying(title,call,open_word,conclusion,sign,sender_name)
        self.now_choose_student=self.comboBox.currentText()
        self.show_preview_by_name(self.now_choose_student)
        self.uprint(self.now_choose_student+"成绩单正在发送。。。")
        try:
            self.server.send(self.now_choose_student)
            self.uprint(self.now_choose_student+"成绩单发送成功")
        except:
            self.uprint(self.now_choose_student+"成绩单发送失败")
            
    
    def click_send_unsend(self):
        if not self.server.already_login():
            self.uprint("还未确认发送者邮箱以及授权码，请先确认发送者邮箱及授权码")
            return
        title,call,open_word,conclusion,sign,sender_name=self.get_mail_saying()
        self.server.set_mail_saying(title,call,open_word,conclusion,sign,sender_name)
        self.uprint("开始发送成绩单...")
        self.save()
        sending_status_message_from_ui_table=self.get_sending_status_message_from_ui_table()
        unsend_student_list=self.get_unsend_student(sending_status_message_from_ui_table)
        number_of_unsend_student=len(unsend_student_list)
        success_send_number=0
        fail_list=[]
        for student in unsend_student_list:
            success=self.server.send(student)
            if success:
                self.textBrowser_3.append(student+"成绩单发送成功\n")
                self.set_status(student,"已发送")
                success_send_number+=1
                QApplication.processEvents()
            else:
                self.textBrowser_3.append(student+"成绩单发送失败\n")
                self.set_status(student,"未发送")
                fail_list.append(student)
                QApplication.processEvents()
        self.textBrowser_3.append("共发送："+str(number_of_unsend_student)+" 成功："+str(success_send_number)+" 失败："+str(number_of_unsend_student-success_send_number)+"\n")
        if success_send_number<number_of_unsend_student:
            self.textBrowser_3.append("以下成绩单发送失败：")
            for student in fail_list:
                self.textBrowser_3.append(student+" ")
            self.textBrowser_3.append("\n")
    def click_cal_rank_button(self):
        subject=self.comboBox_2.currentText()
        self.server.add_rank_according_to_subject(subject)
        self.show_preview_by_name(self.comboBox.currentText())
        self.now_choose_student=self.comboBox.currentText()
    
if __name__=="__main__":
 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()#获取主窗口
    ui=ui_with_logic_class(MainWindow)#配置主窗口
    MainWindow.show()
    
    sys.exit(app.exec_())