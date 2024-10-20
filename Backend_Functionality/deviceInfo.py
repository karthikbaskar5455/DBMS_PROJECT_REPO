import platform
import socket
import os
import requests


def Get_Device_Info():
    # Get system OS details
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()

    # Get processor and machine details
    if os_name != "Windows":
        uname_info = os.uname()  # Get uname information
        # Read processor info from /proc/cpuinfo
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info = f.readlines()

        # Extract relevant processor information
        processor_brand = None
        for line in cpu_info:
            if line.startswith("model name"):
                processor_brand = line.split(":")[1].strip()
                break

        # Fallback if we don't find the brand
        if processor_brand is None:
            processor_brand = "Unknown processor"

        # Prepare the processor and machine info
        processor_info = f"{processor_brand}"
        machine_info = f"{uname_info.machine} architecture"
    else:
        processor_info = platform.processor()  # Better compatibility with Windows
        machine_info = platform.machine()  # Machine type for Windows

    # Get the external IP address
    try:
        external_ip_response = requests.get('https://api.ipify.org')
        ip_address = external_ip_response.text
    except requests.RequestException as e:
        ip_address = f"Could not retrieve external IP address: {e}"

    # Return device information as a dictionary
    return {
        "IP_Address": ip_address,
        "System_OS": os_name,
        "Release": os_release,
        "Version": os_version,
        "Machine_Info": machine_info,
        "Processor_Info": processor_info,
        
    }

def Get_Location_Info():
    device_info=Get_Device_Info()
    ip_address=device_info["IP_Address"]
    # Get location details using an external API
    location_info = {}
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        location_info = response.json()
    except requests.RequestException as e:
        location_info['error'] = f"Could not retrieve location info: {e}"

    # Return location information as a dictionary
    if 'error' in location_info:
        return {"error": location_info['error']}
    
    return {
        "Location_Coordinates": location_info.get('loc'),
        "Country_Code": location_info.get('country'),
        "Region": location_info.get('region'),
        "City": location_info.get('city'),
    }


#--THIS function is to be called during insertion
def Get_List_DeviceInfo():
    """
    IP_Address
    System_OS
    Release
    Version
    Machine
    Processor
    """
    device_info = Get_Device_Info()
    return(list(device_info.values()))

#--THIS function is to be called during insertion
def Get_List_LocationInfo():
    """
    Location_Coordinates
    Country_Code
    Region
    City
    """
    location_info = Get_Location_Info()
    return(list(location_info.values()))



# deviceInfo=Get_List_DeviceInfo()
# locationInfo=Get_List_LocationInfo()

# for i in deviceInfo:
#     print(i)

# print()

# for j in locationInfo:
#     print(j)
