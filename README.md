# satori-remote
Package for Remote acquisition of Satori Images 

![logo4](https://github.com/satori-ng/Logos/blob/master/logos/light/logo4.png)

[![PyPI version](https://badge.fury.io/py/satori-remote.svg)](https://pypi.org/project/satori-remote) - `pip install satori-remote`

When this package is installed, `satori-imager` and `satori-differ` entrypoints can be used with remote system to create and diff *SatoriImage* files.

### The `satori-remote` entrypoint

When used as standalone, `satori-remote` tries to connect to the URL given as argument.

```bash
$ satori-remote --remote sftp://localhost
Username: user1 
Password:
[+] Connection Successful!
```

```bash
$ satori-remote --remote sftp://user1@localhost//etc/passwd 
Password:
[+] Connection Successful!
[+] 'stat' call to '/etc/passwd' succeded!
```

```bash
$ satori-remote --remote sftp://user1@localhost//etc/
Password:
[+] Connection Successful!
[+] 'stat' call to '/etc/' succeded!
[+] Directory Listing for '/etc/' succeded!
	Files under '/etc/':
gdbinit.d
chrony.conf
default
logrotate.conf
locale.conf
[...]
```
If the connection succeeds, equivalents of `stat` and `listdir` will be run, ensuring that a *SatoriImage* can be extracted from the remote host.


The connection argument accepts URL strings like:
```
  smb://username@host:445
  smb://username@host:445//SMBSHARE/share_folder/share_file
  sftp://host:22
  ssh://host:22
  sftp://username#pub_key_path@host:22
  sftp://username:password@host:22
  sftp://username:password@192.168.1.5:22  
```

currently working with `SSH/SFTP`. `SMB` support is also experimental.
