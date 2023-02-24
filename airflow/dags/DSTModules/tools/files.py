from datetime import datetime

def writeFile(filename, text, openmode='w'):
    f = open(filename, openmode)
    f.write(text)
    f.close()

def appendFile(filename, text, openmode='a'):
    f = open(filename, openmode)
    f.write(text)
    f.close()

def updateLog(message, c_path, withTime=True, logName="Log"):
    dt = datetime.now()
    fDate = dt.strftime('%Y-%m-%d')
    time = dt.strftime('%Y-%m-%d %H:%M:%S')
    fileLog = c_path["path_log"]+c_path["folder_separator"]+logName+"_"+fDate+".txt"
    f = open(fileLog, "a")
    line = ""
    if (withTime): line = time + " - "
    f.write(line + message + "\n")
    f.close()
    print(line + message)
