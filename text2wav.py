import requests
import json
import hashlib

def generate_wav(text):
    url = f"http://127.0.0.1:8080/api/speechtext/{text}"
    res = requests.get(url)
    filename = hashlib.md5(text.encode("utf-8")).hexdigest() + ".wav"
    path = "output" + "/" + filename
    with open(path, "wb") as file:
        file.write(res.content)
    return path

if __name__ == "__main__":
    generate_wav("test")