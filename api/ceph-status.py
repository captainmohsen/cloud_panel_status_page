import datetime
import time
import requests  # Install this if you don't have it already.

USER = "admin"
PASS = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"

PROMETHEUS = 'http://{}:{}@metric.kcdn.ir/'.format(USER, PASS)

resp = requests.get(PROMETHEUS + '/api/v1/query',
  params={
    'query': 'ceph_health_status'
  })
results = resp.json()['data']['result']
ceph_health_status = results[0]['value'][1]
print(ceph_health_status)
if ceph_health_status == '0':
    print("HEALTHY")
elif ceph_health_status == '1':
    print("WARNING")
elif ceph_health_status == '2':
    print("ERROR")
else:
    print("NULL")
