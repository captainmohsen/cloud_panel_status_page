import datetime
import time
import requests  # Install this if you don't have it already.

USER = "admin"
PASS = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"

PROMETHEUS = 'https://{}:{}@metric.kcdn.ir/'.format(USER, PASS)


def get_openstack_uptime(day_time):
  resp = requests.get(PROMETHEUS + '/api/v1/query',
    params={
      'query': 'avg_over_time(openstack_is_up[1d]) * 100',
      'time': time.mktime(day_time.timetuple())
    })
  print(resp.text)
  results = resp.json()['data']['result']

  if not results:
      print("No DATA")
  else:
      uptime = results[0]['value'][1]
      print("Openstack Uptime: ", uptime)


def get_ceph_uptime(date_time):
    resp = requests.get(PROMETHEUS + '/api/v1/query',
                        params={
                            'query': 'avg_over_time(ceph_is_up[1d]) * 100',
                            'time': time.mktime(day_time.timetuple())
                        })
    print(resp.text)
    results = resp.json()['data']['result']

    if not results:
        print("No DATA")
    else:
        uptime = results[0]['value'][1]
        print("Ceph Uptime: ", uptime)

for day_index in range(29):
  day_time = datetime.datetime.today().replace(day=day_index+1).date()
  print(day_time)
  get_openstack_uptime(day_time)
  get_ceph_uptime(day_time)