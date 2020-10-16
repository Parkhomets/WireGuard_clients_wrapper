#!/usr/bin/python3
import subprocess
import sys
from termcolor import colored
CLIENTS_FILE = 'clients.txt'


def get_clients():
    clients = []
    with open(CLIENTS_FILE) as file:
        for line in file:
            clients.append([i.strip() for i in line.split('|')])
    return clients


def show_clients():
    clients = get_clients()
    for client in clients:
        print(colored('\nPeer:\t', 'magenta'), colored(client[0], 'yellow'))
        print(colored('Name:\t', 'magenta'), colored(client[1], 'blue'))
        print(colored('IP:\t', 'magenta'), client[2])


def get_client_by_key(key):
    for client in get_clients():
        if client[0] == key:
            return client


def get_client_by_name(name):
    clients = []
    for client in get_clients():
        if name.lower() in client[1].lower():
            clients.append(client)
    return clients


def show_all():
    stdoutdata = subprocess.getoutput("wg")
    for line in stdoutdata.split('\n'):
        headers = ['Name:', 'endpoint:', 'allowed ips:', 'latest handshake:', 'transfer:']
        if 'interface' in line:
            line = colored(line.split()[0], 'magenta') + " " + colored(line.split()[1], 'blue')
        if 'peer' in line:
            name = get_client_by_key(line.split()[1])[1]
            line = colored(line.split()[0], 'magenta') + " " + colored(line.split()[1], 'yellow')
            line += '\n  Name: {}'.format(colored(name, 'blue'))
        for header in headers:
            line = line.replace(header, colored(header, 'red'))
        print(line)


def show_client_info(client_info):
    cli_by_key = get_client_by_key(client_info)
    cli_by_name = get_client_by_name(client_info)
    if cli_by_key:
        stdoutdata = subprocess.getoutput("wg")
        for line in stdoutdata.split('\n\n'):
            if client_info in line:
                line = line.split('\n')
                for subline in line:
                    headers = ['Name:', 'endpoint:', 'allowed ips:', 'latest handshake:', 'transfer:']
                    if 'peer' in subline:
                        subline = colored(subline.split()[0], 'magenta') + " " + colored(subline.split()[1], 'yellow')
                        subline += '\n  Name: {}'.format(colored(cli_by_key[1], 'blue'))
                    for header in headers:
                        subline = subline.replace(header, colored(header, 'red'))
                    print(subline)
    else:
        stdoutdata = subprocess.getoutput("wg")
        for line in stdoutdata.split('\n\n'):
            for client in cli_by_name:
                if client[0] in line:
                    line = line.split('\n')
                    for subline in line:
                        headers = ['Name:', 'endpoint:', 'allowed ips:', 'latest handshake:', 'transfer:']
                        if 'peer' in subline:
                            subline = colored(subline.split()[0], 'magenta') + " " + colored(subline.split()[1], 'yellow')
                            subline += '\n  Name: {}'.format(colored(client[1], 'blue'))
                        for header in headers:
                            subline = subline.replace(header, colored(header, 'red'))
                        print(subline)
                    print()


def add_client(public_key, name, ip):
    clients = get_clients()
    for i in clients:
        if public_key in i:
            print(colored('Error: Client already exists', 'red'))
            return
        if ip in i:
            print(colored('Error: IP already exists', 'red'))
            return
        if name in i:
            print(colored('Error: Name already exists', 'red'))
            return


    stdoutdata = subprocess.getoutput("wg set wg0 peer '{}' allowed-ips {}".format(public_key, ip))
    clients.append([public_key, name, ip])
    if not stdoutdata:
        save_clients(clients)
        print(colored("OK", 'green'))
    else:
        print(colored('Error: ' + stdoutdata, 'red'))

    
def remove_client(public_key):
    clients = get_clients()
    control = len(clients)
    for i in clients:
        if public_key in i:
            client = i
            clients.remove(i)
    if len(clients) == control:
        print(colored('Error: No such client...', 'red'))
        return
    stdoutdata = subprocess.getoutput("wg set wg0 peer '{}' remove".format(public_key))
    if not stdoutdata:
        save_clients(clients)
        print(colored("Client", 'green'), colored(client[1], 'red'), colored("removed", 'green'))
    else:
        print(colored('Error: ' + stdoutdata, 'red'))


def save_clients(clients):
    with open(CLIENTS_FILE, 'w') as clients_file:
        for client in clients:
            clients_file.write('|'.join(client)+'\n')


def help():
    print('\nThis is WireGuard wrapper for more convenient working with users.\n')
    print('Usage:')
    print('`./wrapper` - show full info with user names')
    print('`./wrapper show` - show full info with user names')
    print('`./wrapper clients` - show all clients')
    print('`./wrapper client <public key>` - show full client info by publickey')
    print('         OR          ')
    print('`./wrapper client <name>` - show full client info by name')
    print('`./wrapper add <publickey> <name> <IP>` - add new client')
    print('`./wrapper remove <publickey>` - remove client\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        show_all()
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'show':
            show_all()
            exit()
        elif sys.argv[1] == 'clients':
            show_clients()
            exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'client':
            show_client_info(sys.argv[2])
            exit()
        elif sys.argv[1] == 'remove':
            remove_client(sys.argv[2])
            exit()
    elif len(sys.argv) == 5:
        if sys.argv[1] == 'add':
            add_client(sys.argv[2], sys.argv[3], sys.argv[4])
            exit()
    help()
