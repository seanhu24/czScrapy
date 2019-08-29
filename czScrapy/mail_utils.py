import smtplib
import logging
from email.mime.text import MIMEText


# 授权码：123456Guo
def send_email(receiver=None, title=None, cont=None):

    host = 'smtp.yeah.net'
    # 设置发件服务器地址
    port = 465
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
    sender = 'xiaohu@yeah.net'
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = '123456Guo'
    # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    # receiver = to
    # 设置邮件接收人，可以是QQ邮箱
    body = cont
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html')
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = title
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    # msg['to'] = receiver
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        for r in receiver:
            msg['to'] = r
            s.sendmail(sender, r, msg.as_string())
            # 发送邮件！
            print('Done.sent email to {} success'.format(r))
            logging.info('Done.sent email to {} success'.format(r))
    except smtplib.SMTPException:
        print('Error.sent email fail')
        logging.error('Error.sent email fail')


if __name__ == '__main__':
    send_email(receiver=['8206741@163.com'],
               title='杭州余杭政府门户网站', cont='<h1>今日杭州余杭政府门户网站最新更新日期是{}</h1>'.format(111))
