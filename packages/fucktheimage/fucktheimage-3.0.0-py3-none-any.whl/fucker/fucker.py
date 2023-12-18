import requests
import json

def upload_image(file_path):
    url = "https://pics.sunbangyan.cn/application/upload.php"
    files = {'file': open(file_path, 'rb')}
    
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return json.loads(response.text)["url"]
    else:
        return None