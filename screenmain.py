from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.image import Image

from computetemperatureconfig import *

from sys import platform
import time
import requests
import json
import os

if platform == 'darwin':
    pass
elif platform == 'linux' or 'linux2':
    import Adafruit_DHT

Builder.load_file('screenmain.kv')

class ScreenMain(Screen):
    computeTempLocation = ''

    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)
        Clock.schedule_interval(self.updateTemperature, 5)
        self.SetupComputeTemp()

    def SetupComputeTemp(self):
        global computeTempLocation

        if platform == 'linux' or 'linux2':
            try:
                for i in os.listdir('/sys/bus/w1/devices'):
                    if i != 'w1_bus_master1':
                        computeTempLocation = i
            except:
                pass
       
    def updateTemperature(self, *args):
        global computeTempLocation

        computeTemp = '--'
        indoorTemp = '--'
        indoorHumidity = '--'

        try:
            ''' 
            tempMsg = requests.get("http://192.168.1.135:5000/indoor_temperature", timeout=1)
            tempJson = tempMsg.content
            decoded = json.loads(tempJson)
            temp = str(decoded['Temperature'][0]['indoortemperature'])
            '''
            if platform == 'linux' or 'linux2':
                # POD Compute Temperature
                location = '/sys/bus/w1/devices/' + computeTempLocation + '/w1_slave'
                tfile = open(location)
                text = tfile.read()
                tfile.close()
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temperature = float(temperaturedata[2:])
                temperature = temperature / 1000
                computeTemp = str(temperature)
        except:
            pass
        
        computeTempLabel = self.ids['ComputeTemperatureControl']
        computeTempLabel.setTemperature(computeTemp)
        if(computeTempLabel.configdialog == None):
            computeTempLabel.configdialog = ComputeTemperatureConfig()

        try:
            if platform == 'linux' or 'linux2':
                sensor = Adafruit_DHT.DHT22
                pin = 22
                indoorHumidity, indoorTemperature = Adafruit_DHT.read_retry(sensor, pin) 
                indoorTemp = indoorTemperature
                indoorHumidity = round(indoorHumidity, 2)
        except:
            pass

        indoorTempLabel = self.ids['IndoorTemperatureControl']
        indoorTempLabel.setTemperature(indoorTemp)
        indoorTempLabel.setHumidity(indoorHumidity)

class ClockControl(Widget):
    manager = ObjectProperty()
    alarmShowing = False

    def __init__(self, **kwargs):
        super(ClockControl, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        
    def update(self, *args):
        dateLabel = self.ids['DateLabel']
        dateLabel.text = time.strftime("%A %B %d %Y")
        
        timeLabel = self.ids['TimeLabel']
        timeLabel.text = time.strftime("%I:%M:%S %p")

        if self.manager.AlarmService:
            alarmOnButton = self.ids['alarmOn_button']
            if self.manager.AlarmService.AlarmOn == True:
                if self.alarmShowing == False:
                    self.alarmShowing = True
                    alarmImage = Image()
                    alarmImage.source = 'trans-alarmclock.png'
                    alarmOnButton.add_widget(alarmImage)
            else:
                alarmOnButton.clear_widgets()
                self.alarmShowing = False

    def ClockConfig(self):
        self.manager.current = 'ScreenClockConfig'  
        
class TemperatureControl(Widget):
    manager = ObjectProperty()
    temperatureLabel = StringProperty()
    configdialog = ObjectProperty(None)

    def setTemperature(self, temperature):
        if temperature == '--':
            temp_f = temperature
        else:           
            temp_f = float(temperature) * 9.0 / 5.0 + 32.0
            temp_f = round(temp_f, 1)

        if(self.configdialog != None and temp_f != "--"):
            self.manager.ComputeTemperatureService.ComputeTemperature = int(temp_f)

        tempLabel = self.ids['TemperatureLabel']
        tempLabel.text = str(temp_f) + u"\u00b0"
    
    def setHumidity(self, humidity):
        humidityLabel = self.ids['HumidityLabel']
        humidityLabel.text = 'Humidity: ' + str(humidity) + ' %'

    def TemperatureConfig(self):
        if(self.configdialog != None):
            content = self.configdialog 
            content.manager = self.manager
            content.SetupScreen()
            content.bind(on_update=self._on_computetempupdate)
            self.popup = Popup(title='Set ' + self.temperatureLabel,
                                content=content,
                                size_hint=(None, None),
                                size=(600,480),
                                auto_dismiss= False)
            self.popup.open()
    
    def _on_computetempupdate(self, instance, answer, *args):
        self.popup.content.parent.remove_widget(self.popup.content)
        self.popup.dismiss()
        if answer == 'yes':
            print args[0][0]
            print args[0][1]
        
    