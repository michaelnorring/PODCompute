from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from alarmclockconfig import *
from setupclockconfig import *
from alarmservice import Alarm
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty

import sqlite3
import time
from sys import platform
import os
from datetime import datetime
from datetime import timedelta

Builder.load_file('screenclockconfig.kv')

class ScreenClockConfig(Screen):
    def __init__(self, **kwargs):     
        super(ScreenClockConfig, self).__init__(**kwargs)
    
    def SetupScreen(self, *args):
        self.LoadAlarms()
        
    def LoadAlarms(self):
        alarmList = self.ids['Alarm_content']
        alarmList.clear_widgets()

        alarms = self.manager.AlarmService.Alarms
        
        for alarm in alarms:
            item = AlarmItem()
            item.manager = self.manager
            item.bind(on_alarmDelete=self._on_alarmDelete)
            item.SetAlarm(alarm)
            alarmList.add_widget(item)

        alarmList.add_widget(Widget())        

    def _on_alarmDelete(self, instance, alarmid):
        alarmList = self.ids['Alarm_content']
        alarmList.remove_widget(instance)
    
    def on_AddButton_Press(self):
        content = AlarmClockConfig()
        content.SetupScreen()
        content.bind(on_update=self._on_alarmupdate)
        self.popup = Popup(title="Set Alarm",
							content=content,
							size_hint=(None, None),
							size=(600,480),
							auto_dismiss= False)
        self.popup.open()

    def _on_alarmupdate(self, instance, answer, *args):
        self.popup.dismiss()
        if answer == 'yes':
            #Save new alarm
            hour = args[0][0]
            if args[0][2] == 'PM' and int(hour) < 12:
                hour = str( int(hour) + 12)
            elif args[0][2] == 'AM' and int(hour) == 12:
                hour = '00'
            
            minute = args[0][1]
            if int(minute) > 0 and int(minute) < 10:
                minute = '0' + minute
            onoff = args[0][3]

            alarm = Alarm()
            alarm.hour = str(hour)
            alarm.minute = str(minute)
            alarm.onoff = str(onoff)

            self.manager.AlarmService.NewAlarm(alarm)
        
        self.LoadAlarms()

    def on_SetClockButton_Press(self):
        content = SetupClockConfig()
        content.SetupScreen()
        content.bind(on_update=self._on_clockupdate)
        self.popup = Popup(title="Set Clock",
							content=content,
							size_hint=(None, None),
							size=(720,480),
							auto_dismiss= False)
        self.popup.open()

    def _on_clockupdate(self, instance, answer, *args):
        self.popup.dismiss()

        if answer == 'yes':
            #Save new time and date
            month = args[0][0]
            day = args[0][1]
            year = args[0][2]

            #month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            hour = args[0][3]
            if args[0][5] == 'PM' and int(hour) < 12:
                hour = str( int(hour) + 12)
            elif args[0][5] == 'AM' and int(hour) == 12:
                hour = '00'
            
            minute = args[0][4]
            if int(minute) > 0 and int(minute) < 10:
                minute = '0' + minute
            
            seconds = '00'

            if platform == 'linux2' or platform == 'linux':
                newDateTime = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(seconds)
                command = 'sudo date -s "' + newDateTime + '"'
                os.system(command)
            else:
                print 'Date & Time change for ' + str(platform) + ' is not implemented.'


class AlarmItem(BoxLayout):
    manager = ObjectProperty()
    alarm_time = StringProperty()
    alarm_ampm = StringProperty()
    alarm_onoff = StringProperty()
    
    alarm = None

    def __init__(self, **kwargs):
        self.register_event_type('on_alarmDelete')
        self.register_event_type('on_alarmUpdate')
        super(AlarmItem, self).__init__(**kwargs)

    def SetAlarm(self, alarm):
        self.alarm = alarm
        self.id = str(alarm.id)
        self.alarm_time = alarm.alarmTime
        self.alarm_ampm = alarm.ampm
        self.alarm_onoff = alarm.onoff

        self.SetOnOffButtonState()
        
    def delete(self):
        self.dispatch('on_alarmDelete', self.id)
        self.alarm.DeleteAlarm()

    def on_alarmDelete(self, *args):
        pass

    def on_alarmUpdate(self, *args):
        pass

    def on_OnOffStateChange(self):
        
        if self.alarm_onoff == 'on':
            self.alarm_onoff = 'off'
        else:
            self.alarm_onoff = 'on'
            
        self.alarm.onoff = self.alarm_onoff
        self.alarm.OnOffStateChanged()
        
        self.SetOnOffButtonState()
        self.dispatch('on_alarmUpdate')
    
    def SetOnOffButtonState(self):
        
        button = self.ids['OnOffButton']
        
        if self.alarm_onoff == 'on':
            button.state = 'down'
            button.text = 'On'    
        else:
            button.state = 'normal'
            button.text = 'Off'