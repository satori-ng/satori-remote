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

	# monkey patch some remote utilities
	sftp.__dict__['path'] = os.path
	yield sftp

	# Close
	sftp.close()
	transport.close()



	# print (f.listdir('/'))