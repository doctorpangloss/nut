from Fs.File import File
import Fs.Type
from binascii import hexlify as hx, unhexlify as uhx
from nut import Print
from nut import Keys
from nut import blockchain

class ContentEntry:
	def __init__(self, f):
		self.hash = f.read(32)
		self.ncaId = hx(f.read(16)).decode()
		self.size = f.readInt48()
		self.type = f.readInt8()

		f.readInt8() # junk


class Cnmt(File):
	def __init__(self, path = None, mode = None, cryptoType = -1, cryptoKey = -1, cryptoCounter = -1):
		super(Cnmt, self).__init__(path, mode, cryptoType, cryptoKey, cryptoCounter)

		self.titleId = None
		self.version = None
		self.titleType = None
		self.headerOffset = None
		self.contentEntryCount = None
		self.metaEntryCount = None
		self.contentEntries = []


	def open(self, file = None, mode = 'rb', cryptoType = -1, cryptoKey = -1, cryptoCounter = -1):
		super(Cnmt, self).open(file, mode, cryptoType, cryptoKey, cryptoCounter)
		self.rewind()

		self.titleId = hx(self.read(8)[::-1]).decode()
		self.version = self.readInt32()
		self.titleType = self.readInt8()

		self.readInt8() # junk

		self.headerOffset = self.readInt16()
		self.contentEntryCount = self.readInt16()
		self.metaEntryCount = self.readInt16()

		self.contentEntries = []

		self.seek(0x20 + self.headerOffset)
		for i in range(self.contentEntryCount):
			self.contentEntries.append(ContentEntry(self))





	def printInfo(self, maxDepth = 3, indent = 0):
		tabs = '\t' * indent
		Print.info('\n%sCnmt\n' % (tabs))
		Print.info('%stitleId = %s' % (tabs, self.titleId))
		Print.info('%sversion = %x' % (tabs, self.version))
		Print.info('%stitleType = %x' % (tabs, self.titleType))

		for i in self.contentEntries:
			Print.info('%s\tncaId: %s  type = %x' % (tabs, i.ncaId, i.type))
		super(Cnmt, self).printInfo(maxDepth, indent)


