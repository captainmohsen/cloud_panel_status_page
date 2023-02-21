class StatusConfig():
    prometheus_user = "admin"
    prometheus_pass = "bXn7PYzPc3wDSYVrXjzJ3E3Ba55AF3"
    prometheus_url = 'https://{}:{}@metric.kcdn.ir/'.format(prometheus_user, prometheus_pass )
    # servicedesk_url = 'http://localhost:8080/'
    # servicedesk_user = 'mohsen.baghdadi'
    # servicedesk_pass = '8312031'
    servicedesk_url = 'http://185.194.76.24:8080'
    servicedesk_user = 'mohsen.baghdadi'
    servicedesk_pass = '8312031'
    query_url = prometheus_url + '/api/v1/query'
    nova_query = 'sum(openstack_nova_agent_state) by (service)'
    neutron_query = 'sum(openstack_neutron_agent_state) by (service)'
    cinder_query = 'sum(openstack_cinder_agent_state) by (service)'
    ceph_query = 'ceph_health_status'
    uptime_query = 'avg_over_time(openstack_is_up[1d]) * 100'
    ceph_uptime_query = 'avg_over_time(ceph_is_up[1d]) * 100'
    flask_host = "172.16.13.81"
