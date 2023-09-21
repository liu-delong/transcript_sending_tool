import xlrd
from ldlpkg.ldl_email_helper import * 
class server_class:
    def __init__(self) -> None:
        self.school_report={}
        self.school_report_subjects=[]
        self.school_report_students=[]
        self.sender=None
        self.title="成绩单"
        self.call="同学"
        self.open_word="以下是您的成绩单，请查收"
        self.conclusion="请继续努力"
        self.sign=""
    def read_school_report(self,school_report_file_name):
        try:
            workbook=xlrd.open_workbook(school_report_file_name)
        except:
            return False
        worksheets=workbook.sheet_names()
        school_report_sheet=workbook.sheet_by_name(worksheets[0])
        self.school_report.clear()
        self.school_report_students.clear()
        self.school_report_subjects.clear()
        for i in range(2,school_report_sheet.ncols):
            self.school_report_subjects.append(school_report_sheet.cell(1,i).value)
        for i in range(2,school_report_sheet.nrows):
            temp={}
            student_name=str(school_report_sheet.cell(i,1).value)
            temp['邮箱']=str(school_report_sheet.cell(i,0).value)
            temp['发送状态']="未发送"
            self.school_report_students.append(student_name)
            for j in range(len(self.school_report_subjects)):
                try:
                    temp[self.school_report_subjects[j]]=str(school_report_sheet.cell(i,j+2).value)
                except:
                    temp[self.school_report_subjects[j]]="none"
            self.school_report[student_name]=temp
        return True
    def get_sending_status_message_list(self):
        sending_status_message_list=[]
        for student in self.school_report_students:
            sending_status_message_for_one_student=[]
            sending_status_message_for_one_student.append(self.school_report[student]["邮箱"])
            sending_status_message_for_one_student.append(student)
            sending_status_message_for_one_student.append(self.school_report[student]["发送状态"])
            sending_status_message_list.append(sending_status_message_for_one_student)
        return sending_status_message_list
    def get_student_name_list(self):
        return self.school_report_students
    def get_subject_list(self):
        return self.school_report_subjects
    def login(self,sender_address,authcode):
        try:
            self.sender=email_sender_class(sender=sender_address,authcode=authcode,smtp_server='smtp.qq.com',smtp_sever_port=25)
        except:
            self.sender=None
            return "登录失败，请检查网络是否连接，或填写的邮箱和授权码是否均正确,然后重试"
        return "登录成功"
    def already_login(self):
        if self.sender:
            return True
        else:
            return False
    def set_mail_saying(self,title,call,open_word,conclusion,sign,sender_name):
        self.title=title
        self.call=call
        self.open_word=open_word
        self.conclusion=conclusion
        self.sign=sign
        self.sender_name=sender_name
    def create_mail(self,student):
        email=ldl_email_class(self.sender_name,self.sender.sender_address,self.title,student,self.call,self.sign)
        email.addtext(self.open_word)
        the_list=[]
        for subject in self.school_report_subjects:
            subject_tem=subject
            if subject_tem=="ldlpm":
                subject_tem="排名"
            list=[subject_tem,self.school_report[student][subject]]
            the_list.append(list)
        email.addtable(the_list,"")
        email.addtext(self.conclusion)
        email.complete_mail()
        return email
    def get_preview_by_name(self,student):
        if not (student in self.school_report_students):
            return None
        email=self.create_mail(student)
        return email.html_content.to_str()

    def send(self,student):
        if not self.sender:
            return False
        email=self.create_mail(student)
        try:
            self.sender.SendEmail(self.school_report[student]["邮箱"],email)
            self.school_report[student]["发送状态"]="已发送"
            return True
        except:
            self.school_report[student]["发送状态"]="未发送"
            return False

    def get_next_name(self,now_name):
        if self.school_report_students.count(now_name)>0:
            index=self.school_report_students.index(now_name)
            if index<len(self.school_report_students)-1:
                return self.school_report_students[index+1]
            else:
                return self.school_report_students[0]
    
        else:
            return ""
    def get_last_name(self,now_name):
        if self.school_report_students.count(now_name)>0:
            index=self.school_report_students.index(now_name)
            if index>0:
                return self.school_report_students[index-1]
            else:
                return self.school_report_students[len(self.school_report_students)-1]
        else:
            return ""

    def rank(self,the_number_list):
        '''
        返回一个数组，数组内某个位置的数表示原数组这个位置的数的排位。
        如[2,4,4,7,6]会返回[5,3,3,1,2],以为7是最大的排第1，7在原数组的第4位，所以返回数组的第4位是1。
        '''
        if len(the_number_list)==0:
            return []
        return_list=[i for i in range(len(the_number_list))]
        temp_list=[(num,i) for i,num in enumerate(the_number_list)]
        temp_list.sort(reverse=True)
        rank_number=1
        return_list[temp_list[0][1]]=1
        if(len(the_number_list)>1):
            for i in range(1,len(the_number_list)):
                if temp_list[i][0]==temp_list[i-1][0]:
                    return_list[temp_list[i][1]]=rank_number
                else:
                    return_list[temp_list[i][1]]=i+1
                    rank_number=i+1
        return return_list
    
    def add_rank_according_to_subject(self,subject):
        if subject=="不计算排名":
            if "ldlpm" in self.school_report_subjects:
                self.school_report_subjects.remove("ldlpm")
        else:
            if not("ldlpm" in self.school_report_subjects):
                self.school_report_subjects.append("ldlpm")
            subject_point_list=[]
            for student in self.school_report_students:
                try:
                    point=float(self.school_report[student][subject])
                except:
                    point=0
                subject_point_list.append(point)
            rank_list=self.rank(subject_point_list)
            for index,student in enumerate(self.school_report_students):
                self.school_report[student]["ldlpm"]=rank_list[index]

            
            



            
if __name__=="__main__":
    server=server_class()
    server.read_school_report("成绩单发送模板.xlsx")
    print(server.school_report)
    print(server.school_report_subjects)
    print(server.school_report_students)
            
