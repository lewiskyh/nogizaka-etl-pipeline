import requests
import json
from json import JSONDecodeError

def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_str = response.text.strip()[4:-2] # Remove "res (" and " ); "
        data = json.loads(json_str)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except JSONDecodeError as e:
        print(f"JSON decoding error: {e}")

def fetch_data():
    URL = "https://www.nogizaka46.com/s/n46/api/list/member"
    data = fetch_json(URL)
    if data:
        with open('/tmp/nogizaka46_data.json', 'w') as outfile:
            json.dump(data, outfile)
        print("Data successfully fetched and saved to /tmp/nogizaka46_data.json")