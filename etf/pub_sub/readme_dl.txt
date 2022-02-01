

publish to and subscribe from a server on the windows operating system.


pub: publish
sub: subscribe


server: windows registry key

registry editor
Computer\HKEY_CURRENT_USER\SOFTWARE\some\server\path\Servers\SERVER_NAME
Computer\HKEY_CURRENT_USER\SOFTWARE\Bluefin Trading LLC\Bluefin.P2P\Servers\LONDL


SERVER_NAME has many value hashes: {value_name, value_data}

we set up the following 2 hashes:
one for the port:  {port, 44803}
the other for the server:  {server, londondl.p2p.bluefintrading.com}

This is sufficient and necessary for connecting.



The API connects with this.
