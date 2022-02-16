import numpy as np
import simpleaudio as sa


from random import sample
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import tkinter as tk
from kivy.config import Config
Config.set('graphics', 'resizable', '0')

class FancyLabel(Label):
	def __init__(self,bgcolor,text,font_size,color,size_hint,bold):
		self.bg_color = bgcolor
		super().__init__(text=text,font_size=font_size,color=color,size_hint=size_hint,bold=bold)
	def on_size(self, *args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3])
			Rectangle(pos=self.pos, size=self.size)
 
class FancyBorder(GridLayout):
	def __init__(self,cols,bgcolor,padding):
		self.bg_color = bgcolor
		super().__init__(cols=cols,padding=padding)
	def on_size(self, *args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3])
			Rectangle(pos=self.pos, size=self.size)


class OnCue(App):
	def build(self):
		# Okay lets get screensize and this is hacky I know
		self.icon = 'OnCueIcon.png'
		screensize = self._getScreenSize()
		Window.size = (int(screensize[0]*0.15), int(screensize[0]*0.2))
		self.window = GridLayout(cols=1)
		# Calculate fontsize from screensize and define our color scheme
		self.fontsize = int(screensize[0]*0.015)
		self.scheme={'Blue':[0.52,0.72,0.9,1],'Pink':[0.91,0.7,0.97,1],'White':[0.9,0.94,0.99,1],'Pink_2':[0.93,0.79,.97,1],
		'Blue_2':[0.62,0.77,0.9,1],'White_2':[0.81,0.85,0.90,1],'Font':[0.09,0.37,0.64],'Blue_3':[0.35,0.6,0.81,1]}

		# first we need to generate an affirmation duh
		self.greeting = FancyLabel(text= '{}!'.format(self._genAffirmation()),font_size= self.fontsize,size_hint=(1,1),color=self.scheme['Font'],bgcolor=self.scheme['Blue'],bold=True)
		self.window.add_widget(self.greeting)

		# Add Frequency input
		fc,self.freq_control = self._addControl(160,'Hz','Pink')
		self.window.add_widget(fc)
		# Add Interval input
		ic,self.interval_control = self._addControl(0.05,'Min','White')
		self.window.add_widget(ic)
		# Add Volume slider
		vc,self.volume_control = self._addControl(20,'Vol','Pink',True)
		self.window.add_widget(vc)
		# Add StartStop Button
		button_border = FancyBorder(cols=1,padding=[int((x/x)*self.fontsize*0.05) for x in range(1,5)],bgcolor=self.scheme['Blue_3'])
		self.button = Button(text= "START",bold= True,background_color = self.scheme['Blue'],background_normal = "",font_size=self.fontsize)
		self.button.bind(on_press=self.StartStop)
		button_border.add_widget(self.button)
		self.window.add_widget(button_border)
		self.loop_counter = 0

		# Define our variables
		self.running = False
		self.freq = None
		self.vol = None
		self.interval = None
		return self.window

	def _addControl(self,default,label,color,slider=False):
		layout = GridLayout(cols = 2)
		# Create sub layout to add a thicccc border
		sub_layout = FancyBorder(cols=1,padding=[int((x/x)*self.fontsize*0.35) for x in range(1,5)],bgcolor=self.scheme[color])
		if slider:
			inp = Slider(min=0, max=40, value=default)
		else:
			cursor_tmp = self.scheme['White'].copy()
			cursor_tmp[3] = 0.5
			inp = TextInput(multiline= False,text=str(default),font_size=self.fontsize,input_filter='float',halign='center',
			padding_y = [int(self.fontsize/2),0],cursor_width='4sp',background_color=self.scheme['White_2'],background_normal="",
			selection_color=cursor_tmp,cursor_color=cursor_tmp)
		sub_layout.add_widget(inp)
		layout.add_widget(sub_layout)
		# add a label to our control too how nice
		label = FancyLabel(text=label,font_size=self.fontsize,color=self.scheme['Font'],bold=True,size_hint=(0.35,1),bgcolor=self.scheme[color])
		layout.add_widget(label)
		return layout,inp

	def _getScreenSize(self):
		root = tk.Tk()
		return (root.winfo_screenwidth(),root.winfo_screenheight())

	def _genAffirmation(self):
		affirms = ['Pitch Perfect','You Rock','Sounding Good','Barb Is Listening','Snazzy as Usual']
		tmp = sample(affirms,1)
		return tmp[0]

	def StartStop(self, instance):
		if self.running:
			self.running = False
			self.button.text = 'START'
			self.clock_int.cancel()
		else:
			self.running = True
			self.button.text = 'STOP'
			self.interval = float(self.interval_control.text)*60 #convert to seconds
			self.clock_int = Clock.schedule_interval(self.playTone, self.interval)


	def playTone(self, *args):
		# calculate note frequencies
		freq = float(self.freq_control.text)
	
		# get timesteps for each sample, T is note duration in seconds
		sample_rate = 44100
		noteduration = 1
		timesteps = np.linspace(0, noteduration, noteduration * sample_rate, False)

		# generate sine wave notes
		note = np.sin(freq * timesteps * 2 * np.pi)

		audio = np.zeros((44100, 2))
		n = len(timesteps)
	
		audio[0 : n , 0] += note
		audio[0 : n , 1] += 0.125 * note
		# normalize to 16-bit range
		audio *= 32767 / np.max(np.abs(audio))
		# convert to 16-bit data
		audio = audio.astype(np.int16)

		# start playback
		play_obj = sa.play_buffer(audio, 2, 2, sample_rate)

		# wait for playback to finish before exiting
		play_obj.wait_done()
		   
if __name__ == '__main__':
	OnCue().run()