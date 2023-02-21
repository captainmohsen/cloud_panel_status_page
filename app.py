from flask import Flask, json , render_template
import datetime
import time
import requests  # Install this if you don't have it already.
from atlassian import ServiceDesk
from config import StatusConfig


#importtant_functions
#-----------------------------------------------------------
def get_date(day):
    favorite_date = today - datetime.timedelta(days=day)
    return favorite_date

def get_weeks_day():
    for day_index in range(6):
         week_ago = today - datetime.timedelta(days=day_index+1)
         days.append(week_ago)
    return days

def get_query(day_time):
    resp = requests.get(StatusConfig.query_url,
                        params={
                            'query': StatusConfig.uptime_query,
                            'time': time.mktime(day_time.timetuple())
                        })
    res_results = resp.json()['data']['result']
    return res_results

def get_ceph_query(date_time):
    resp = requests.get(StatusConfig.query_url,
                        params={
                            'query': StatusConfig.ceph_uptime_query,
                            'time': time.mktime(date_time.timetuple())
                        })
    res_results = resp.json()['data']['result']
    return res_results


def get_up_day(i,results):
    day_res = {'status': '', 'up_time': '','flag':''}
    if results and len(results)>1:
        up_time = results[i].get('value')[1]
    elif len(results)==1:
        up_time = results[0].get('value')[1]

    day_res.update([('up_time', round(float(up_time),2))])
    if float(up_time) >= 75:
        day_res.update([('status', 'OK')])
        day_res.update([('flag', 'glyphicon  glyphicon-ok-sign status-success')])
    elif float(up_time) > 50 and float(up_time) < 75:
        day_res.update([('status', 'WARNING')])
        day_res.update([('flag', 'glyphicon glyphicon-exclamation-sign status-warning')])

    else:

        day_res.update([('status', 'ERROR')])
        day_res.update([('flag', 'glyphicon glyphicon-remove-sign status-danger')])


    return day_res

def update_dic(key):
        res_results = get_query(final_result[key]['date'])
        res_ceph_results = get_ceph_query(final_result[key]['date'])
        final_result[key].update({'ComputeService': {'status': get_up_day(3,res_results)['status'],
                                               'up_time': get_up_day(3,res_results)['up_time'],
                                               'flag': get_up_day(3,res_results)['flag']},
                            'NetworkService': {'status': get_up_day(2,res_results)['status'],
                                               'up_time': get_up_day(2,res_results)['up_time'],
                                               'flag': get_up_day(2,res_results)['flag']},
                            'StorageService': {'status': get_up_day(1,res_results)['status'],
                                               'up_time': get_up_day(1,res_results)['up_time'],
                                               'flag': get_up_day(1,res_results)['flag']},
                            'CephService': {'status': get_up_day(0,res_ceph_results)['status'],
                             'up_time': get_up_day(0,res_ceph_results)['up_time'],
                             'flag': get_up_day(0,res_ceph_results)['flag']}})


# def get_final_result():
#     for key in result:
#         update_dic(key)
#     return result

#-----------------------------------------------------------

#important_params
#==============================================================
sd = ServiceDesk(
        url= StatusConfig.servicedesk_url,
        username= StatusConfig.servicedesk_user,
        password= StatusConfig.servicedesk_pass)

today=datetime.datetime.today().date()

incidents = []
resolved_incidents = []
CR = []
days = [today]


final_result = {'day1': {'date': get_date(6), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '', 'flag':''}},
          'day2': {'date': get_date(5), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '','flag':''}},
          'day3': {'date': get_date(4), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '','flag':''}},
          'day4': {'date': get_date(3), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '','flag':''}},
          'day5': {'date': get_date(2), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '','flag':''}},
          'day6': {'date': get_date(1), 'ComputeService': {'status': '', 'up_time': '','flag':''},
                   'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                   'CephService': {'status': '', 'up_time': '','flag':''}},
          'today': {'date': today, 'ComputeService': {'status': '', 'up_time': '','flag':''},
                    'NetworkService': {'status': '', 'up_time': '','flag':''}, 'StorageService': {'status': '', 'up_time': '','flag':''},
                    'CephService': {'status': '', 'up_time': '','flag':''}}}

fresult = {'ComputeService':{'status': '', 'flag':''},'NetworkService':{'status': '', 'flag':''},'StorageService':{'status': '', 'flag':''},
'CephService':{'status': '', 'flag':''}}

#=====================================================================================================================


api = Flask(__name__,static_url_path='/static')


#main api route for getting status and upadte related dict
@api.route('/Apistatus', methods=['GET'])
def get_status_api():
  nova_resp = requests.get(StatusConfig.query_url,
  params={
    'query': StatusConfig.nova_query
  })
  nova_results = nova_resp.json()['data']['result']

  if nova_results and all(res['value'][1] for res in nova_results):
      fresult.update({'ComputeService':{'status':'OK','flag':'glyphicon  glyphicon-ok-sign status-success'}})
  elif not nova_results:
      print ("not result")
      pass
  else:
      fresult.update({'ComputeService':{'status':'ERROR','flag':'glyphicon glyphicon-remove-sign status-danger'}})

  neutron_resp = requests.get(StatusConfig.query_url,
  params={
    'query': StatusConfig.neutron_query
  })
  neutron_results = neutron_resp.json()['data']['result']
  if neutron_results and all(res['value'][1] for res in neutron_results):
      fresult.update({'NetworkService':{'status':'OK','flag':'glyphicon  glyphicon-ok-sign status-success'}})
  elif not neutron_results:
      print("not result")
      pass
  else:
      fresult.update({'NetworkService':{'status':'ERROR','flag':'glyphicon glyphicon-remove-sign status-danger'}})


  cinder_resp = requests.get(StatusConfig.query_url,
  params={
    'query': StatusConfig.cinder_query
  })
  cinder_results = cinder_resp.json()['data']['result']

  if cinder_results and all(res['value'][1] for res in cinder_results):
      fresult.update({'StorageService':{'status':'OK','flag':'glyphicon  glyphicon-ok-sign status-success'}})
  else:
      fresult.update({'StorageService':{'status':'ERROR','flag':'glyphicon glyphicon-remove-sign status-danger'}})

  ceph_resp = requests.get(StatusConfig.query_url,
  params={
    'query': StatusConfig.ceph_query
  })
  ceph_results = ceph_resp.json()['data']['result']
  ceph_health_status = ceph_results[0]['value'][1]

  if ceph_health_status == '0':
    fresult.update({'CephService':{'status':'OK','flag':'glyphicon  glyphicon-ok-sign status-success'}})
  elif ceph_health_status == '1':
    fresult.update({'CephService':{'status':'WARNING','flag':'glyphicon glyphicon-exclamation-sign status-warning'}})
  elif ceph_health_status == '2':
    fresult.update({'CephService':{'status':'ERROR','flag':'glyphicon glyphicon-remove-sign status-danger'}})
  else:
    fresult.update({'CephService':{'status':'ERROR','flag':'glyphicon glyphicon-remove-sign status-danger'}})
  print(fresult)
#  return render_template('index.html', result = fresult)
  my_requests = sd.get_queues(1)
  issues = sd.get_issues_in_queue(1, 5)
  incidents[:] = issues.get("values")
  resolved_issues =  sd.get_issues_in_queue(1, 15)
  resolved_incidents[:] = resolved_issues.get("values")
  # cr_issue = sd.get_issues_in_queue(2, 26)
  # CR[:] = cr_issue.get("values")
#  print(incidents)

  return json.dumps(fresult)

@api.route('/uptime', methods=['GET'])
def get_uptime_api():
    for key in final_result:
         update_dic(key)
    return json.dumps(final_result)

#main route for displaying status
@api.route('/status', methods=['GET'])
def get_status():
  # my_requests = sd.get_queues(1)
  # issues = sd.get_issues_in_queue(1, 5)
  # incidents = issues.get("values")

  return render_template('index.html', result =fresult,incident=incidents,resolved=resolved_incidents,final_res=final_result,cr_res =CR)


#additional route for displaying incidents of jira_service_desk
@api.route('/incidents', methods=['GET'])
def get_incidents():
  my_requests = sd.get_queues(1)
  issues = sd.get_issues_in_queue(1, 5)
  incidents = issues.get("values")
  resolved_issues =  sd.get_issues_in_queue(1, 15)
  resolved_incidents[:] = resolved_issues.get("values")
  return json.dumps(incidents)

#route of login page
@api.route('/loginpage')
def go_to_login():
    return render_template('login.html')

#route of incident history
@api.route('/history')
def incidents_history():
    return render_template('history.html',resolved=resolved_incidents)



if __name__ == '__main__':
    api.run(host= StatusConfig.flask_host,debug=True)
