import re


def standard_format(mac_address):
    result = {
        'result': False,
        'message': ""
    }
    mac_address_list = []
    allowed_characters = re.compile('^[0-9a-fA-F]$')
    for char in mac_address:
        if allowed_characters.search(char):
            mac_address_list.append(char)
    if len(mac_address_list) < 12:
        result['message'] = "Not enough usable characters."
    elif len(mac_address_list) > 12:
        result['message'] = "Too many usable characters."
    else:
        result['result'] = True
        result['message'] = mac_address_list
    return result


def format_groups_of_2(mac_address, separator):
    temp = standard_format(mac_address)
    if not temp['result']:
        return temp['message']
    temp_mac_address = temp['message']
    formatted_mac_address = ""

    for index, char in enumerate(temp_mac_address):
        formatted_mac_address += char
        if (int(index) % 2) and (index != len(temp_mac_address) - 1):
            formatted_mac_address += separator

    return formatted_mac_address.capitalize()


def format_groups_of_4(mac_address, separator):
    temp = standard_format(mac_address)
    if not temp['result']:
        return temp['message']
    temp_mac_address = temp['message']
    formatted_mac_address = ""

    for index, char in enumerate(temp_mac_address):
        formatted_mac_address += char
        if not (int(index+1) % 4) and (index != len(temp_mac_address) - 1):
            formatted_mac_address += separator

    return formatted_mac_address.capitalize()

mac_address_in = input("Mac Address: ")
separator_character = input("Separating character: ")
selection = 0
print("Choose format:\n2.Groups of 2\n4.Groups of 4")
while not(selection == 2 or selection == 4):
    selection = int(input(""))
if selection == 2:
    formatted_mac = format_groups_of_2(mac_address_in, separator_character)
if selection == 4:
    formatted_mac = format_groups_of_4(mac_address_in, separator_character)

print (formatted_mac)
