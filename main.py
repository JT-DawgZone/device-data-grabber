import json
import platform
import getmac
import requests
import argparse
import socket

def get_sys_info():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        finally:
            s.close()
    except socket.error:
        ip_address = "127.0.0.1"

    sys_info = {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "os": platform.system(),
        "architecture": platform.architecture()[0],
        "local_ip" : ip_address,
        "mac": getmac.get_mac_address(),
        "processor" : platform.processor(),
    }

    if sys_info["mac"] is None:  sys_info["mac"] = "Unknown"

    return sys_info

def get_geo_info(quiet=False):
    url = "http://ip-api.com/json/?fields=status,message,country,countryCode,region,city,lat,lon,isp,org,query"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        if data.get("status") == "fail":
            if not quiet:
                print("Error querying ip-api.com, outputting system data.")
            return {}

        return data

    except requests.exceptions.Timeout as e:
        if not quiet:
            print("Connection to the server has timed out, outputting system data.")
            print(f"Error: {e}")
        return {}
    except requests.exceptions.ConnectionError as e:
        if not quiet:
            print("DNS failure or lack of internet connectivity, outputting system data.")
            print(f"Error: {e}")
        return {}
    except requests.exceptions.RequestException as e:
        if not quiet:
            print(f"Error: {e}")
            print("Outputting system data.")
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gathers system and geolocation info about your device.")
    parser.add_argument("-o",
                        "--output",
                        action="store",
                        type=argparse.FileType("w"),
                        dest="output",
                        help="Directs the output to a named file, creates the file if it doesn't exist.")
    parser.add_argument("-q",
                        "--quiet",
                        action="store_true",
                        dest="quiet",
                        help="Suppresses error output and status messages.")

    args = parser.parse_args()

    info = get_sys_info() | get_geo_info(quiet=args.quiet)
    info.pop("status", None)
    info = json.dumps(info, indent=4)

    if args.output:
        args.output.write(info)
        args.output.close()
        if not args.quiet:
            print(f"Saved output to the path: {args.output.name}")
    else:
            print(info)