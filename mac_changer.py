
"""Input syntax: python mac_changer.py eth0 00:11:22:33:44:55"""

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help = "Interface to change the MAC Address")
    parser.add_option("-m","--mac", dest = "new_mac", help = "New MAC Address")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
        print("Interface is eth0/wlan0/wlan1/l0.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return  options

def change_mac(interface , new_mac):
    print("[+] Changing MAC Address for " + interface + "to" + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address. ")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC : "+ str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC Address was successfully chnged to "+ current_mac)
else:
    print("[-] MAC Address did not get changed")