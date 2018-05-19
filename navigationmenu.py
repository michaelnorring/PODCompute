import sys
import os
from sys import platform

from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

Builder.load_file('navigationmenu.kv')

class NavigationMenu(ActionBar):
    _manager = None

    def Navigate(self, navtext):
        _manager.current = navtext

    def Exit(self):
        _manager.KillServices()
        App.get_running_app().stop()

    def SetManager(self, manager):
        global _manager
        _manager = manager
        self.Navigate("ScreenMain")

    def Reboot(self):
        content = ConfirmPopup(text='Are you sure?')
        content.bind(on_answer=self._on_answer_reboot)
        self.popup = Popup(title="Reboot POD Compute",
							content=content,
							size_hint=(None, None),
							size=(480,400),
							auto_dismiss= False)
        self.popup.open()

    def _on_answer_reboot(self, instance, answer):
        self.popup.dismiss()
        
        if repr(answer) == "'yes'":
            #if RaspberryPI
            if platform == "linux" or platform == "linux2":
                _manager.KillServices()
                os.system('sudo shutdown -r now')
            
            #if Mac OS X
            elif platform == "darwin":
                print 'Reboot not implemented on MAC OS Darwin'

            #if Win32
            elif platform =="Win32":
                print 'Reboot not implemented on Windows'

        else:
            pass

    def Shutdown(self):
        content = ConfirmPopup(text='Are you sure?')
        content.bind(on_answer=self._on_answer_shutdown)
        self.popup = Popup(title="Shutdown POD Compute",
							content=content,
							size_hint=(None, None),
							size=(480,400),
							auto_dismiss= False)
        self.popup.open()

    def _on_answer_shutdown(self, instance, answer):
        self.popup.dismiss()
        
        if repr(answer) == "'yes'":
            #if RaspberryPI
            if platform == "linux" or platform == "linux2":
                _manager.KillServices()
                os.system('sudo shutdown -P now')
            
            #if Mac OS X
            elif platform == "darwin":
                print 'Shutdown not implemented on MAC OS Darwin'

            #if Win32
            elif platform =="Win32":
                print 'Shutdown not implemented on Windows'

        else:
            pass

class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)
		
	def on_answer(self, *args):
		pass	