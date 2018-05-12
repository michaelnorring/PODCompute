import threading
import pyaudio
import wave
import sys

from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('AlarmDialog.kv')

class AlarmDialog(BoxLayout): 
    audio_thread = None
    is_playing = False

    def __init__(self, **kwargs):
        global is_playing
        global audio_thread
        
        self.register_event_type('on_alarmStop')
        super(AlarmDialog, self).__init__(**kwargs)

        is_playing = True
        audio_thread = threading.Thread(target=self.loop_audio)
        audio_thread.start()

    def on_alarmStop(self, *args):
	    pass

    def on_StopAlarm(self): 
        global is_playing
        global audio_thread

        is_playing = False
        audio_thread.join()      
        self.dispatch('on_alarmStop', 'yes')

    def on_SnoozeAlarm(self):
        global is_playing
        global audio_thread

        is_playing = False
        audio_thread.join()
        self.dispatch('on_alarmStop', 'snooze')

    def loop_audio(self):
        global is_playing

        while is_playing:
            self.play_audio()

    def play_audio(self):
        global is_playing
        global audio_thread

        chunk = 1024
        wf = wave.open('Buzzer.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)

        data = wf.readframes(chunk)

        while data != '' and is_playing: # is_playing to stop playing
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
                