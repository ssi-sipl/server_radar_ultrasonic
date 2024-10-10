
import requests
import json

def send_http_command(url, method='POST', params=None, data=None, headers=None):
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage:
url = 'http://192.168.1.5:3300/analyticEvent'
method = 'POST'
data = {
    "cameraId": "RD001",
    "eventTime": 1233232,
    "timestampStr": 787878,
    "eventType": "Sensor_Event",
    "eventTag": "PIR SENSOR"
}
headers = {'Content-Type': 'application/json'}
response = send_http_command(url, method, data=json.dumps(data), headers=headers)
if response:
    print("Response:", response)
