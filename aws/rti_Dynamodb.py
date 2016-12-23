from __future__ import print_function # Python 2/3 compatibility
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

table = dynamodb.Table('EnsembleData')

response = table.put_item(
    Item={
        "Second": 16,
        "Year": 2016,
        "HSec": 8,
        "image": 0,
        "DesiredPingCount": 1,
        "element_multiplier": 1,
        "Month": 12,
        "SysFirmwareRevision": 54,
        "DateTime": "2016-12-23 01:13:16.080000",
        "Status": 512,
        "SysFirmwareMajor": 0,
        "SubsystemConfig": 0,
        "Name": "E000008",
        "SysFirmwareSubsystemCode": "2",
        "SerialNumber": "01200000000000000000000000000208",
        "SysFirmwareMinor": 5,
        "name_len": 8,
        "NumBeams": 4,
        "ds_type": 10,
        "Minute": 13,
        "Meta":
            {
                "Host": "Ricos-MBP-2.attlocal.net",
                "HostExtIp": "104.54.6.207",
                "HostIp": "192.168.1.241",
                "Revision": "1.0"
            },
        "num_elements": 23,
        "EnsembleNumber": 21122,
        "NumBins": 30,
        "Hour": 1,
        "Day": 23,
        "ActualPingCount": 1
    }
)

print("PutItem succeeded:")
print(json.dumps(response, indent=4))