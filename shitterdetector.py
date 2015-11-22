import kivy
import time
import urllib2
from urllib import urlopen
import os
import json
from threading import Thread

import RPi.GPIO as io

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

io.setmode(io.BCM)

pir_pin = 18

io.setup(pir_pin, io.IN, pull_up_down=io.PUD_DOWN)		 # activate PiR input


class Netconf():

	def is_connected(self):
		print ('Running network connectivity check.')
		try:
			urllib2.urlopen("http://www.google.com").close()
		except urllib2.URLError:
			print("Not Connected")
			return False
		else:
			print("Connected")
			return True

    def CallMotionDetectedApi(self):
	   print ('Calling the SongAPI to subscribe to music.')
	   url = "http://10.0.5.138:3000/publications/motiondetected"
	   response = urlopen(url).read()
	   return True

    def CallNoMotionDetectedApi(self):
		print('Calling the SongAPI to unsubscribe from music.')
	    url = "http://10.0.5.138:3000/publications/nomotion"
        response = urlopen(url).read()
		return True

	def conf(self):
		print ('Running configuration checks.')
		if self.is_connected():
			return True
		else:
			print ('Device is offline.')
			return False

def motion_detector(self):
	print ("motion detect thread called.")
	counter = 0
	net = Netconf()
	while True:
		if io.input(pir_pin):
			counter += 1
			time.sleep(0.5)
		else:
			counter = 0
			time.sleep(1)
		if counter >= 3:
			print ("motion detected!")

			if(net.conf()):
				net.CallMotionDetectedApi()
			time.sleep(6)

		else:
			net.CallNoMotionDetectedApi()


class MainScreen(BoxLayout):
	active_label = ObjectProperty(None)

	def on_active_label(self, instance, value):
		#start listener thread
		pIR = Thread(target=motion_detector, args=(self,))
		pIR.start()

class prometheusApp(App):
	def build(self):
		Window = MainScreen()
		return Window

if __name__ == '__main__':
	prometheusApp().run()
