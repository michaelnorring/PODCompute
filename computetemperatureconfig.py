from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from roulettescroll import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from kivy.uix.boxlayout import BoxLayout

import json

Builder.load_file('computetemperatureconfig.kv')

class ComputeTemperatureConfig(BoxLayout):
    # set globals
    manager = ObjectProperty()
    temperatureSettings = None
    _setup = False
    #_temperature = 0
    #_onoff = ''
    
    def __init__(self, **kwargs):
        self.register_event_type('on_update')
        super(ComputeTemperatureConfig, self).__init__(**kwargs)

        self.temperatureSettings = ComputeTemperatureSettings()

    def on_update(self, *args):
		pass
    
    def SetupScreen(self):
        #global _setup
        #global _onoff
        
        # retrieve ComputeTemperatureSettings to get saved values
        objectsettings = self.manager.ComputeTemperatureService.Load()
        if(objectsettings) != '':
            self.temperatureSettings.Load(objectsettings)
        else:
            self.temperatureSettings.OnOff = 'On'
            self.temperatureSettings.Temperature = 80

        tempRoulette = self.ids['TemperatureRoulette']
        onoffButton = self.ids['OnOffButton']

        try:
            if self._setup == True or self._setup == False:
                pass
        except:
            self._setup = False

        if self._setup == False:  
            tempRoulette.bind(selected_value=lambda _, val:
                    self.set_Temp(_, str(val)))
            self._setup = True

        # Set all values
        
        onoffButton.text = self.temperatureSettings.OnOff
        if self.temperatureSettings.OnOff == 'On':
            onoffButton.state = 'down'
        else:
            onoffButton.state = 'normal'

        tempRoulette = self.ids['TemperatureRoulette']
        #tempRoulette.selected_value = self.temperatureSettings.Temperature
        tempRoulette.select_and_center(self.temperatureSettings.Temperature)
        
        
    def set_Temp(self, scroll, val):
        self.temperatureSettings.Temperature = val

    def on_ONOFFClick(self):
        #global _onoff
        button = self.ids['OnOffButton']

        if button.text == 'On':
            button.text = 'Off'
            button.state = 'normal'
            self.temperatureSettings.OnOff = 'Off'
        else:
            button.text = 'On'
            button.state = 'down'
            self.temperatureSettings.OnOff = 'On'

    def saveTemperatureConfig(self):
        global _setup
        _setup = False

        settingsJSON = self.temperatureSettings.toJSON()
        self.manager.ComputeTemperatureService.Update(settingsJSON)
        self.dispatch('on_update', 'yes', [self.temperatureSettings.Temperature, self.temperatureSettings.OnOff])
    
    def cancelTemperatureConfig(self):
        global _setup
        _setup = False
        self.dispatch('on_update', 'no')

class ComputeTemperatureSettings():
    Temperature = 0
    OnOff = ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def Load(self, objectsettingsJSON):
        if objectsettingsJSON != '':
            jsondata = json.loads(objectsettingsJSON)

            self.OnOff = jsondata['OnOff']
            self.Temperature = int(jsondata['Temperature'])