import sqlite3
import time
from datetime import datetime
from datetime import timedelta

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from AlarmDialog import *

class AlarmService():

    Alarms = list()
    AlarmOn = False
    
    def __init__(self):
        self.LoadAlarms()
    
    def LoadAlarms(self):   
        # clear _alarms of value
        del self.Alarms[:]
        self.AlarmOn = False

        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        curs.execute('SELECT id, hour, minute, onoff FROM t_alarm')
        result = curs.fetchall()
        curs.close()
        conn.close()
        
        for column in result:
            alarm = Alarm()
            alarm.id = column[0]
            alarm.hour = column[1]
            alarm.minute = column[2]
            alarm.onoff = column[3]
            alarm.SetAlarm()
            alarm.bind(on_alarmFire=self._on_alarmFire)
            alarm.bind(on_alarmUpdate=self._on_alarmUpdate)
            alarm.bind(on_alarmDelete=self._on_alarmDelete)
            self.Alarms.append(alarm)

            # Test if any of the alarms are on, if so, set AlarmOn to True
            if alarm.onoff == 'on':
                self.AlarmOn = True

    def _on_alarmFire(self, instance):
        pass

    def _on_alarmUpdate(self, instance):
        self.UpdateAlarm(instance)

    def _on_alarmDelete(self, instance):
        self.DeleteAlarm(instance)

    def NewAlarm(self, alarm):

        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        ins = 'INSERT INTO t_alarm (hour, minute, onoff) VALUES(?, ?, ?)'
        curs.execute(ins, (str(alarm.hour), str(alarm.minute), str(alarm.onoff)))
        conn.commit()
        curs.close()
        conn.close()

        self.LoadAlarms()

    def UpdateAlarm(self, alarm):
        
        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        curs.execute("UPDATE t_alarm SET onoff = '" + alarm.onoff + "' WHERE id = " + str(alarm.id))
        conn.commit()
        curs.close()
        conn.close()

        self.LoadAlarms()

    def DeleteAlarm(self, alarm):
        
        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        curs.execute('DELETE FROM t_alarm WHERE id = ' + str(alarm.id))
        conn.commit()
        curs.close()
        conn.close()

        self.LoadAlarms()

    def KillAlarms(self):
        for alarm in self.Alarms:
            alarm.KillAlarm()
            
class Alarm(Widget):
    id = 0
    hour = ''
    minute = ''
    onoff = ''
    ampm = ''
    alarmTime = ''
    fullAlarmTime = ''
    timer = None
    snoozeInterval = 8
    clockInterval = 5
    
    def __init__(self, **kwargs):
        self.register_event_type('on_alarmFire')
        self.register_event_type('on_alarmUpdate')
        self.register_event_type('on_alarmDelete')
        super(Alarm, self).__init__(**kwargs)
        

    def SetAlarm(self):
        currenttime = time.localtime()
        year = currenttime.tm_year
        month = currenttime.tm_mon
        day = currenttime.tm_mday

        self.fullAlarmTime = str(year) + '-' + str(month) +'-' + str(day) + ' ' + self.hour + ':' + self.minute + ':00'

        if int(self.hour) > 12:
            self.alarmTime = str(int(self.hour) - 12) + ':' + self.minute
            self.ampm = 'PM' 
        elif int(self.hour) == 12:
            self.alarmTime = '12:' + self.minute
            self.ampm = 'PM'
        elif int(self.hour) == 0:
            self.alarmTime = '12:' + self.minute
            self.ampm = 'AM'
        else:
            self.alarmTime = self.hour + ':' + self.minute
            self.ampm = 'AM'

        self.OnOffStateChanged()
        
    def OnOffStateChanged(self):
        self.dispatch('on_alarmUpdate')
        
        if self.onoff == 'on':
            # check if we are passed the time in the day for the alarm, in which case move the alarm out one day
            cftime = datetime.fromtimestamp(time.mktime(time.localtime()))
            atime = datetime.strptime(self.fullAlarmTime, "%Y-%m-%d  %H:%M:%S")
            if cftime > atime:
                adjTime = datetime.strptime(self.fullAlarmTime, "%Y-%m-%d  %H:%M:%S") + timedelta(days=1)
                self.fullAlarmTime = str(adjTime)
            if not self.timer:
                self.timer = Clock.schedule_interval(self.update, self.clockInterval)
        else:
            # todo: remove the schedule interval so that it is not running
            if self.timer:
                self.timer.cancel()

    def update(self, *args):       
        if self.onoff == 'on' and self.fullAlarmTime != '':
            currenttime = datetime.fromtimestamp(time.mktime(time.localtime()))
            alarmtime = datetime.strptime(self.fullAlarmTime, "%Y-%m-%d  %H:%M:%S")
            
            if currenttime > alarmtime:              
                self.dispatch('on_alarmFire')
                self.AlarmFire()

    def on_alarmUpdate(self, *args):
        pass

    def on_alarmFire(self, *args):
        pass

    def on_alarmDelete(self, *args):
        pass

    def DeleteAlarm(self):
        self.KillAlarm()
        self.dispatch('on_alarmDelete')

    def KillAlarm(self):
        if self.timer:
            self.timer.cancel()

    def AlarmFire(self):   
        self.timer.cancel()
        self.onoff = 'off'
        
        # Open Alarm Popup screen
        content = AlarmDialog()
        
        content.bind(on_alarmStop=self._on_alarmStop)
        self.popup = Popup(title="Alarm",
                            content=content,
                            size_hint=(None, None),
                            size=(800,480),
                            auto_dismiss= False)
        self.popup.open()

    def _on_alarmStop(self, instance, answer, *args):
        self.popup.dismiss() 
        
        if answer == 'snooze':
            snoozeTime = datetime.strptime(self.fullAlarmTime, "%Y-%m-%d  %H:%M:%S") + timedelta(minutes=self.snoozeInterval)
            self.fullAlarmTime = str(snoozeTime)
            self.onoff = 'on'
            self.OnOffStateChanged()
            #self.timer = Clock.schedule_interval(self.update, self.clockInterval)
        else:
            self.onoff = 'off'
            #self.timer.cancel()
            self.OnOffStateChanged()
            self.dispatch('on_alarmUpdate')


