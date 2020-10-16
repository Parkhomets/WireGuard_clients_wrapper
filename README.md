# WireGuard_clients_wrapper
Working with clients in WireGuard is not very convenient in terms of names. Of course, this is a very cool service, but there is a small detail missing, which I hope the developers will correct. But for now, I made the following script for myself, which makes working with users more convenient.  
What is it for? It allows you to bind public keys and addresses to names (usernames), adds names to standard output, allows you to search for connections by name, and easily delete and add clients

## Installation 
1) git clone https://github.com/Parkhomets/WireGuard_clients_wrapper
2) pip3 install termcolor
3) mv WireGuard_clients_wrapper/wrapper.py /etc/wireguard/wrapper.py
4) chmow +x wrapper.py


## Usage
`./wrapper.py` - show full info with user names  
`./wrapper.py show` - show full info with user names   
`./wrapper.py clients` - show all clients (short info)  
`./wrapper.py client <public key>` - show full client info by publickey  
OR  
`./wrapper.py client <name>` - show full client info by name  
`./wrapper.py add <publickey> <name> <IP>` - add new client  
`./wrapper.py remove <publickey>` - remove client by publickey  
