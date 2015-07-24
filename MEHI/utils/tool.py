################################
# Author   : septicmk
# Date     : 2015/4/3 9:13:31
# FileName : MEHI_tool.py
################################

import numpy as np
import os,sys
import skimage.external.tifffile as tiff

@exeTime
def load_tiff(pwd):
    '''
    Usage:
     - just read all the image under the pwd
    '''
    if os.path.isdir(pwd):
        img_stack = []
        names = []
        for imgname in os.listdir(pwd):
            if imgname.endswith('.tif'):
                names.append(imgname)
        names = sorted(names, key = lambda x: int(filter(str.isdigit, x)))
        for z,imgname in enumerate(names):
            msg = "reading %d-th frame" % (z)
            end = len(names)
            bar('info')(msg, z, end)
            img_pwd = os.path.join(pwd, imgname)
            if img_pwd.endswith('.tif'):
                img = tiff.imread(img_pwd)
                img_stack.append(img)
        return np.array(img_stack)
    else:
        return tiff.imread(pwd)

@exeTime 
def save_tiff(img_stack, name, pwd=None):
    '''
    Usage:
     - write the img_stack
    '''
    if not pwd:
        tiff.imsave(name, img_stack) 
    else:
        for z,frame in enumerate(img_stack):
            fname = pwd + name + '_%03d' % (z+1) + '.tif'
            dir, file = os.path.split(fname)
            if not os.path.exists(dir):
                os.makedirs(dir)
                tiff.imsave(fname, frame)
    

def exeTime(func):
    '''
    Usage:
     - just put '@exeTime'(with out quotation) before your function
     - will show the running time
    '''
    import time
    def wraper(*args, **args2):
        s = time.time()
        ret = func(*args, **args2)
        e = time.time()
        msg = "%3.3fs taken for {%s}" % (e-s, func.__name__)
        log('time')(msg)
        return ret
    return wraper

def showsize(obj, name = ''):
    '''
    Usage:
     - show the size of a object
     - e.g. showsize(img_stack, '1-L-Red.tif')
    Args:
     - obj: a variable
     - name: the name you want to print
    '''
    sz = sys.getsizeof(obj)
    if type(obj) is np.ndarray:
        sz = obj.nbytes + .0
    if sz < 1024.0:
        print "%s %.2f B" % (name ,sz)
    elif sz < 1024*1024:
        print "%s %.2f K" % (name, sz/(1024.0))
    elif sz < 1024*1024*1024:
        print "%s %.2f M" % (name, sz/(1024.0*1024.0))
    else:
        print "%s %.2f G" % (name, sz/(1024.0*1024.0*1024.0))
    
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    PUP = '\033[35m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    dic = { 'warn' : WARNING,
            'info'  : '',
            'error' : FAIL,
            'endc' : ENDC,
            'time' : OKGREEN,
            'debug' : PUP
        }
    @staticmethod
    def decode(level):
        return bcolors.dic.get(level,'')
    
def bar(level):
    '''
    Usage:
     - this will show a progress bar
     - e.g. bar('info')(msg, i, 100)
    '''
    if level in loglevel:
        def wraper(msg, i, end):
            if i <= end:
                sys.stdout.write('[' + bcolors.decode(level) + level + bcolors.decode('endc') + '] ('+ str(i)+'/' + str(end) + ') '+ msg + '\r')
                sys.stdout.flush()
            if i == end:
                print
        return wraper
    else:
        def wraper(msg, i, end):
            pass
        return wraper

def log(level):
    '''
    Usage:
     - this will just show info
     - e.g. log('info')(msg)
    '''
    if level in loglevel:
        def wraper(msg):
            print '[' + bcolors.decode(level) + level + bcolors.decode('endc') + '] '+ msg
        return wraper
    else:
        def wraper(msg):
            pass
        return wraper

def send_mail(sub, content):
    '''
    Usage:
     - send a mail when an error has occurred
     - change the mail_to to your mail address
    '''
    import smtplib 
    from email.mime.text import MIMEText
    mail_host = "smtp.sina.com"
    mail_user = "mehireporter"
    mail_pass = "mehi123"
    mail_postfix = "sina.com"
    # change the mail_to to your mail address
    mail_to = "septicmk@163.com" 
    fr = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = fr
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(fr, mail_to, msg.as_string())
        s.close()
        return True
    except Exception,e:
        log('error')(str(e))
        return False


if __name__ == '__main__':
    pass
    
