import os,json,wutil

def popEmail(message,title,sfrom='wtd',tar=[]):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    conf = {}
    if os.path.exists('./conf.json'):
        f = open('./conf.json','r')
        conf = json.loads(f.read())
        f.close()
    mail_hosts = conf["mail_hosts"]
    mailIndex = conf["mailIndex"]
    users = conf["users"]
    keysIndex = conf["keysIndex"]
    pwds = conf["pwds"]
    tarMails = tar
    e = wutil.Email(mail_hosts[mailIndex], users[keysIndex], pwds[keysIndex])
    e.sendEmail(message, sfrom, title, tarMails)
