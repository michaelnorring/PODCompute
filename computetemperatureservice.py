import sqlite3
import json
from sys import platform

if platform == 'darwin':
    pass
elif platform == 'linux' or 'linux2':
    import RPi.GPIO as GPIO

from kivy.clock import Clock

class ComputeTemperatureService():
    Temperature = 0
    OnOff = 'Off'
    timer = None
    clockInterval = 60

    def __init__(self):
        if platform == 'linux' or platform == 'linux2':
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17, GPIO.HIGH)

        self.Load()

    def KillService(self):
        if self.timer:
            self.timer.cancel()
        
        if platform == 'linux' or platform == 'linux2':
            GPIO.output(17, GPIO.HIGH)
            GPIO.cleanup()

    def Load(self):
        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM t_objectsettings WHERE type = 'ComputeTemperatureSettings'")
        result = curs.fetchall()
        curs.close()
        conn.close()

        objectsettings = ''

        for row in result: 
            objectsettings = row[2]

        self.SetFanTemperature(objectsettings)

        return objectsettings

    def Update(self, objectsetting):
        conn = sqlite3.connect('PODStore.db')
        curs = conn.cursor()
        curs.execute("DELETE FROM t_objectsettings WHERE type = 'ComputeTemperatureSettings'")
        conn.commit()

        sqlstring = str("INSERT INTO t_objectsettings(type, objectsettings) values('ComputeTemperatureSettings', '" + str(objectsetting) + "')")
        
        curs.execute(sqlstring)
        conn.commit()
        curs.close()
        conn.close()

        self.SetFanTemperature(objectsetting)

    def SetFanTemperature(self, objectsettings):
        if objectsettings != '':
            jsondata = json.loads(objectsettings)

            self.OnOff = jsondata['OnOff']
            self.Temperature = int(jsondata['Temperature'])

        if self.OnOff == 'On':
            if not self.timer:
                self.timer = Clock.schedule_interval(self.CheckTemperature, self.clockInterval)
        else:
            if self.timer:
                self.timer.cancel()
    
    def CheckTemperature(self, *args):       
        if self.OnOff == 'On':
            # check if computetemp is higher than self.temparate (fantemp), if so, then turn fan on.
            computeTemp = 110
            if (computeTemp > self.Temperature):
                if platform == 'linux' or platform == 'linux2':
                    GPIO.output(17, GPIO.LOW)
            else:
                if platform == 'linux' or platform == 'linux2':
                    GPIO.output(17, GPIO.HIGH)
        else:
            # test if fan is on, if yes, then turn fan off.
            if platform == 'linux' or platform == 'linux2':
                GPIO.output(17, GPIO.HIGH)
            


        