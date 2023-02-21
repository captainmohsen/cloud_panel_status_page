import datetime
import time
import requests  # Install this if you don't have it already.

USER = "admin"
PASS = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"

PROMETHEUS = 'https://{}:{}@metric.kcdn.ir/'.format(USER, PASS)

#############################################################
days = []
today = datetime.datetime.today().date()


def get_date(day):
    favorite_date = today - datetime.timedelta(days=day)
    return favorite_date


day1 = {'date': get_date(2), 'ComputeService': {'status': '', 'up_time': ''},
        'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
        'CephService': {'status': '', 'up_time': ''}}

result = {'day1': {'date': get_date(6), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'day2': {'date': get_date(5), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'day3': {'date': get_date(4), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'day4': {'date': get_date(3), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'day5': {'date': get_date(2), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'day6': {'date': get_date(1), 'ComputeService': {'status': '', 'up_time': ''},
                   'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                   'CephService': {'status': '', 'up_time': ''}},
          'today': {'date': today, 'ComputeService': {'status': '', 'up_time': ''},
                    'NetworkService': {'status': '', 'up_time': ''}, 'StorageService': {'status': '', 'up_time': ''},
                    'CephService': {'status': '', 'up_time': ''}}}

def get_query(day_time):
    resp = requests.get(PROMETHEUS + '/api/v1/query',
                        params={
                            'query': 'avg_over_time(openstack_is_up[1d]) * 100',
                            'time': time.mktime(day_time.timetuple())
                        })
    res_results = resp.json()['data']['result']
    return res_results

def get_ceph_query(date_time):
    resp = requests.get(PROMETHEUS + '/api/v1/query',
                        params={
                            'query': 'avg_over_time(ceph_is_up[1d]) * 100',
                            'time': time.mktime(date_time.timetuple())
                        })
    res_results = resp.json()['data']['result']
    return res_results



def get_up_day(i,results):

    day_res = {'status': '', 'up_time': ''}
    if results and len(results)>1:
        up_time = results[i].get('value')[1]
    elif len(results)==1:
        up_time = results[0].get('value')[1]

    day_res.update([('up_time', up_time)])
    if float(up_time) >= 75:
        day_res.update([('status', 'OK')])
    elif float(up_time) > 50 and float(up_time) < 75:
        day_res.update([('status', 'WARNING')])
    else:
        day_res.update([('status', 'ERROR')])

    return day_res


def update_dic(key):
        res_results = get_query(result[key]['date'])
        res_ceph_results = get_ceph_query(result[key]['date'])
        result[key].update({'ComputeService': {'status': get_up_day(3,res_results)['status'],
                                               'up_time': get_up_day(3,res_results)['up_time']},
                            'NetworkService': {'status': get_up_day(2,res_results)['status'],
                                               'up_time': get_up_day(2,res_results)['up_time']},
                            'StorageService': {'status': get_up_day(1,res_results)['status'],
                                               'up_time': get_up_day(1,res_results)['up_time']},
                            'CephService': {'status': get_up_day(0,res_ceph_results)['status'],
                            'up_time': get_up_day(0,res_ceph_results)['up_time']}})

def get_final():
    for key in result:
        update_dic(key)
    return result
##################################################################
def get_openstack_uptime(day_time):
    resp = requests.get(PROMETHEUS + '/api/v1/query',
                        params={
                            'query': 'avg_over_time(openstack_is_up[1d]) * 100',
                            'time': time.mktime(day_time.timetuple())
                        })
    print(resp.text)
    results = resp.json()['data']['result']
 #   print(results)
    if not results:
        print("No DATA")
    # if results and results[0]:
    #     print(results[0].get('metric').get('module'))
    for res in results:
        print('{metric}: {value[1]}'.format(**res))
    #    print(res.get('metric').get('module'))
    #    print(res.get('value')[1])


def get_ceph_uptime(date_time):
    resp = requests.get(PROMETHEUS + '/api/v1/query',
                        params={
                            'query': 'avg_over_time(ceph_is_up[1d]) * 100',
                            'time': time.mktime(date_time.timetuple())
                        })
    print(resp.text)
    results = resp.json()['data']['result']

    if not results:
        print("Ceph No DATA")
    else:
        uptime = results[0]['value'][1]
        print("Ceph Uptime: ", uptime)


today = datetime.datetime.today().date()
days.append(today)
for day_index in range(29):
    day_time = datetime.datetime.today().replace(day=day_index + 1).date()

    today = datetime.datetime.today().date()

    week_ago = today - datetime.timedelta(days=day_index + 1)
    days.append(week_ago)
    # print(days)
    print("week_ago:", week_ago)

#    print("day_time:",day_time)
    # if week_ago == day_time:
    #     print("yesssssssssssssssss")
# for day in days:
#   print(day)
# get_openstack_uptime(week_ago)
    #get_ceph_uptime(week_ago)
    get_ceph_uptime(week_ago)
#get_ceph_uptime(today)


#print(get_final())
