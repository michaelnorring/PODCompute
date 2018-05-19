from subprocess import check_output
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from sys import platform

Builder.load_file('screenconfig.kv')

class ScreenConfig(Screen):
 
    def SetupScreen(self, *args):
        currentOSLabel = self.ids['OS']
        currentOS = ""
        if platform == "darwin": 
            currentOS = "Mac OS X (Darwin)"
            self.ifconfig('en0')
        elif platform == "win32":
            currentOS = "Windows"
            self.ifconfig('none')
        elif platform == "linux" or platform == "linux2":
            currentOS = "Linux"
            self.ifconfig('wlan0')
        else:
            currentOS = platform

        currentOSLabel.text = currentOS

    def ifconfig(self, interface):
        ifacelabel = self.ids['Interface']
        ifacelabel.text = interface

        statuslabel = self.ids['Status']

        if interface != 'none':
            ifconfig = check_output(['ifconfig', interface])
            
            statuslabel.text = ifconfig
        else:
            statuslabe.text = '' 
    
