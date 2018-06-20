
from contextlib import contextmanager

import io
import os

from smb.SMBConnection import SMBConnection
import smb.smb_structs

from satoricore.logger import logger


@contextmanager
def load(connection_dict):
	client_hostname = 'satori_smbclient'
	remote_hostname = connection_dict['host']

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
	if connection_dict['path'] is not None and "/" in connection_dict['path']:
		share = connection_dict['path'].split("/",1)[0]
	else:
		share = "C$"

	context = SatoriSMBContext(conn, share=share)
	yield context

	conn.close()


class SatoriSMBContext(object):

	def __init__(self, smb_connection, share="C$"):
		self.smb_connection = smb_connection
		self.path = os.path
		self.path.isdir = self.is_dir
		self.share = share

	def _strip_share(self, path):
		if path.startswith(self.share):
			return path[len(self.share)+1:]
		return path

	def listdir(self, path):
		try:
			files = self.smb_connection.listPath(self.share, self._strip_share(path))
		except smb.smb_structs.OperationFailure:
			logger.info("Could not list Directory '{}' in share '{}'"
					.format(path, self.share)
				)
			return []
		# print (files)
		ret = []
		for f in files:
			if f.filename == "." or f.filename == "..":
				continue
			ret.append(f.filename)
		return ret

	def stat(self, path):
		# print(self.share, self.__strip_share(path))
		# import pdb; pdb.set_trace();
		try:
			attrs = self.smb_connection.getAttributes(self.share, self._strip_share(path))
		except smb.smb_structs.OperationFailure:
			logger.info("Could not get Attributes of '{}' in share '{}'"
				.format(self._strip_share(path), self.share)
			)
			return SatoriSMBContext.smb_stat_result()

		return SatoriSMBContext.smb_stat_result(attrs)

	def lstat(self, path):
		# print(self.share, self.__strip_share(path))
		return self.stat(self._strip_share(path))

	def is_dir(self, path):
		try:
			return self.smb_connection.getAttributes(self.share, self._strip_share(path)).isDirectory
		except smb.smb_structs.OperationFailure:
			logger.info("Could not get Attributes of '{}' in share '{}'"
				.format(self._strip_share(path), self.share)
			)
			return False


	class smb_stat_result(dict):

		def __init__(self, smb_file_attr=None):
			if smb_file_attr is None:
				self['st_atime'] = 0
				self['st_mtime'] = 0
				self['st_ctime'] = 0
				self['st_size'] = 0
				self['st_mode'] = 32768
			else:
				self['st_atime'] = smb_file_attr.last_access_time
				self['st_mtime'] = smb_file_attr.last_write_time
				self['st_ctime'] = smb_file_attr.create_time
				self['st_size'] = smb_file_attr.file_size
				self['st_mode'] = 16384 if smb_file_attr.isDirectory else 32768

			for k, v in self.items():
				setattr(self, k, v)


	# @contextmanager
	def open(self, path, mode='r', **kwrags):
		path = self._strip_share(path)
		smb_fd = SatoriSMBContext.smb_file_descriptor(path, self.share, self.smb_connection)
		# yield smb_fd
		return smb_fd
		smb_fd.close()


	class smb_file_descriptor(object):

		def __enter__(self):
			return self

		def __exit__(self, *args, **kwargs):
			pass


		def __init__(self, path, share, smb_connection):
			self.path = path
			self.seek_offset = 0
			self.share = share
			self.conn = smb_connection

		def seek(self, offset):
			self.seek_offset = offset

		def read(self, offset=0):
			if offset == 0:
				offset = -1

			ret = io.BytesIO()
			attrs, read_n = self.conn.retrieveFileFromOffset(
					self.share,
					self.path,
					ret,
					offset=self.seek_offset,
					max_length=offset,
				)
			# print(attrs, read_n)
			self.seek_offset += read_n
			return ret.getvalue()

			#	f = self.open("C$/USers/IEUSER/Downloads/desktop.ini")
			#	f.read()

			#	with self.open("C$/USers/IEUSER/Downloads/desktop.ini") as f: f.read()

		def close(self):
			'''
				No need to deallocate any object
			'''
			return