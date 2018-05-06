import re

__version__ = '0.1.0'
__name__ = 'satori-remote'
__desc__ = 'Package for Remote acquisition of Satori Images'
__email__ = 'satori_ng@email.com'



AVAILABLE_PROTOCOLS = [
    'sftp',
    'ssh',
    # 'smb',
]


def parse_conn_string(conn_string):
    arg_regex = r'(\w*)://((\w*)(([:#])(.+))?@)?([\.\w]*)(\:(\d+))?'
    m = re.match(arg_regex, conn_string)

    try:
        conn_dict={}
        conn_dict['protocol'] = m.group(1)
        conn_dict['username'] = m.group(3)
        conn_dict['auth_type'] = "key" if m.group(5) == '#' else "passwd"
        conn_dict['auth'] = m.group(6)
        conn_dict['host'] =  m.group(7)
        conn_dict['port'] = m.group(8)

        if conn_dict['username'] is None:
            conn_dict['username'] = raw_input("Username:")

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

        return load(
                    conn_dict['host'], conn_dict['username'],

                    password=conn_dict['auth'] if conn_dict['auth_type'] == 'passwd' else None,
                    pub_key_path=conn_dict['auth'] if conn_dict['auth_type'] == 'key' else None,
                    port=conn_dict['port'],
                ), conn_dict['host']

    raise ConnectionError("Connection could not be made!")


# con_arg = 'sftp://unused:pass@172.16.47.212'
