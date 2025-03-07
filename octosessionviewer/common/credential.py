

class Credential:
	def __init__(
			self, username:str, secret:str, stype:str, domain:str = None, certfile:str = None, keyfile:str = None, 
			hidden:bool = False, certfiledata:str=None, keyfiledata:str=None, sid:str=None, source:str=None, 
			description:str = None, favorite:bool=False, subprotocol:str = 'NATIVE', subprotocolobj = None, checksum:str = None,
			projectid:str=None, **kwargs):
		self.projectid = projectid
		self.domain = domain
		self.username = username
		self.stype = stype #password/nt/rc4/aes/kirbi/...
		self.secret = secret
		self.hidden = hidden
		self.certfile = certfile
		self.keyfile = keyfile
		self.certfiledata = certfiledata
		self.keyfiledata = keyfiledata
		self.description = description
		self.subprotocol = subprotocol
		self.subprotocolobj = subprotocolobj
		self.sid = sid
		self.source = source
		self.favorite = favorite
		self.metadata = kwargs

	@staticmethod
	def from_dict(d:dict):
		projectid = d.get('projectid', None)
		username = d.get('username', '')
		secret = d.get('secret', '')
		stype = d.get('stype', '')
		hidden = d.get('hidden', False)
		domain = d.get('domain', None)
		certfile = d.get('certfile', None)
		keyfile = d.get('keyfile', None)
		certfiledata = d.get('certfiledata', None)
		keyfiledata = d.get('keyfiledata', None)
		description = d.get('description', None)
		sid = d.get('sid', None)
		source = d.get('source', None)
		subprotocol = d.get('subprotocol', 'NATIVE')
		checksum = d.get('checksum', None)
		favorite = d.get('favorite', False)

		return Credential(
			username,
			secret,
			stype,
			domain = domain,
			certfile = certfile,
			keyfile = keyfile, 
			hidden = hidden, 
			certfiledata = certfiledata, 
			keyfiledata = keyfiledata, 
			sid = sid, 
			source = source,
			description = description, 
			favorite = favorite,
			subprotocol = subprotocol,
			checksum = checksum,
			projectid = projectid
		)
