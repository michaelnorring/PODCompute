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

Builder.load_file('setupclockconfig.kv')

class SetupClockConfig(BoxLayout):
    # set globals
    _setup = False
    _month = 0
    _day = 0
    _year = 0
    _hour = 0
    _minute = '00'
    _ampm = ''
    
    def __init__(self, **kwargs):
        self.register_event_type('on_update')
        super(SetupClockConfig, self).__init__(**kwargs)

    def on_update(self, *args):
		pass
    
    def SetupScreen(self):
        global _setup
        global _ampm
        
        try:
            if _setup == True or _setup == False:
                pass
        except:
            _setup = False

        if _setup == False:    
            b = self.ids['ClockRoulette']

            b.add_widget(Widget())

            monthRoulette = CyclicRoulette(cycle=12, density=2.8, zero_indexed=False)
            monthRoulette.bind(selected_value=lambda _, val:
                    self.set_Month(_, str(val)))
            b.add_widget(monthRoulette)

            dayRoulette = CyclicRoulette(cycle=31, density=2.8, zero_indexed=False)
            dayRoulette.bind(selected_value=lambda _, val:
                    self.set_Day(_, str(val)))
            b.add_widget(dayRoulette)

            yearRoulette = Roulette(density=2.8)
            yearRoulette.bind(selected_value=lambda _, val:
                    self.set_Year(_, str(val)))
            b.add_widget(yearRoulette)

            hourRoulette = TimeFormatCyclicRoulette(id='Hour', cycle=12, density=7, zero_indexed=False)
            hourRoulette.bind(selected_value=lambda _, val:
                    self.set_Hour(_, str(val)))
            b.add_widget(hourRoulette)

            minuteRoulette = TimeFormatCyclicRoulette(id='Minute', cycle=60, density=7)
            minuteRoulette.bind(selected_value=lambda _, val:
                    self.set_Minute(_, str(val)))
            b.add_widget(minuteRoulette)

            ampmButton = Button(text='AM', size=(100,100), size_hint=(None, None), 
                    pos_hint={'center_x': .5, 'center_y': .5}, on_press=self.on_AMPMClick)
            b.add_widget(ampmButton)
            
            _setup = True

            # Preset roulette values and associated globals
            monthRoulette.selected_value = 1
            self.set_Month(monthRoulette, monthRoulette.selected_value)
            dayRoulette.selected_value = 1
            self.set_Day(dayRoulette, dayRoulette.selected_value)
            yearRoulette.selected_value = 2018
            self.set_Year(yearRoulette, yearRoulette.selected_value)
            hourRoulette.selected_value = 12
            self.set_Hour(hourRoulette, hourRoulette.selected_value)
            minuteRoulette.select_value = 0
            self.set_Minute(minuteRoulette, minuteRoulette.selected_value)
            _ampm = 'AM'

            b.add_widget(Widget())

    def set_Month(self, scroll, val):
        global _month
        _month = val

    def set_Day(self, scroll, val):
        global _day
        _day = val

    def set_Year(self, scroll, val):
        global _year
        _year = val

    def set_Hour(self, scroll, val):
        global _hour
        _hour = val

    def set_Minute(self, scroll, val):
        global _minute
        if val < 10:
            _minute = '0' + str(val)
        else:
            _minute = str(val)

    def on_AMPMClick(self, button):
        global _ampm
        if button.text == 'AM':
            button.text = 'PM'
            _ampm = 'PM'
        else:
            button.text = 'AM'
            _ampm = 'AM'
    
    def saveClock(self):
        global _month
        global _day
        global _year
        global _hour
        global _minute
        global _ampm
        global _setup

        _setup = False
        self.dispatch('on_update', 'yes', [_month, _day, _year, _hour, _minute, _ampm])
    
    def cancelClock(self):
        global _setup
        _setup = False
        self.dispatch('on_update', 'no')

    