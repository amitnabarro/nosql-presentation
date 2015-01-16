from logging import Handler
from pymongo import MongoClient
from sys import modules
import datetime

class MongoDBHandler(Handler):

	def __init__(self, address, db, collection):
		try:
			self.client = MongoClient(address)
			self.db = self.client[db]
			self.coll = self.db[collection]
		except Exception as ex:
			print 'failed to connect to mongodb database', ex.message
		super(MongoDBHandler, self).__init__()


	def emit(self,record):
		if hasattr(self,'coll') and isinstance(record.msg, dict):
			record.msg['timestamp'] = datetime.datetime.utcnow()
			record.msg['level'] = getattr(modules['logging'],record.levelname)
			self.coll.insert(record.msg)