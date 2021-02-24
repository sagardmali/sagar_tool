import time
import ast
import json
import base64
import requests
import urllib3
import yaml
import flex_env
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def token_authenticate(default_username=flex_env.username,\
                        default_password=flex_env.password):
        """
        Funtion to get token for authentication
        """
        try:
            sesion = requests.Session()
            sesion.verify = False
            data = {}
            data['password'] = default_password
            data['username'] = default_username
            d_a_t_a = json.dumps(data)
            response = sesion.post(flex_env.auth_url, data=d_a_t_a)
            return response
        except Exception('Token authenticate failed : {}'.format(data)):
            raise Exception('Failed to authenticate with  : {}'.format(data))

def run_api(**kwargs):
        '''
        This function forms requests for api
        :param url: Request URL
        :param rq_type: Type of request(get,post,delete,update)
        :param headers:Header for the request
        :param data: Data to be sent to request(this is for put request type)
        :return: The request output for vcenter api
        '''
        url = kwargs['url']
        rq_type = kwargs.get('rq_type', "get")
        headers = kwargs.get('headers', None)
        data = kwargs.get('data', None)
        authenticate = kwargs.get('authenticate', True)
        token_username = kwargs.get('token_username', None)
        token_password = kwargs.get('token_password', None)
        if authenticate:
            if token_username and token_password:
                token = token_authenticate(\
                    default_username=token_username, \
                    default_password=token_password)
            else:
                token = token_authenticate()
            session_id = token.json()['token']
            if headers is None:
                headers = {"content-type": "application/json", "accept":\
                        "application/json", "x-auth-token": session_id}
        elif not authenticate and headers:
            headers = headers
        else:
            headers = {"content-type": "application/json", "accept": "*/*"}

        if rq_type == 'get':
            resp = requests.get(url=url, params=data, headers=headers,\
                verify=False)
        elif rq_type == 'post':
            data = json.dumps(data)
            resp = requests.post(url=url, data=data, headers=headers,\
            verify=False)
        elif rq_type == 'delete':
            resp = requests.delete(url=url, headers=headers, verify=False)
        elif rq_type == 'put' and data != None:
            data = json.dumps(data)
            resp = requests.put(url=url, data=data, headers=headers,\
            verify=False)
        elif rq_type == 'patch' and data != None:
            data = json.dumps(data)
            resp = requests.patch(url=url, data=data, headers=headers,\
                verify=False)
        else:
            raise Exception("The request type {} is not valid"\
        .format(rq_type))
        return resp

def change_admin_password(node_ip='thunder_vip', oldpassword='P@ssw0rd',\
        newpassword='P@ssw0rdpassword', username='admin'):
        """
        :param : password
                newpassword
                username
        :return: json content
        """
        #auth_url = 'https://{}/authservice/api/v1/auth'.format(node_ip)
        auth_url = 'https://{}/authservice/api/v1/login'.format(node_ip)
        sesion = requests.Session()
        sesion.verify = False
        data = {}
        data['password'] = oldpassword
        data['username'] = username
        d_a_t_a = json.dumps(data)
        token = sesion.post(auth_url, data=d_a_t_a)
        session_id = token.json()['token']
        userid = token.json()['userId']
        username = token.json()['username']
        headers = {"content-type": "application/json", "accept": \
                "application/json", "x-auth-token": session_id}
        data = {}
        data = {"id":"xxx", "newPassword":"xxx", "currentPassword":\
            "xxx", "username": "xxx"}
        data["id"] = userid
        data["newPassword"] = newpassword
        data["currentPassword"] = oldpassword
        data["username"] = username
        url = 'https://{}/authservice/api/v1/users/local/{}/password'.format(\
            node_ip, username)
        res = run_api(url=url, rq_type='put', data=data,\
            headers=headers, authenticate=False)
        if res.status_code != 200:
            raise Exception('Failed to change password {}'.format(res.json()))
        return res.status_code

def wait_for_task_to_complete(task_id, timeout=30):
        """
        :param : task_id
                 timeout
        :return: json content
        """
        counter = 0
        while counter < timeout:
            task = get_task_status_by_id(task_id)
            if task['status']['status'] == 'DONE':
                return True
            if task['status']['status'] == 'FAILED':
                return task
            counter += 1
            time.sleep(6)
        return task

def get_task_status_by_id(task_id):
        """
        :param : task_id
        :return: json content
        """
        url = '{}/tasks/{}'.format(flex_env.api_url, task_id)
        res = run_api(url=url, rq_type='get')
        if res.status_code != 200:
            raise Exception('Failed to retrive status for task id {}\n {}'.\
                            format(task_id, res.json()))
        return res.json()

def iiinstall_applications(filename, image_type):
        """ POST Api for installing applications and add-on in repository.
        :param filename: rpm file name
        :param image_type: application/add-on
        :return: json content
        """
        url = '{}/applications/{}?image-type={}'.format(
            flex_env.api_url, filename, image_type)
        res = run_api(url=url, rq_type='post')
        if res.status_code != 200:
            if res.status_code == 400:
                return json.dumps(res.json())
            raise Exception('Failed to post install applications Api {}'
                            .format(res.json()))

        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=130)
        if status is True:
            return True
        else:
            raise Exception('Failed to install applications Api {} and \
        reason is {}'.format(status['status']['status'], \
        status['taskMessages']))


def install_applications(filename, image_type):
        """ POST Api for installing applications and add-on in repository.
        :param filename: rpm file name
        :param image_type: application/add-on
        :return: json content
        """

        url = '{}/applications/{}?image-type={}'.format(
            flex_env.api_url, filename, image_type)
        res = run_api(url=url, rq_type='post')
        if res.status_code != 200:
            if res.status_code == 400:
                return json.dumps(res.json())
            raise Exception('Failed to post install applications Api {}'
                            .format(res.json()))

        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=130)
        if status is True:
            return True
        else:
            raise Exception('Failed to install applications Api {} and \
        reason is {}'.format(status['status']['status'], \
        status['taskMessages']))

def configure_vlan(**kwargs):
        """
        :param : "macvlan_interface"
                    "macvlan_tag"
                    "macvlan_name"
                    "node_name"
                    "macvlan_subnet"
                    "macvlan_gateway"
                    "ipv6"
        :return: json content
        """
        data = {}
        data = {"interface":"", \
                "name":"XXX", "node-name":"", \
                "subnet":"", "gateway":"", \
                "ipv6":""}
        data["interface"] = kwargs.get("interface")
        data["name"] = kwargs.get("name")
        data["node-name"] = kwargs.get("node_name")
        data["subnet"] = kwargs.get("subnet")
        data["gateway"] = kwargs.get("gateway")
        data["ipv6"] = kwargs.get("ipv6")

        url = '{}/network/vlans/0'.format(flex_env.api_url)
        print(url)
        print(data)
        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception('Failed to create VLAN : {}'\
                .format(json.dumps(res.json())))
        return json.dumps(res.json())

def edit_vlan_config(**kwargs):
        """
        :param : "interface"
                    "node_name"
                    "mtu"
        :return: json content
        """
        data = {}
        data = {"interface":"", "node_name":"", "mtu":""}
        data["interface"] = kwargs.get("interface")
        data["node_name"] = kwargs.get("node_name")
        data["mtu"] = kwargs.get("mtu")

        url = '{}/network/mtu'.format(api_url)

        res = run_api(url=url, rq_type='put', data=data)
        if res.status_code != 200:
            raise Exception('Failed to edit VLAN : {}'\
                .format(json.dumps(res.json())))
        return json.dumps(res.json())

def post_tenant(**kwargs):
        """
        :param : "name"
                "location"
                "emails"
                "domainName"
                "searchDomains"
                "nameServers"
                "etcHostsPath"
        :return: json content
        """
        data = {}
        data = {"id":"", "name":"XXX", "location":"XXX", "emails":[], \
            "network":{"domainName":"XXX", "searchDomains":["XXX"], \
            "nameServers":["XXX", "XXX"], "etcHostsPath":""}, \
            "storage":{}, "applications":[]}
        data["name"] = kwargs.get("name")
        data["location"] = kwargs.get("location")
        data["emails"] = kwargs.get("emails", [])
        data["network"]["domainName"] = kwargs.get("domainName")
        data["network"]["searchDomains"] = kwargs.get("searchDomains", [])
        data["network"]["nameServers"] = kwargs.get("nameServers", [])
        data["network"]["etcHostsPath"] = kwargs.get("etcHostsPath")
        data["storage"] = kwargs.get("storage", {})
        data["applications"] = kwargs.get("applications", [])

        url = '{}/tenants'.format(flex_env.api_url)
        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception(
                'Failed to post tenant : {}'.format(json.dumps(res.json())))
        return json.dumps(res.json())

def get_tenant():
        """
        :return: jso content
        """
        url = '{}/tenants'.format(flex_env.api_url)
        res = run_api(url=url, rq_type='get')
        if res.status_code != 200:
            raise Exception(
                'Failed to Get tenant : {}'.format(res.json()))
        return json.dumps(res.json())

def post_user(**kwargs):
        """ post Users
        :param : "subject"
                "password"
                "fullName"
                "idpType"
        :return: json content
        """

        data = {}
        data = {"subject":"XXX", "password":"XXX", "fullName":"XXX", \
                "idpType":"XXX"}
        data["subject"] = kwargs.get("subject")
        data["password"] = kwargs.get("password")
        data["fullName"] = kwargs.get("fullName")
        data["idpType"] = kwargs.get("idpType", "local")
        token_username = kwargs.get('token_username', None)
        token_password = kwargs.get('token_password', None)
        url = '{}/users/local/{}'.format(flex_env.policy_auth_url, data["subject"])
        if token_username and token_password:
            res = run_api(url=url, rq_type='post', data=data, \
            token_username=token_username, token_password=token_password)
        else:
            res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 201:
            raise Exception('Failed to put users {}'.format(res.json()))
        return res

def create_bond_api(**kwargs):
        """
        :param : "bond_name"
                    "mode"
                    "node"
                    "interfaces"
        :return: json content
        """
        data = {}
        data = {"bond_name":"XXX", "mode":"XXX", \
                "node":"XXX", "interfaces":[]}
        data["bond_name"] = kwargs.get("bond_name")
        data["mode"] = kwargs.get("mode")
        data["node"] = kwargs.get("node")
        data["interfaces"] = kwargs.get("interfaces", [])

        url = '{}/network/bonds'.format(flex_env.api_url)

        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception('Failed to create bond : {}'\
                .format(json.dumps(res.json())))

        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=50)
        if status is True:
            return "DONE"
        else:
            raise Exception('Failed to create bond : {}'\
                .format(status['status']['status']))

def get_tenant():
        """
        :return: json content
        """

        url = '{}/tenants'.format(flex_env.api_url)
        res = run_api(url=url, rq_type='get')
        if res.status_code != 200:
            raise Exception(
                'Failed to Get tenant : {}'.format(res.json()))
        return res.json()

def master_server(**kwargs):
        """
        :param : application_version_xx="8.2"
                hostname
                interface
                ipaddress
                tenant
                domainname
                nameservers
                searchdomains
                etchosts
                catalog
                env_nb_regkey
                env_nb_lickey
                env_nb_svc_up
        :return: True
        """
        data = {}
        data = {"network":[], "envvars":[], "volume":[]}
        data["network"].append({"id": "hostname_netbackup/main_XX",\
                                "value": kwargs.get('hostname')})
        data["network"].append({"id": "interface_netbackup/main_XX",\
                                "value": kwargs.get('interface')})
        data["network"].append({"id": "ipaddress_netbackup/main_XX",\
                                "value": kwargs.get('ipaddress')})
        data["network"].append({"id": "tenant_netbackup/main_XX",\
                                "value": kwargs.get('tenant')})
        data["network"].append({"id": "domainname_netbackup/main_XX",\
                                "value": kwargs.get('domainname')})
        data["network"].append({"id": "nameservers_netbackup/main_XX",\
                                "value": kwargs.get('nameservers')})
        data["network"].append({"id": "searchdomains_netbackup/main_XX",\
                                "value" : kwargs.get('searchdomains')})
        data["network"].append({"id": "etchosts_netbackup/main_XX",\
                                "value": kwargs.get('etchosts')})
        data["volume"].append({"id": "catalog_netbackup/main_XX",\
                                "value": kwargs.get('catalog')})

        data["envvars"].append({"id": "ENV_NB_REGKEY_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_regkey')})

        data["envvars"].append({"id": "ENV_NB_LICKEY_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_lickey')})
        data["envvars"].append({"id": "ENV_NB_SVC_UP_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_svc_up')})
        data["application.name"] = "NetBackupMaster"
        data["application.version"] = kwargs.get('application_version_xx')

        result = str(data)
        data = ast.literal_eval(result.replace('XX',\
                                kwargs.get('application_version_xx')))

        url = '{}/instances'.format(flex_env.api_url)
        print(data)
        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception('Failed master {}'.format(res.json()))
        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=123)
        if status:
           return res.json()['id']
        else:
            raise Exception("Failed to create Master ")

def media_sever(**kwargs):
        """
        :param : application_version_xx="8.2"
                hostname
                interface
                ipaddress
                tenant
                domainname
                nameservers
                searchdomains
                etchosts
                msdpdata
                cldcache
                advdisk
                env_nb_master
                env_nb_catype
                env_nb_stoken
                env_nb_cafprn
                env_nb_lickey
        :return: True
        """
        data = {}
        data = {"network":[], "envvars":[], "volume":[]}
        data["application.version"] = kwargs.get('application_version_xx')
        data["network"].append({"id": "hostname_netbackup/main_XX",\
                                "value": kwargs.get('hostname')})
        data["network"].append({"id": "interface_netbackup/main_XX",\
                                "value": kwargs.get('interface')})
        data["network"].append({"id": "ipaddress_netbackup/main_XX",\
                                "value": kwargs.get('ipaddress')})
        data["network"].append({"id": "tenant_netbackup/main_XX",\
                                "value": kwargs.get('tenant')})
        data["network"].append({"id": "domainname_netbackup/main_XX",\
                                "value": kwargs.get('domainname')})
        data["network"].append({"id": "nameservers_netbackup/main_XX",\
                                "value": kwargs.get('nameservers')})
        data["network"].append({"id": "searchdomains_netbackup/main_XX",\
                                "value": kwargs.get('searchdomains')})
        data["network"].append({"id": "etchosts_netbackup/main_XX",\
                                "value": kwargs.get('etchosts')})
        data["volume"].append({"id": "msdpdata_netbackup/main_XX",\
                            "value": kwargs.get('msdpdata')})
        data["volume"].append({"id": "cldcache_netbackup/main_XX",\
                            "value": kwargs.get('cldcache')})
        data["volume"].append({"id": "advdisk_netbackup/main_XX",\
                            "value": kwargs.get('advdisk')})
        data["envvars"].append({"id": "ENV_NB_MASTER_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_master')})

        if data["application.version"] == "8.2":
            data["envvars"].append({"id": "ENV_NB_CATYPE_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_catype')})
        elif data["application.version"] == "8.1.2":
            data["envvars"].append({"id": "ENV_NB_ATPSWD_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_atpswd')})
        else:
	    print("another version")
        data["envvars"].append({"id": "ENV_NB_CAFPRN_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_cafprn')})
        data["envvars"].append({"id": "ENV_NB_STOKEN_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_stoken')})
        data["envvars"].append({"id": "ENV_NB_LICKEY_netbackup/main_XX",\
                                "value": kwargs.get('env_nb_lickey')})
        data["application.name"] = "NetBackupMedia"
        result = str(data)
        data = ast.literal_eval(result.replace('XX',\
                                kwargs.get('application_version_xx')))
 
        url = '{}/instances'.format(flex_env.api_url)
        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception('Failed media {}'.format(res.json()))
        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=123)
        print(status)
        if status:
            return status
        else:
            raise Exception("Media Failed : ")

def create_bond_api(**kwargs):
        """
        :param : "bond_name"
                    "mode"
                    "node"
                    "interfaces"
        :return: json content
        """
        data = {}
        data = {"mode":"XXX", \
                "node":"XXX", "interfaces":[]}
        data["mode"] = kwargs.get("mode")
        data["node"] = kwargs.get("node")
        data["interfaces"] = kwargs.get("interfaces", [])

        url = '{}/network/bonds/bond'.format(flex_env.api_url)

        res = run_api(url=url, rq_type='post', data=data)
        if res.status_code != 200:
            raise Exception('Failed to create bond : {}'\
                .format(json.dumps(res.json())))

        task_id = res.json()['task-id']
        status = wait_for_task_to_complete(task_id, timeout=50)
        if status is True:
            return "DONE"
        else:
            raise Exception('Failed to create bond : {}'\
                .format(status['status']['status']))
