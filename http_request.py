import requests
import json
import time 

def send_http_command(url, method='POST', params=None, data=None, headers=None):
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
# Example usage:
url = 'http://192.168.1.5:3300/analyticEvent' #url for AI BOX
#url = 'http://192.168.0.79:80' #url for testing on local server
method = 'POST'
data = {
            "cameraId": "RD001",
            "eventTime": int(time.time()),
            "timeStampStr": time.strftime("%Y-%m-%d %H:%M:%S"),
            "eventType": "Sensor_Event",
            "eventTag": "distance"
        }
headers = {'Content-Type': 'application/json'}
response = send_http_command(url, method, data=json.dumps(data), headers=headers)
if response:
    print("Response:", response)
