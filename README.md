# device-data-grabber
A simple python script that uses some standard python libraries to gather info about the current system as well as geolocation data based off of public IP information using ip-api.com.

# Standard execution to stdout
python footprint.py

# Export formatted JSON to a file
python footprint.py -o host_audit.json

# Quiet mode execution for automated pipelines
python footprint.py -q -o host_audit.json
