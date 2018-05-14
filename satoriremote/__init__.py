import re

__version__ = '0.1.0'
__name__ = 'satori-remote'
__desc__ = 'Package for Remote acquisition of Satori Images'
__email__ = 'satori_ng@email.com'

# input() fix for python2/3
try: input = raw_input 
except NameError: pass    

AVAILABLE_PROTOCOLS = [
    'sftp',
    'ssh',
    'smb',
]


def parse_conn_string(conn_string):

    arg_regex = r'(\w*)://(((\w+)\\)?(\w*)(([:#])(.+))?@)?([\.\w]*)(\:(\d+))?(/(.+))?'
    m = re.match(arg_regex, conn_string)

    try:
        conn_dict={}
        conn_dict['protocol'] = m.group(1)
        conn_dict['domain'] = m.group(4)
        conn_dict['username'] = m.group(5)
        conn_dict['auth_type'] = "key" if m.group(7) == '#' else "passwd"
        conn_dict['auth'] = m.group(8)
        conn_dict['host'] =  m.group(9)
        try:
            conn_dict['port'] = int(m.group(11))
        except: # if :port is not defined
            if conn_dict['protocol'] == 'smb':
                conn_dict['port'] = 445
            elif conn_dict['protocol'] in ['ssh', 'sftp']:
                conn_dict['port'] = 22
            elif conn_dict['protocol'] == 'ftp':
                conn_dict['port'] = 21
            else:
                conn_dict['port'] = None

        conn_dict['path'] =  m.group(13)

        if conn_dict['username'] is None:
            conn_dict['username'] = input("Username: ")

        if conn_dict['auth'] is None:
            import getpass
            conn_dict['auth'] = getpass.getpass("Password:")
        return conn_dict
    except AttributeError:
        raise ValueError("'{}' is not a valid remote argument".format(conn_string))



def connect(remote_arg):
    """
Parses arguments like:

smb://username@host:445
sftp://host:22
ssh://host:22
sftp://username#pub_key_path@host:22
sftp://username:password@host:22
sftp://username:password@192.168.1.5:22

and opens a connection
    """
        
    conn_dict = parse_conn_string(remote_arg)

    # import pprint
    # pprint.pprint (conn_dict)     # TODO: Get it to debug logs

    if conn_dict['protocol'] not in AVAILABLE_PROTOCOLS:
        raise ValueError("Protocol '{}' not available".format(protocol))

    if conn_dict['protocol'] in ['sftp', 'ssh']:
        from satoriremote.sftp import load

    elif conn_dict['protocol'] in ['smb']:
        from satoriremote.smb import load

    else:
        raise ConnectionError(
                "Protocol '{}' not available".format(
                    conn_dict['protocol']
                )
            )

    return load(conn_dict), conn_dict



# con_arg = 'sftp://unused:pass@172.16.47.212'
