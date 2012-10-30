#coding=utf8

import urllib
import shutil
import sys
import os
from pyquery import PyQuery as pq
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

HEADERS = {
    'Host': 'manhua.178.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

COMICS = {
    'hz': 'haizeiwang',
    'hy': 'huoyingrenzhe',
    'ss': 'sishen',
    'yj': 'yaojingdeweiba'
}

COMIC_NAMES = {
    'haizeiwang': '海贼王',
    'huoyingrenzhe': '火影忍者',
    'sishen': '死神',
    'yaojingdeweiba': '妖精的尾巴'
}

SMTP_HOST = {
    '163': 'smtp.163.com',
    '126': 'smtp.126.com',
    'yeah': 'smtp.yeah.net',
    'sina': 'smtp.sina.com.cn',
    'gmail': 'smtp.gmail.com',
    'sohu': 'smtp.sohu.com',
    'yahoo': 'smtp.mail.yahoo.com',
    'yahoo.com.cn': 'smtp.mail.yahoo.com.cn'
}

PIC_URL_PREFIX = u'http://imgfast.manhua.178.com/'


def fetch_chapter_url(comic_url=''):
    req = requests.get(comic_url, headers=HEADERS)
    html = pq(req.text)
    newest_url = html('a').filter('#newest_chapter')
    comic_chapter = newest_url.eq(1)
    chapter_url = comic_chapter.attr('href')
    chapter_name = comic_chapter.html() # 最新一章的名称
    print chapter_name
    print chapter_url
    return (chapter_url, chapter_name)


def fetch_images_url(chapter_url=''):
    req = requests.get(chapter_url, headers=HEADERS)
    tmp_url = req.text.split('\n')[10] # html中第11行保存了图片的URL后缀
    pic_url_str = tmp_url[len(r'''var pages = pages = '["'''): -4]

    pic_url_arr = [] # 保存最新一章的图片URL
    for i in pic_url_str.replace('\/', '/').split('","'):
        url = PIC_URL_PREFIX + urllib.quote(i.decode('unicode-escape').encode('utf8'))
        pic_url_arr.append(url)
    return pic_url_arr


def fetch_and_sava_images(comic='', chapter_name='', pic_url_arr=[]):
    dir = os.path.join('images', comic, chapter_name)
    print dir
    if not os.path.isdir(dir): os.makedirs(dir)
    images_path_arr = []
    for url in pic_url_arr:
        #pic = url[url.rfind('/')+1:]
        #pic = re.findall(r'\d+.*', url[url.rfind('/')+1:])[-1]
        pic = url[url.rfind('/')+1:]
        pic = pic[::-1][:7][::-1] # 图片名称只用001.jpg，去除前面的中文，方便排序
        pic_path = os.path.join(chapter_name, pic)
        images_path_arr.append(pic_path)
        print pic_path
        f = urllib.urlretrieve(url)
        shutil.move(f[0], os.path.join(dir, pic))
    return images_path_arr


def gen_mobi_html(images_path_arr=[], comic='', chapter_name=''):
    # 生成 mobi 文件所需的 html 模版
    HTML_TEMPLATE = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <head>
        <title>%s %s</title>
        <link rel="stylesheet" href="../../sample.css" type="text/css" />
    </head>
    <body>
        %s
    </body>
</html>
    '''
    # 每张图片在 mobi 的 html 模版中的格式
    IMAGE_P = '''
        <p class="pagebreak">&nbsp;</p>
        <p class="centered">
            <img alt="%s" src="%s"/>
        </p>
        '''
    images_html = ''
    mobi_html = ''
    idx = 1
    for path in images_path_arr:
        images_html += IMAGE_P % (idx, path)
        idx += 1
    mobi_html = HTML_TEMPLATE % (COMIC_NAMES[comic], chapter_name, images_html)
    #print mobi_html
    # 写到文件
    html_file_path = os.path.join('images', comic, '%s_%s.html'%(COMIC_NAMES[comic], chapter_name))
    #print html_file_path
    with open(html_file_path, 'w') as f:
        f.write(mobi_html)
    return html_file_path


def gen_mobi(comic, chapter_name, mobi_html_file):
    '''调用命令生成mobi文件'''
    import subprocess
    print mobi_html_file
    mobi_file_path = '%s_%s.mobi' % (COMIC_NAMES[comic], chapter_name)
    cmd = u'kindlegen %s -c2 -locale zh -o %s' % \
          (mobi_html_file, mobi_file_path)
    print cmd.encode('gbk')
    subprocess.call(cmd.encode('gbk'))
    print u'\nmobi 文件生成完毕'
##    return os.path.join(mobi_file_path.encode('gbk'))
    return mobi_file_path
        

def send_mail(subject='', mail_from='comics4kindle@163.com', mail_to=[], filename='', uid='', pwd=''):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import mimetypes
    
    #send_mail('subject', 'kindle4work@163.com', 'kindle4work@163.com', 'images/sishen/死神_第513话.mobi', 'smtp.163.com', 'kindle4work@163.com', 'kingsTON0987')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = ';'.join(mail_to)

    #msg.attach(MIMEText(filename))
    
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_attach = MIMEBase(maintype, subtype)    
    with open(filename, 'rb') as f:
        file_attach.set_payload(f.read())    
    encoders.encode_base64(file_attach)
    file_attach.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file_attach)

    # 处理smtp服务器
    i = mail_from.index('@')
    mail_type = mail_from[i+1: mail_from.find('.', i)]
    smtp_host = ('smtp.%s.com' if mail_type is not 'yahoo' else 'smtp.mail.%s.com') % mail_type
    
    mail = smtplib.SMTP()
    mail.connect(smtp_host)
    mail.login(uid, pwd)
    print u'正在发送邮件[===%s===]...' % subject
    mail.sendmail(mail_from, mail_to, msg.as_string())
    mail.quit()
    print u'邮件[===%s===]发送成功...' % subject



def main():
    if len(sys.argv) == 1:
        comic = COMICS['hz'] # 默认为海贼王
        send_to_kindle = False
    elif len(sys.argv) == 2:
        comic = COMICS[sys.argv[1]]
        send_to_kindle = False
    elif len(sys.argv) == 5:
        send_to_kindle = True
        comic = COMICS[sys.argv[1]]
        mail_from = sys.argv[2]
        mail_to = []
        mail_to.append(sys.argv[3])
        #uid = sys.argv[4]
        pwd = sys.argv[4]
    else:
        print u"""Usage: python comics4kindle.py phz/hy/ss/yj] --> 抓取漫画图片保存到本地
python comics4kindle.py [hz/hy/ss/yj] [mail_from] [mail_to] [mail_pwd] --> 发到邮箱，例如kindle邮箱
"""
        sys.exit(0)
        
    comic_chapter_url = "http://manhua.178.com/%s/" % comic
    chapter_url, chapter_name = fetch_chapter_url(comic_chapter_url)
    pic_url_arr = fetch_images_url(chapter_url)
    images_path_arr = fetch_and_sava_images(comic, chapter_name, pic_url_arr)
    html_file_path = gen_mobi_html(images_path_arr, comic, chapter_name)
    mobi_file_path = gen_mobi(comic, chapter_name, html_file_path)
   
    subject = '%s_%s@%s' % (COMIC_NAMES[comic], chapter_name, 'comics4kindle')
    mobi_file_path = os.path.join('images', comic, mobi_file_path).encode('gbk')
    print mobi_file_path
    
    if send_to_kindle:
        send_mail(subject, mail_from, mail_to, mobi_file_path, mail_from, pwd)


if __name__ == '__main__':
    main()


