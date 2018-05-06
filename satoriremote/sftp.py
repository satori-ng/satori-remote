from contextlib import contextmanager

import os
import paramiko


@contextmanager
def load(host, username, password=None, pub_key_path=None, port=None):
	if port is None:
		port=22	# default

	# Open a transport
	transport = paramiko.Transport((host, port))
	# transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# Auth
	transport.connect(
			username=username,
			password=password,
		)

	# Go!
	sftp = paramiko.SFTPClient.from_transport(transport)

	sContext = SatoriSFTPContext(transport, sftp)

	yield sContext

	# Close
	sftp.close()
	transport.close()
	# print ("Closed")


	# print (f.listdir('/'))

class SatoriSFTPContext(object):

	def __init__(self, ssh_transport, sftp_connection):
		self.ssh_transport = ssh_transport
		self.sftp_connection = sftp_connection

		# monkey-patch some remote utilities
		self.__dict__['path'] = os.path

		# Implement os methods into the SatoriContext
		for attr in dir(self.sftp_connection):
			# Paramiko SFTP object happens to have same behavior - copy it
			if not attr.startswith('__'):	# Without private fields/methods
				setattr(
						self,
						attr, 
						getattr(self.sftp_connection, attr),
					)