from contextlib import contextmanager

import os
import paramiko


@contextmanager
def load(connection_dict):

	# Open a transport
	transport = paramiko.Transport(
			(
				connection_dict['host'],
				connection_dict['port']
			)
		)
	# transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# Auth
	transport.connect(
			username=connection_dict['username'],
			password=connection_dict['auth'],
		)

	# Go!
	sftp = paramiko.SFTPClient.from_transport(transport)

	sContext = SatoriSFTPContext(transport, sftp)

	yield sContext

	# Close
	sftp.close()
	transport.close()


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