import io
from typing import Dict, Tuple, List
from pathlib import Path
import zipfile
import base64
import gzip
import json
import os


from octosessionviewer.common.target import Target
from octosessionviewer.common.credential import Credential
from octosessionviewer.common.proxy import Proxy, ProxyChain
from octosessionviewer.common.clientconfig import ClientConfigBase, ClientConsoleBase

import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



class OctoSessionViewer:
	def __init__(self, key:str=None):
		self.__session_file_password = key
		if self.__session_file_password is None:
			self.__session_file_password = 'OCTOPWN_DEMO_MODE'
		self.projectid:str = None
		self.dcip:str = None
		self.realm:str = None
		self.resolver:int = None
		self.screensettings:Dict[str, str] = {}
		self.credentials:Dict[int, Credential] = {}
		self.targets:Dict[int, Target] = {}
		self.proxies:Dict[int, Proxy] = {}
		self.sessions:Dict[int, Tuple[ClientConfigBase, ClientConsoleBase]] = {}
		self.work_dir:str = None
		self.messagebuffers:Dict[int, str] = {}
		self.workfiles:Dict[str, str] = {}

	@staticmethod
	def from_json(data:str):
		return OctoSessionViewer.from_dict(json.loads(data))
	
	@staticmethod
	def from_json_f(fileh:io.IOBase):
		return OctoSessionViewer.from_dict(json.load(fileh))
	
	def extract_workdir(self, outdir:str):
		if outdir is None:
			outdir = os.path.join(os.getcwd(), 'workdir')
		if self.workfiles is None:
			raise Exception('No workfiles in the session!')
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		self.workfiles.extractall(outdir)

	@staticmethod
	def from_file(filepath:str|Path, key:str=None):
		session = OctoSessionViewer(key)
		with open(filepath, 'rb') as f:
			decdata = session.decrypt_session_file(f)
			decdata = gzip.decompress(decdata.read())
			return OctoSessionViewer.from_json(decdata.decode())


	def decrypt_session_file(self, session_file_data:bytes|io.BytesIO):
		if isinstance(session_file_data, bytes):
			if len(session_file_data) <= 28:
				raise Exception('Session file data too small!')
			session_file_data = io.BytesIO(session_file_data)
		version = session_file_data.read(4)
		salt = session_file_data.read(16)
		nonce = session_file_data.read(12)
		tag = session_file_data.read(16)
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=100000,
			backend=default_backend()
		)
		key = kdf.derive(self.__session_file_password.encode())
		decrypted_buffer = io.BytesIO()
		cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), default_backend())
		decryptor = cipher.decryptor()
		while True:
			chunk = session_file_data.read(4166656)
			if not chunk:
				break
			pt_chunk = decryptor.update(chunk)
			decrypted_buffer.write(pt_chunk)
		
		pt_final = decryptor.finalize()
		decrypted_buffer.write(pt_final)
		decrypted_buffer.seek(0)
		return decrypted_buffer
	
	@staticmethod
	def from_dict(d:dict):
		res = OctoSessionViewer()
		res.work_dir = None
		res.projectid = d.get('projectid')
		res.dcip = d.get('dcip')
		res.realm = d.get('realm')
		res.resolver = d.get('resolver')
		res.work_dir = d.get('work_dir', None)
		if 'screensettings' in d:
			try:
				res.screensettings = json.loads(d['screensettings'])
			except:
				pass
		
		res.credentials = {}
		if 'credentials' in d:
			for tid in d['credentials']:
				res.credentials[int(tid)] = Credential.from_dict(d['credentials'][tid])
		
		res.targets = {}
		if 'targets' in d:
			for tid in d['targets']:
				res.targets[int(tid)] = Target.from_dict(d['targets'][tid])
		
		res.proxies = {}
		if 'proxies' in d:
			for tid in d['proxies']:
				if d['proxies'][tid]['ptype'].upper() == 'CHAIN':
					res.proxies[int(tid)] = ProxyChain.from_dict(d['proxies'][tid])
				else:
					res.proxies[int(tid)] = Proxy.from_dict(d['proxies'][tid])
		
		res.sessions = {}
		if 'sessions' in d:
			for tid in d['sessions']:
				client_config = d['sessions'][tid]['config']
				res.sessions[str(tid)] = client_config

		res.messagebuffers = {}
		if 'messagebuffers' in d:
			for tid in d['messagebuffers']:
				res.messagebuffers[int(tid)] = []
				try:
					for timestamp, msg in d['messagebuffers'][tid]:
						buffer = base64.b64decode(msg).decode('utf-8')
						res.messagebuffers[int(tid)].append([timestamp, buffer])
				except:
					# old format
					for msg in base64.b64decode(d['messagebuffers'][tid]).split(b'\r\n'):
						res.messagebuffers[int(tid)].append(['??????', msg.decode()])

		if 'workfiles' in d:
			if 'workdir.zip' in d['workfiles']:
				zipbuffer = io.BytesIO(base64.b64decode(d['workfiles']['workdir.zip']))
				with zipfile.ZipFile(zipbuffer, 'r') as zipf:
					zipf.extractall(res.work_dir)
		return res
	
	def __str__(self):
		t = '=== OctoSessionViewer ===\r\n'
		t += 'DC IP: %s\r\n' % self.dcip
		t += 'Realm: %s\r\n' % self.realm
		t += 'Resolver: %s\r\n' % self.resolver
		t += 'Workdir: %s\r\n' % self.work_dir
		t += 'Credentials:\r\n'
		for cred in self.credentials.values():
			t += str(cred)
		t += 'Targets:\r\n'
		for target in self.targets.values():
			t += str(target)
		t += 'Proxies:\r\n'
		for proxy in self.proxies.values():
			t += str(proxy)
		t += 'Sessions:\r\n'
		for session in self.sessions.values():
			t += str(session)
		
		t += 'Console Messages:\r\n'
		for tid in self.messagebuffers:
			t += '\tClient %s:\r\n' % tid
			for timestamp, msg in self.messagebuffers[tid]:
				t += '\t\tTimestamp: %s\r\n' % timestamp
				t += '\t\tMessage:\r\n%s\r\n' % msg
		
		if self.workfiles is not None and 'workdir.zip' in self.workfiles:
			t += 'Workfiles:\r\n'
			zipbuffer = io.BytesIO(base64.b64decode(d['workfiles']['workdir.zip']))
			with zipfile.ZipFile(zipbuffer, 'r') as zipf:
				t += zip_tree(zipf)
		return t


def zip_tree(zipf:zipfile.ZipFile):
	# Get the list of file names in the zip
	names = zipf.namelist()
	# Sort the names to ensure directories are listed before their contents
	names.sort()

	# Create a tree structure
	tree = {}
	for name in names:
		path_parts = name.split('/')
		current_level = tree
		for part in path_parts:
			if part not in current_level:
				current_level[part] = {}
			current_level = current_level[part]

	# Function to print the tree structure
	def print_tree(current_tree, indent=""):
		t = ''
		for key, value in current_tree.items():
			t += f"{indent}{key}/\r\n" if value else f"{indent}{key}\r\n"
			if value:  # If it's a directory and not a file
				t += print_tree(value, indent + "    ")
		return t
	# Print the tree starting from the root
	return print_tree(tree)