from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock

from alarmservice import AlarmService

Builder.load_file('manager.kv')

class Manager(ScreenManager):
    screen_main = ObjectProperty(None)
    screen_maintenance = ObjectProperty(None)
    screen_config = ObjectProperty(None)
    screen_clockconfig = ObjectProperty(None)

    AlarmService = None

    def __init__(self, **kwargs): 
        super(Manager, self).__init__(**kwargs)

        self.LoadServices() 

    def LoadServices(self):
        # load all alarms
        self.AlarmService = AlarmService()

    def KillServices(self):
        # Kill all threads associated with the AlarmService
        self.AlarmService.KillAlarms()

        # Kill all Kivy Clock objects
        for clockevent in Clock.get_events():
            clockevent.cancel()
    