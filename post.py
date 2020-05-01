import requests
import json
data = {
    "query_id": "1001",
    "deal_id": "1588009932",
    "order_id": "101231121266",
    "order_time": 1583868012,
    "user_id": "10001",
    "bmid": "1000022",
    "location": "(25.021295, 121.539112)",
    "start_time": 1585134900,
    "end_time": 1585138500
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)
r = requests.post("http://127.0.0.1:5000/api/order/confirm/car",
                  data=json.dumps(data), headers=headers)
print(r.status_code, r.text)
