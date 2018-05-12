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
            self.ifconfig_Darwin()
        elif platform == "win32":
            currentOS = "Windows"
            self.ifconfig_Win32()
        elif platform == "linux" or platform == "linux2":
            currentOS = "Linux"
            self.ifconfig_Linux()
        else:
            currentOS = platform

        currentOSLabel.text = currentOS

    def ifconfig_Darwin(self):
        ifconfig = check_output(['ifconfig', 'en0'])
        iface, status, MAC, Bcast, Nmask, IPv6 = (ifconfig.split()[i] for i in (0,24, 5, 18, 16, 14))

        ifacelabel = self.ids['IFace']
        ifacelabel.text = iface

        statuslabel = self.ids['Status']
        statuslabel.text = status

        iplabel = self.ids['IPAddress']
        iplabel.text = IPv6

        maclabel = self.ids['MACAddress']
        maclabel.text = MAC

        bcastlabel = self.ids['BCast']
        bcastlabel.text = Bcast

        nmarklabel = self.ids['NMask']
        nmarklabel.text = Nmask

    def ifconfig_Win32(self):
        pass

    def ifconfig_Linux(self):
        pass
    
