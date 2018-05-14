import argparse
import sys

import satoriremote


def main():


	parser = argparse.ArgumentParser()

	parser.add_argument("--remote", '-r',
			help="The connection string to test",
		)

	parser.add_argument("--list", '-l',
			help="",
			action="store_true",
		)

	args = parser.parse_args()

	if not args.list and not args.remote:
		parser.print_usage()
		sys.exit(-1)

	if args.list:
		print (satoriremote.AVAILABLE_PROTOCOLS) 

	if args.remote:
		conn, conn_dict = satoriremote.connect(args.remote)

		with conn as obj:
			if obj:
				print ("[+] Connection Successful!")
			else:
				print ("[-] Connection Failed.") 

			if conn_dict['path']:
				try:
					st_res = obj.lstat(conn_dict['path'])
					print ("[+] 'stat' call to '{}' succeded!".
							format(conn_dict['path'])
						)
					# print (st_res)

				except Exception as e:
					# print (e)
					print ("[-] Failed to use 'stat' on remote file '{}'".
							format(conn_dict['path'])
					) 
					sys.exit(1)
				try:
					import stat
					if stat.S_ISDIR(st_res.st_mode):
						dlist = obj.listdir(conn_dict['path'])
						print ("[+] Directory Listing for '{}' succeded!".
								format(conn_dict['path'])
							)
						print (
								"\tFiles under '{}':".format(
									conn_dict['path']
								)
							)
						[ print (f) for f in dlist ]
						
				except Exception as e:
					# print (type(e))
					print ("[-] Failed to list directory: '{}'".
							format(conn_dict['path'])
					) 
					sys.exit(2)


if __name__ == '__main__':
	main()