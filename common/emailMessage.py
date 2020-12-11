import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
# 格式化邮件地址
def formatAddr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def sendMail(body, attachment):
    smtp_server = 'smtp.exmail.qq.com'
    from_mail = 'ruijie.qiur@eeoa.com'
    mail_pass = 'qiuruijie@123'
    to_mail = ['ruijie.qiur@eeoa.com']
    # 构造一个MIMEMultipart对象代表邮件本身
    msg = MIMEMultipart()
    # Header对中文进行转码
    msg['From'] = formatAddr('管理员 <%s>' % from_mail).encode()
    msg['To'] = ','.join(to_mail)
    msg['Subject'] = Header('监控', 'utf-8').encode()
    # plain代表纯文本
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    # 二进制方式模式文件
    with open(attachment, 'rb') as f:
        # MIMEBase表示附件的对象
        mime = MIMEBase('text', 'txt', filename=attachment)
        # filename是显示附件名字
        mime.add_header('Content-Disposition', 'attachment', filename=attachment)
        # 获取附件内容
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        # 作为附件添加到邮件
        msg.attach(mime)
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_mail, mail_pass)
    print(2)
    print(type(msg))
    server.sendmail(from_mail, to_mail, msg.as_string())  # as_string()把MIMEText对象变成str
    server.quit()
#
# if __name__ == "__main__":
#     sendMail('附件是测试数据, 请查收！', 'setting.py')