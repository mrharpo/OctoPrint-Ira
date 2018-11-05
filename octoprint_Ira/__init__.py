# coding=utf-8
from __future__ import absolute_import
from serial import Serial
from cobs import cobs
from struct import pack
# from os import excel
from glob import glob
port = '/dev/ttyUSB1'
baud = 1200
# from time import sleep

# s = Serial(port, BAUD, )



import octoprint.plugin
from octoprint.printer import PrinterInterface
from octoprint.util import RepeatedTimer

class Ira(octoprint.plugin.StartupPlugin,
#		octoprint.plugin.TemplatePlugin,
		octoprint.plugin.SettingsPlugin,
#		octoprint.plugin.AssetPlugin,
		octoprint.plugin.EventHandlerPlugin,
		octoprint.plugin.ProgressPlugin,
		PrinterInterface,
		RepeatedTimer):
	interface = PrinterInterface()

	def getTemps(self):
		temps = self._printer.get_current_temperatures()
		bed = temps['bed']['actual']
		try:
			tool = temps['tool0']['actual']
			return (bed, tool)
		except:
			self._logger.error('no tool! %s' % temps)
			return (bed, 0)
	def showProgress(self):
		bed, tool = self.getTemps()
		self._logger.info("FX: progress: %s, bed: %s tool: %s" % (self.progress, bed, tool))
		self.send(255, self.progress, bed, tool)


		timer = None
	def startTimer(self):
		self.timer = RepeatedTimer(1.0, self.showProgress)
		self.timer.start()
		self._logger.info('timer started! %s' % self.timer)

	def stopTimer(self):
		self.timer.cancel()
		self._logger.info('timer stopped')

	progress = None
	try:
		# ports = [p for p in glob('/dev/ttyUSB[0-9]')]
		# _logger.info('found ports %s' % ports)
			#excel(["udevadm", "info", "-a", "-n", port])

		serial = Serial(port, baud, )
	except:
		# _logger.error('unable to connect to Ira!')
		serial = None

	def send(self, *args):
		p = cobs.encode(pack('>{}B'.format(len(args)), *args)) + b'\x00'
		if self.serial is not None:
			self.serial.write(p)
		else:
			self._logger.warn("Ira not connected")
		# sleep(.1)
		# if s.in_waiting:
		# 	print(s.read(s.in_waiting))

	def on_event(self, event, payload):
		self._logger.info("Event: %s Payload: %s" % (event, payload))
		if event == 'Startup':
			self._logger.info("FX: rain - teal")
			self.send(102,127,255,255)
		elif event == 'PrinterStateChanged':
			if payload['state_id'] == 'OFFLINE':
				self._logger.info("FX: wash - red")
				self.send(0,10,0,0)
			elif payload['state_id'] == 'PRINTING':
				self._logger.info("FX: rain - green")
				self.send(102,0,255,0)
		elif event == 'Connecting':
			self._logger.info("FX: rain - blue")
			self.send(102,0,0,255)
		elif event == 'Connected':
			self._logger.info("FX: wash - green")
			self.send(0,8,255,8)
		elif event == 'Error':
			self._logger.info("FX: wash - red")
			self.send(0,255,0,0)
		elif event == 'PrintStarted':
			self._logger.info("FX: cylon - green")
			self.send(27,0,255,0)
			self.startTimer()
		elif event == 'PrintFailed':
			self._logger.info("FX: rain - red")
			self.send(102,255,0,0)
			self.stopTimer()
		elif event == 'PrintDone':
			self._logger.info("FX: rain - green")
			self.send(102,8,255,8)
			self.stopTimer()
		elif event == 'PrintCancelling':
			self._logger.info("FX: rain - orange")
			self.send(102,255,125,0)
			self.stopTimer()
		elif event == 'PrintCancelled':
			self._logger.info("FX: wash - orange")
			self.send(0,255,125,0)
			self.stopTimer()
		elif event == 'PrintPaused':
			self._logger.info("FX: rain - yellow")
			self.send(102,255,255,0)
			self.stopTimer()
		elif event == 'PrintResumed':
			self._logger.info("FX: cylon - green")
			self.send(27,0,255,0)
			self.startTimer()
		# elif event == 'PositionUpdate':
			# self._logger.info()
			# self.showProgress()
		# self._logger.info(event)
		# self._logger.info(payload)
		# return
	def on_print_progress(self, storage, path, progress):
		self.progress = progress
		if progress < 100:
			self.showProgress()

	def on_startup(self, a, b):
		self._logger.info("pIra starting! ")
		self._logger.info(a)
		self._logger.info(b)
	def on_after_startup(self):
		self._logger.info("pIra running!")
		self._settings.get(["url"])

	def get_settings_defaults(self):
		return dict(url="https://apothecary.kagstrom.guru")

	# def shouldWeStop():
	# 	if self.state in [""]

	# def get_template_vars(self):
	# 	return dict(url=self._settings.get(["url"]))
	# def get_template_configs(self):
	# 	return [
	# 		dict(type="navbar", custom_bindings=False),
	# 		dict(type="settings", custom_bindings=False)
	# 		]
	# def get_assets(self):
	# 	return dict(js=["js/Ira.js"])
__plugin_name__="Ira"
__plugin_implementation__ = Ira()
