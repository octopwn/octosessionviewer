class ClientConsoleBase:
	def __init__(self, projectid, majortype, subtype, client_id:int, connection, cmd_q, msg_queue, prompt, octopwnobj, params, history, command_modifier = None):
		self.projectid = projectid
		self.majortype = majortype
		self.subtype = subtype
		self.params = params
		self.history = history
		self.prompt = prompt
		self.octopwnobj = octopwnobj
		self.command_modifier = command_modifier

class ClientConfigBase:
	def __init__(self, config_type:str, clientname:str, completer, description = None, settings = None):
		self.config_type = config_type
		self.clientname = clientname
		self.completer = completer
		self.description = description
		self.settings = settings

class ClientConfig(ClientConfigBase):
	def __init__(self, connection_type:str, authentication_type:str, target_id:int, credential_id:int, proxy_id:int, clientname:str, completer, client_type, description = None, params=None, port:int=None, timeout:int=None, settings = None):
		ClientConfigBase.__init__(self, 'NORMAL', clientname, completer, description, settings = settings)
		self.connection_type = connection_type
		self.authentication_type = authentication_type
		self.target_id = target_id
		self.credential_id = credential_id
		self.proxy_id = proxy_id
		self.client_type = client_type
		self.params = params
		self.port = port
		self.timeout = timeout
	
	@staticmethod
	def from_dict(d:dict):
		connection_type = d['connection_type']
		authentication_type = d['authentication_type']
		client_type = d['client_type']
		target_id = int(d['target_id'])
		credential_id = None
		if 'credential_id' in d:
			credential_id = int(d['credential_id'])
		proxy_id = d.get('proxy_id')
		description = d.get('description')
		params = d.get('params')
		port = d.get('port')
		timeout = d.get('timeout')
		settings = d.get('settings')

		return ClientConfig(
			connection_type, 
			authentication_type, 
			target_id, 
			credential_id, 
			proxy_id, 
			'', 
			None, 
			client_type, 
			description = description, 
			params = params,
			port = port,
			timeout = timeout,
			settings = settings
		)


class ScannerConfig(ClientConfigBase):
	def __init__(self, scanner_type:str, clientname, completer, description = None, settings = None):
		ClientConfigBase.__init__(self, 'SCANNER', clientname, completer, description, settings = settings)
		self.scanner_type = scanner_type
		self.params = {}
	
	@staticmethod
	def from_dict(d:dict):
		scanner_type = d.get('scanner_type', None)
		clientname = d.get('clientname', None)
		description = d.get('description', None)
		settings = d.get('settings', None)
		res = ScannerConfig(scanner_type, clientname, None, description, settings = settings)
		res.params = d.get('params', None)
		
		return res

class ServerConfig(ClientConfigBase):
	def __init__(self, scanner_type:str, clientname:str, completer, description:str = None, settings = None):
		ClientConfigBase.__init__(self, 'SERVER', clientname, completer, description, settings = settings)
		self.scanner_type = scanner_type
		self.params = {}
	
	@staticmethod
	def from_dict(d:dict):
		scanner_type = d.get('scanner_type', None)
		clientname = d.get('clientname', None)
		description = d.get('description', None)
		settings = d.get('settings', None)
		res = ServerConfig(scanner_type, clientname, None, description, settings=settings)
		res.params = d.get('params', None)
		return res

class UtilsConfig(ClientConfigBase):
	def __init__(self, scanner_type:str, clientname:str, completer, description:str = None, settings = None):
		ClientConfigBase.__init__(self, 'UTILS', clientname, completer, description, settings = settings)
		self.scanner_type = scanner_type
		self.params = {}
	
	@staticmethod
	def from_dict(d:dict):
		scanner_type = d.get('scanner_type', None)
		description = d.get('clientname', None)
		clientname = d.get('clientname', '???')
		settings = d.get('settings', None)
		res = UtilsConfig(scanner_type, clientname, None, description, settings=settings)
		res.params = d.get('params', None)
		return res
