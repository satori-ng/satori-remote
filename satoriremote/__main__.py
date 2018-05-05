import argparse

import satoriremote



parser = argparse.ArgumentParser()

parser.add_argument("--remote", 
		help="",
	)

parser.add_argument("--list", 
		help="",
		action="store_true",
	)



args = parser.parse_args()

if args.list:
	print (satoriremote.AVAILABLE_PROTOCOLS) 
if args.remote:
	
	conn = satoriremote.connect(args.remote)
	print(conn)
	with conn as obj:
		if obj:
			print ("[+] Connection Successful!")
		else:
			print ("[-] Connection Failed.") 