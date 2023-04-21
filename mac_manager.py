#!/usr/bin/python
#coding=utf-8
from telnetlib import Telnet
import sys

SWITCH_NAME = ""
SWITCH_MAC = ""
HOST_IP = ""
ACCOUNT_NAME = ""
PASSWORD = ""
VLAN_ID = ""


mac = SWITCH_MAC
host = HOST_IP
account = ACCOUNT_NAME
password = PASSWORD
config = 'conf t'


def mac_process(mac):
    '''
    input mac address with ":" seperated every 2 digits
    return mac address that meet with cisco command -> "." seperated every 4 digits
    '''
    mac = mac.lower().replace(':', '')
    return mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]


def telnet_process(choice, mac):
    '''
    process ban or unban the mac address
    '''

    # ban mac command
    ban_mac = 'mac address-table static ' + mac_process(mac) + ' vlan {} drop'.format(VLAN_ID)
    # unban mac command
    unlock_mac = 'no mac address-table static ' + mac_process(mac) + ' vlan {} drop'.format(VLAN_ID)
    # initialize telnet
    tn = Telnet(host)
    tn.read_until(b"Username:")
    #enter account name
    tn.write(account.encode('ascii') + b'\r\n')

    tn.read_until(b"Password:")
    # enter password
    tn.write(password.encode('ascii') + b'\r\n')

    tn.read_until(b"{}#".format(SWITCH_NAME))
    # entering configuration terminal
    tn.write(config.encode('ascii') + b'\r\n')
    tn.read_until(b"{}(config)#".format(SWITCH_NAME))

    if choice == 2:
        tn.write(ban_mac.encode('ascii') + b'\r\n')
        f = open('black_list.txt', 'a')
        f.write( '\n' + mac)
        f.close()
        print('{} has been banned!'.format(mac))

    elif choice == 3:
        tn.write(unlock_mac.encode('ascii') + b'\r\n')
        f = open('black_list.txt', 'r')
        line = f.read().replace('\n' + mac, '')
        f.close()
        f = open('black_list.txt', 'w+') 
        f.write(line)
        f.close()
        print('{} has been unbanned'.format(mac))
    

def black_list():
    f = open('black_list.txt')
    print(f.read())
    f.close()

if __name__ == '__main__':
    mac_select = int(sys.argv[1])
    
    if mac_select == 1:
        black_list()
    elif mac_select == 2 or mac_select == 3:
        mac = sys.argv[2]
        telnet_process(mac_select, mac)
    else:
        print('Invalid input, please enter again\n')
    
