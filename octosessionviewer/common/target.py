from typing import List

class Target:
	def __init__(self, ip:str, hostname:str = None, ports:List[str] = None, dcip:str = None, \
			realm:str = None, hidden:bool = False, isdc:bool=False, sid:str=None, source:str=None, \
			description:str = None, samaccountname:str = None, ostype:str=None, osver:str=None, \
			uac:int=None, groups:List[str] = None, favorite:bool=False, projectid:str=None, checksum:str = None):
		self.projectid = projectid
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
		self.groups = groups
		self.favorite = favorite

		if self.groups is None:
			self.groups = []

		if self.ports is None:
			self.ports = []

		if checksum is None:
			self.checksum = self.calc_checksum()

	def to_dict(self):
		# we can do this as it's a simple object
		return self.__dict__
	
	@staticmethod
	def from_dict(d:dict):
		projectid = d.get('projectid', None)
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
		groups = d.get('groups', None)
		favorite = d.get('favorite', False)
		return Target(
			ip, 
			hostname=hostname, 
			ports = ports, 
			dcip = dcip, 
			realm = realm, 
			hidden = hidden, 
			isdc = isdc,
			sid = sid, 
			source = source, 
			description = description, 
			samaccountname = samaccountname, 
			ostype = ostype, 
			osver = osver, 
			uac = uac, 
			groups = groups, 
			checksum = checksum,
			favorite = favorite,
			projectid = projectid
		)