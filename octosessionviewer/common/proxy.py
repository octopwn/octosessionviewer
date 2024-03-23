

class Proxy:
	def __init__(self, ptype:str, ip:str, port:int = None, username:str = None, password:str = None, agentid:str = None, proxyfactory = None, description:str = None, hidden:bool=False):
		self.ptype = ptype #socks4,socks5, socks4a, http
		self.ip = ip
		self.port = port
		self.username = username
		self.password = password
		self.agentid = agentid
		self.proxyfactory = proxyfactory #TODO implement this!
		self.description = description
		self.hidden = hidden
	
	def __str__(self):
		t = ''
		for k in self.__dict__:
			t += '%s: %s\r\n' % (k, self.__dict__[k])
		return t
	
	@staticmethod
	def from_dict(d:dict):
		ptype = d['ptype']
		ip = d.get('ip', None)
		port = d.get('port', None)
		username = d.get('username', None)
		password = d.get('password', None)
		agentid = d.get('agentid', None)
		description = d.get('description', None)

		return Proxy(
			ptype, 
			ip, 
			port=port, 
			username=username, 
			password=password, 
			agentid=agentid, 
			description=description)
	
class ProxyChain:
	def __init__(self, description:str = None, hidden:bool=False):
		self.ptype = 'CHAIN'
		self.chain = []
		self.description = description
		self.hidden = hidden
	
	def __str__(self):
		t = 'ProxyChain'
		for item in self.chain:
			t += '%s: %s\r\n' % (item, str(item))
		return t
	
	@staticmethod
	def from_dict(d:dict):
		#ptype = d['ptype']
		chain = d.get('chain', [])
		description = d.get('description', None)
		res = ProxyChain(description)
		res.chain = chain
		return res