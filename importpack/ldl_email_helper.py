# 8月25日写到58行，明天需要完成html的addtext和addtable,预留添加附件的接口。
from smtplib import SMTP
from email.mime.nonmultipart import MIMENonMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from ldlpkg.ldl_html import *
'''
使用本模块发送邮件，首先实例化一个ldl_email_class对象并编辑你的邮件内容。
然后实例化一个email_sender_class对象来发送你的邮件。
这两个类的使用可以看下面说明。
'''
#定义错误类型
class WrongSmtpServer(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if len(args)==1:
            self.args=args[0]
        else:
            self.args=args
class LoginError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if len(args)==1:
            self.args=args[0]
        else:
            self.args=args
class EmailSendError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        if len(args)==1:
            self.args=args[0]
        else:
            self.args=args


#邮件发送类，负责发送邮件。邮件的内容在邮件类编辑。 
'''
    方法：
        构造方法（sender,authcode,smtp_server,smtp_sever_port）
        sender 发送者邮箱地址
        authcode 发送者邮箱SMTP服务授权码，需要到自己邮箱中生成。
        smtp_server 发送者邮箱SMTP服务器，可以百度查询xx邮箱的STMP服务器域名，qq邮箱为smtp.qq.com
        smtp_sever_port  发送者邮箱SMTP服务器服务端口，可百度查询xx邮箱的SMTP服务器端口，qq邮箱为25.

        SendEmail(receiver_address,the_email)
            发送邮件
            receiver_address为接收者邮箱地址
            the_email为编辑好的邮箱，必须是ldl_email_class的对象。
    
'''
class email_sender_class:
    def __init__(self,sender,authcode,smtp_server,smtp_sever_port):
        self.smtper = SMTP(smtp_server,port=smtp_sever_port,timeout=1)
        self.sender=sender
        if not self.smtper:
            raise WrongSmtpServer("smtp服务器连接失败，请检查网络是否畅通，服务器域名和端口是否正确")
        try:
            self.smtper.login(sender,authcode)
        except:
            raise LoginError("登录失败，请检查邮箱地址和授权码是否填写正确！")
    def SendEmail(self,receiver_address,the_email):
        if type(the_email)!=ldl_email_class:
            raise TypeError("邮件主体类型错误，应该为ldl_email_class类型")
        the_email.complete_mail()
        try:
            self.smtper.sendmail(self.sender,receiver_address,the_email.msg_root.as_string())
        except:
            print("send_error")
            raise EmailSendError("发送失败，请检查目的邮箱是否存在，或者邮件本体是否有误！",receiver_address)
            
#邮件类，负责编辑邮件。
'''
方法：
    构造方法（title,to_name,call,from_name)
        title为邮件标题
        to_name为接收者姓名
        call为接收者称呼
        from_name为发送者姓名

    addtext(text,size=16,**argvs)
        在邮件中添加文字。text为要添加的文字，size为文字大小，argvs是html css样式,用来编辑显示效果。可不填。

    addtable(table,title)
        在邮件中添加表格，table为要添加的表格，格式为[[],[],[],……],内部的列表为一行内容，内部有多少格列表就有多少行。表格列数为元素最多的行所拥有的元素个数。
        title为表格标题。
'''
class ldl_email_class:
    def __init__(self,title,to_name,call,from_name) -> None:
        self.from_name=from_name
        self.complete_mail_flag=0 #记录对象是否已经完成最终拼接，完成最终拼接后不能再添加元素。
        self.msg_root=MIMEMultipart('mixed') #顶层载体,载体类型为mixed，可以拼接任何载体
        self.msg_root['To']=Header(to_name,'utf-8') #在顶层载体记录信息
        self.msg_root['From']=Header(from_name,'utf-8') #在顶层载体记录信息
        self.msg_root['Subject']=Header(title,'utf-8') #在顶层载体记录信息

        self.attachmentlist=[] #附件载体（载体内已经装载附件）集合
        self.bodybox=MIMEMultipart('related') #邮件正文载体，载体类型为related，可以把图片通过html引用显示在正文中而并不是当作附件。文本部分由alternative类型的载体承载。
        self.html_pic_index=1 #插入到html页面的图片引索，每插入一张图片，引索+1

        self.htmlbox=MIMEMultipart('alternative') #展示部分，纯文本或者html超文本载体，但只能是其中一个，优先html超文本。
        self.html_content=ldl_html_class() #html的简单封装的类，用来快速构建简单的html界面
        self.html_content.add_text(20,to_name+call+":") #顶格写称呼

    def addtext(self,text,size=16,**argvs):
        '''
        在邮件中添加文字。text为要添加的文字，size为文字大小，argvs是html css样式。可不填。
        '''
        self.html_content.add_text(size,text,**argvs)
    def addtable(self,table,title):
        '''
        在邮件中添加表格，table为要添加的表格，格式为[[],[],[],……],内部的列表为一行内容，内部有多少格列表就有多少行。表格列数为元素最多的行所拥有的元素个数。
        title为表格标题。
        '''
        if type(table)!=list:
            raise TypeError("参数错误，table必须是列表")
        for row in table:
            if type(row)!=list:
                raise TypeError("参数错误,table内所有元素必须都为列表")
        self.html_content.add_table(table,title)

    def complete_mail(self):
        '''
        加上落款。然后拼接各个载体
        首先alternative载体载入html文本。（addtext和addtable其实都只是在写html，并没有把html与邮件关联。
        调用complete_mail后，html才真正在邮件中）

        然后related载体连接alternative载体。作为内嵌资源的图片在addpic中已经进入到了related载体中。

        然后顶层载体mixed连接related载体和附件载体。

        
        '''
        if not self.complete_mail_flag:
            self.html_content.add_text(18,self.from_name,text_align='right')
            self.htmlbox.attach(MIMEText(self.html_content.to_str(),'html','utf-8'))
            self.bodybox.attach(self.htmlbox)
            self.msg_root.attach(self.bodybox)
            for attachment in self.attachmentlist:
                self.msg_root.attach(attachment)
            
            self.complete_mail_flag=1   

if __name__=="__main__":
    email_sender=email_sender_class(sender="1589075757@qq.com",authcode="vgcrsuxoyfhyjifj",smtp_server='smtp.qq.com',smtp_sever_port=25)
    the_list=[['科目','成绩'],['语文',12],['数学',13]]
    the_email=ldl_email_class('成绩单','刘德龙','同学','计科1901')
    the_email.addtext("请查收你本次期中考试的成绩单")
    the_email.addtable(the_list,'成绩单')
    the_email.addtext("请继续努力！")
    email_sender.SendEmail("1589075757@qq.com",the_email)
    
    #except Exception as errortype:
        #print(errortype.args)



