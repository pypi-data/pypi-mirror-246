import sys
from fastapi import FastAPI
from optrabot.config import Config
from ib_insync import *
from loguru import logger
from .tradinghubclient import TradinghubClient
import pkg_resources

class OptraBot():
	def __init__(self, app: FastAPI):
		self.app = app
		self.thc : TradinghubClient = None
	
	def __setitem__(self, key, value):
		setattr(self, key, value)

	def __getitem__(self, key):
		return getattr(self, key)
	
	async def startup(self):
		logger.add("optrabot.log", level="DEBUG", rotation="5 MB")
		logger.info('OptraBot {version}', version=pkg_resources.get_distribution('optrabot').version)
		# Read Config
		self['config'] = Config("config.yaml")
		await self.connect_ib()
		self.thc = TradinghubClient(self)
		await self.thc.start_polling()

	async def shutdown(self):
		logger.debug('OptraBot shutdown()')
		await self.thc.shutdown()
		if self['ib'].isConnected():
			logger.info('Disconnect from IB')
			self['ib'].disconnect()

	async def connect_ib(self):
		logger.debug('Trying to connect with IB ...')
		ibinsync = IB()
		self['ib'] = ibinsync
		try:
			config: Config = self['config']
			twshost = config.get('tws.host')
			if twshost == '':
				twshost = 'localhost'
			try:
				twsport = int(config.get('tws.port'))
			except KeyError as keyErr:
				twsport = 7496

			try:
				twsclient = int(config.get('tws.client'))
			except KeyError as keyErr:
				twsclient = 21
		
			await ibinsync.connectAsync(twshost, twsport, clientId=twsclient)
			logger.debug("Connected to IB")
		except Exception as excp:
			logger.error("Error connecting IB: {}", excp)


