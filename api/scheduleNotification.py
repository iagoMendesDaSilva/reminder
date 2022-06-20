import os
import json
import requests

r = requests.post(os.getenv("REMINER_API_URL")+"notify", data=json.dumps({}))
print(r)