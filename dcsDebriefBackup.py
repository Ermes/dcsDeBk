import sys
import os
from shutil import copy2
from time import localtime, strftime
from filecmp import cmp
import subprocess


class doBackup():
  
  path = "C:\\Users\\JuanLuis\\Saved Games\\DCS.openbeta\\Logs"

  def __init__(self):
    os.chdir(self.path)
    self.listDir()
    self.checkDirectory()
    self.checkDebrief()
    self.checkScheduler()

  def checkScheduler(self):    
    CREATE_NO_WINDOW = 0x08000000
    ## para que le resultado del comando se agrege al objeto de salida como stdout y stderr agregamos capture_output=True,text=True
    result = subprocess.run(['schtasks.exe','/TN','DCS_debriefLogBackup'],creationflags=CREATE_NO_WINDOW)
    if result.returncode==1:
      create_result = subprocess.run(['schtasks.exe','/CREATE','/sc','minute','/mo','5','/tn','DCS_debriefLogBackup','/tr','D:\\Pruebas\\Desktop\\dist\\dcsDebriefBackup.exe'])
  
  def listDir(self):
    dir_list = os.listdir()
    text = ''
    for file in dir_list:
      text = text + file + "<br />"

  def checkDirectory(self):
    if not os.path.isdir('old_debriefing'):
      os.mkdir('old_debriefing')

  def checkDebrief(self):
    found = False  
    if os.path.isfile('debrief.log'):
      files = os.listdir('old_debriefing')
      for file in files:
        if cmp('debrief.log','.\\old_debriefing\\'+file):
          entrontrado = True
          break
      if not found: 
        copy2('debrief.log',".\\old_debriefing\\"+self.getNewFileName())


  def getNewFileName(self):
      mtime = localtime(os.path.getmtime('debrief.log'))
      newFileName = strftime("%y%m%d%H%M%S",mtime)+'_debrief.log'
      return newFileName


if __name__=='__main__':
  GUI = doBackup()
  
  
  