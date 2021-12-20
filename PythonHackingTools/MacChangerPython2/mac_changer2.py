#!usr/bin/env python

import subprocess
import argparse
import random
import re


def get_interface_and_mac_args():
    parser = argparse.ArgumentParser(description = "Changes MAC address of given Network Interface")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--mac", dest = "new_mac_address", help = "New specific MAC address")
    group.add_argument("-rm", "--randmac", dest = "random_mac_address", action = "store_true", help = "Generates new random MAC address")
    parser.add_argument("-i", "--interface", dest = "interface", help = "Network interface (to change its MAC address)")
    arguments = parser.parse_args()

    if not arguments.interface:
        parser.error("\n[-] Please specify an Interface. Use --help for more info.")

    if not arguments.new_mac_address and not arguments.random_mac_address:
        parser.error("\n[-] Please specify a new MAC Address, or use Random MAC Address option. Use --help for more info.")
        
    if arguments.random_mac_address:
        arguments.new_mac_address = generate_random_mac_address()

    return arguments.interface, arguments.new_mac_address
  
    
def generate_random_mac_address():
    random.seed()
    valid_characters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f]
    random_mac_address = ""
    is_valid_mac = False
    
    while not is_valid_mac:
        for i in range(1, 18):
            if i % 3 == 0:
                random_mac_address += ":"
                
            random_mac_address += random.choice(valid_characters)
        
        if not is_valid_mac_address(random_mac_address):
            random_mac_address = ""
            is_valid_mac = False
        else:
            is_valid_mac = True


    return random_mac_address     


def is_valid_mac_address(mac_address):
    if re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_address): # Not a None -> MAC Address is valid
        if mac_address != "00:00:00:00:00:00" and mac_address != "ff:ff:ff:ff:ff:ff":
            return True
        else: 
            return False
    else:
        return False


def is_valid_interface(interface):
    ifconfig_command_result = str(subprocess.check_output(["ifconfig", interface]))
    if re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_command_result): # If interface has MAC address => valid interface
        return True
    else:
        return False
        


def get_current_mac_address(interface):
    ifconfig_command_result = str(subprocess.check_output(["ifconfig", interface])) # check_output() -> bytes: result = str(bytes)
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_command_result) # search() -> group obj

    if mac_address_search_result:
        return mac_address_search_result.group(0) # MAC Address is the first element of the group obj
    else:
        return ""


def display_current_mac_address(current_mac_address):
    if is_valid_mac_address(current_mac_address):
        print("[+] Current MAC Address: " + current_mac_address)
    else:
        print("[-] Could not read MAC Address")


def change_mac_address(interface, new_mac_address):
    if is_valid_mac_address(new_mac_address) and is_valid_interface(interface):
        print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_address])
        subprocess.call(["ifconfig", interface, "up"])
    else:
        if not is_valid_mac_address(new_mac_address):
            print("[-] Please specify a valid new MAC Address")

        if not is_valid_interface(interface):
            print("[-] Please specify a valid Interface")


def check_if_changed_mac_address(interface, new_mac_address):
    current_mac_address = get_current_mac_address(interface)
    if current_mac_address == new_mac_address:
        print("[+] MAC Address was successfully changed to " + new_mac_address)
    else:
        print("[-] MAC Address failed to get changed")


def run_mac_changer_engine():
    interface, new_mac_address = get_interface_and_mac_args()
    current_mac_address = get_current_mac_address(interface)
    display_current_mac_address(current_mac_address)

    change_mac_address(interface, new_mac_address)
    check_if_changed_mac_address(interface, new_mac_address)


# Main:
if __name__ == "__main__":
    run_mac_changer_engine()