from contextlib import contextmanager

import os
from smb.SMBConnection import SMBConnection

@contextmanager
def load(connection_dict):
	client_hostname = 'satori_client'
	remote_hostname = 'Deskjet-4540'

	conn = SMBConnection(
				connection_dict['username'],
				connection_dict['auth'],
				client_hostname,
				remote_hostname,
				# use_ntlm_v2=True,
				is_direct_tcp=True
			)

	success = conn.connect(
				connection_dict['host'],
				connection_dict['port'],
			)
	if not success: 
		raise ConnectionError("Could not connect to '{host}:{port}' through SMB".
				format(**connection_dict)	# contains 'host', 'port' keys
			)

	context = SatoriSMBContext(conn)
	yield context

	conn.close()


class SatoriSMBContext(object):

	def __init__(self, smb_connection):
		self.smb_connection = smb_connection
		self.path = os.path
		# self.path.isdir = 

	def listdir(self, path):
		share, path = path.split('/',1)
		# import pdb; pdb.set_trace();
		files = self.smb_connection.listPath(share, path)
		# print (files)
		return [f.filename for f in files]

	def stat(self, path):
		share, path = path.split('/',1)
		attrs = self.smb_connection.getAttributes(share, path)
		return SatoriSMBContext.smb_stat_result(attrs)

	def lstat(self, path):
		return self.stat(path)

	def is_dir(self):
		share, path = path.split('/',1)
		return self.smb_connection.getAttributes(share, path).isDirectory


	class smb_stat_result(dict):

		def __init__(self, smb_file_attr):
			self['st_atime'] = smb_file_attr.last_access_time
			self['st_mtime'] = smb_file_attr.last_write_time
			self['st_ctime'] = smb_file_attr.create_time
			self['st_size'] = smb_file_attr.file_size
			self['st_mode'] = 16384 if smb_file_attr.isDirectory else 32768

			for k, v in self.items():
				setattr(self, k, v)
