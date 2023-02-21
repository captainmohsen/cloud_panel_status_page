import datetime
import time
import requests  # Install this if you don't have it already.

USER = "admin"
PASS = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"

PROMETHEUS = 'https://{}:{}@metric.kcdn.ir/'.format(USER, PASS)

resp = requests.get(PROMETHEUS + '/api/v1/query',
  params={
    'query': 'sum(openstack_nova_agent_state) by (service)'
  })
print(resp.text)
results = resp.json()['data']['result']

for res in results:
    print('{metric}: {value[1]}'.format(**res))

if results and all(res['value'][1] for res in results):
    print("NOVA OK")
else:
    print("NOVA ERROR")

resp = requests.get(PROMETHEUS + '/api/v1/query',
  params={
    'query': 'sum(openstack_neutron_agent_state) by (service)'
  })
results = resp.json()['data']['result']

for res in results:
    print('{metric}: {value[1]}'.format(**res))

if results and all(res['value'][1] for res in results):
    print("NEUTRON OK")
else:
    print("NEUTRON ERROR")

resp = requests.get(PROMETHEUS + '/api/v1/query',
  params={
    'query': 'sum(openstack_cinder_agent_state) by (service)'
  })
results = resp.json()['data']['result']

for res in results:
    print('{metric}: {value[1]}'.format(**res))

if results and all(res['value'][1] for res in results):
    print("CINDER OK")
else:
    print("CINDER ERROR")
