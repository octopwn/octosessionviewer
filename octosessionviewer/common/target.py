from typing import List

class Target:
	def __init__(self, ip:str, hostname:str = None, ports:List[int] = None, dcip:str = None, realm:str = None, hidden:bool = False, isdc:bool=False, sid:str=None, source:str=None, description:str = None, samaccountname:str = None, ostype:str=None, osver:str=None, uac:int=None, checksum:str = None):
		self.hostname = hostname
		self.ip = ip
		self.ports = ports
		self.dcip = dcip #for kerberos auth
		self.realm = realm
		self.hidden = hidden
		self.description = description
		self.isdc = isdc
		self.sid = sid
		self.samaccountname = samaccountname
		self.ostype = ostype
		self.osver = osver
		self.uac = uac
		self.source = source
		self.dns = None # TODO
		self.checksum = checksum # this is for filtering out duplicates
	
	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s: %s\r\n' % (k, self.__dict__[k])
		return t

	def to_dict(self):
		# we can do this as it's a simple object
		return self.__dict__
	
	@staticmethod
	def from_dict(d:dict):
		ip = d.get('ip', None)
		hostname = d.get('hostname', None)
		ports = d.get('ports', None)
		dcip = d.get('dcip', None)
		description = d.get('description', None)
		realm = d.get('realm', None)
		isdc = d.get('isdc', False)
		hidden = d.get('hidden', False)
		sid = d.get('sid', None)
		samaccountname = d.get('samaccountname', None)
		ostype = d.get('ostype', None)
		osver = d.get('osver', None)
		uac = d.get('uac', None)
		source = d.get('source', None)
		checksum = d.get('checksum', None)
		return Target(ip, hostname, ports, dcip, realm, hidden, isdc, sid, source, description, samaccountname, ostype, osver, uac, checksum)
