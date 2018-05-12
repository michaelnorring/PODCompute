from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from sys import platform

# Custom Imports
from navigationmenu import NavigationMenu
from manager import Manager
from screenconfig import ScreenConfig
from screenmain import ScreenMain
from screenmaintenance import ScreenMaintenance
from screenclockconfig import ScreenClockConfig

if platform == 'darwin':
    pass
elif platform == 'linux' or 'linux2':
    Builder.load_file('PODComputeMain.kv')

#Config.set('graphics', 'width', '720')
#Config.set('graphics', 'height', '480')
#Config.set('kivy', 'window_icon', 'gears.png')

class MainApp(Widget):
    def __init__(self, **kwargs):     
        super(MainApp, self).__init__(**kwargs)
        if platform == 'darwin':
            self.size = (800, 528)
            self.size_hint = (None, None)
        
        _manager = self.ids['manager']
        _nav = self.ids['nav']
        _nav.SetManager(_manager)
        
      
class PODComputeMainApp(App):
    def build(self):
        main = MainApp()
        #Window.size = (720,480)
        
        return main 

if __name__ == "__main__": 
    PODComputeMainApp().run()