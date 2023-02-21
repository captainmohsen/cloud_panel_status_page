import datetime
import time
import requests  # Install this if you don't have it already.

USER = "admin"
PASS = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"

PROMETHEUS = 'https://{}:{}@metric.kcdn.ir/'.format(USER, PASS)


def get_openstack_state(day_time):
  resp = requests.get(PROMETHEUS + '/api/v1/query',
    params={
      'query': 'min(openstack_agent_state) by (module)',
      'time': time.mktime(day_time.timetuple())
    })
  print(resp.text)
  results = resp.json()['data']['result']

  for res in results:
      print('{metric}: {value[1]}'.format(**res))
  if not results:
      print("No DATA")
  elif all(res['value'][1] for res in results):
      print("Openstack OK")
  else:
      print("Openstack ERROR")

for day_index in range(6):
  day_time = datetime.datetime.today().replace(day=day_index+1).date()
  today=datetime.datetime.today().date()
  week_ago = today - datetime.timedelta(days=day_index+1)
  print(week_ago)
  print(day_time)
  get_openstack_state(day_time)
