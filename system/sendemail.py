import sys,getopt
HELP_STR = "usage: sendEmail -e email [-t title | -m message | -h] ...\n"
HELP_STR += "Options and arguments:\n"
HELP_STR += "-e     : target email ,more targets split with ',' (can't be empt)\n"
HELP_STR += "-t     : email title \n"
HELP_STR += "-m     : email message \n"
HELP_STR += "-f     : email sender name\n"
def printHelp():
    print(HELP_STR)
    pass

def popEmail(message,title,sfrom='wtd',tar=[]):
    import wutil
    e = wutil.Email("smtp.qq.com",  "654630498@qq.com", "qfycmohioalybebh")
    e.sendEmail(message, sfrom, title, tar)

try:
    opts, args = getopt.getopt(sys.argv[1:],"he:t:m:f:",["help"])
    title,msg,email,sender = ("title","",[],"www")
    for opt,key in opts:
        if opt == '-h' or opt == '--help':
            printHelp()
            sys.exit()
        elif opt == '-e':
            email = key.split(',')
        elif opt == '-t':
            title = key
        elif opt == '-m':
            msg = key
        elif opt == '-f':
            sender = key
    popEmail(msg,title,sfrom=sender,tar=email)
except getopt.GetoptError as e:
    print("error",e)
