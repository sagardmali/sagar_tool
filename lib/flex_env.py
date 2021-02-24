import os
import sys
import time
import config

if config.model == '5150':
    hostname1 = "{}".format(config.vm_1)
    ipmihost1 = "{}con1".format(config.vm_1)
    node_name1 = "{}".format(config.vm_1)
elif config.model == '5340':
    node_name1 = "{}".format(config.vm_1)
    node_name2 = "{}".format(config.vm_2)
    hostname1 = "{}".format(config.vm_1)
    hostname2 = "{}".format(config.vm_2)
    ipmihost1 = "{}con1".format(config.vm_1)
    ipmihost2 = "{}con1".format(config.vm_2)
else:
    print('Unknown model')

# Mix
domain = "engba.veritas.com"
Netbackup_license = "KZNI-NB93-RUDE-CXCP-CN34-OG94-9G77-7GO9-PP3S-U"
applicaion_ver_8_2 = "8.2"
applicaion_ver_8_1_2 = "8.1.2"
applicaion_ver_8_3_0027 = "8.3.0027"

# Auth
username = "admin"
defaul_password = "P@ssw0rd"
password = "P@ssw0rdpassword"
ipmi_password = "Ver1tasP@55w0rd"

# Interface
interface1 = "{}".format(config.interface1)
interface_name1 = "{}".format(config.interface1)
ipv6 = "0"
subnet = "{}".format(config.subnet)
gateway = "{}".format(config.gateway)

# User
subject = "demouser"
password = "{}".format(password)
fullName = "demo"
idpType = "local"

# Tenant
name = "demotenants"
location = "demo"
emails = ["demo_tenants@veritas.com"]
domainName = ""
searchDomains = []
nameServers = []
etcHostsPath = ""
storage = {}
applications = []

# Master
application_version_xx = "{}".format(applicaion_ver_8_2)
application_version_xx = "{}".format(applicaion_ver_8_1_2)
application_version_xx = "{}".format(applicaion_ver_8_3_0027)
master = "{}".format(config.master_node)
interface1 = "{}".format(config.interface1)
master_ipaddress= "{}".format(config.master_ipaddress)
domainname = "{}".format(domain)
nameservers = "{}".format(config.name_servers)
searchdomains = "{}".format(domain)
etchosts = ""
catalog = "25GB"
env_nb_regkey = "{}"
env_nb_lickey = "{}".format(Netbackup_license)
env_nb_svc_up = "1"

# Media
application_version_xx = "{}".format(applicaion_ver_8_2)
application_version_xx = "{}".format(applicaion_ver_8_1_2)
application_version_xx = "{}".format(applicaion_ver_8_3_0027)
media = "{}".format(config.media_node)
interface1 = "{}".format(config.interface1)
media_ipaddress = "{}".format(config.media_ipaddress)
domainname = "{}".format(domain)
nameservers = "{}".format(config.name_servers)
searchdomains = "{}".format(domain) 
etchosts = ""
msdpdata = "2GB"
cldcache = "2GB"
advdisk = "2GB"
env_nb_master = "{}".format(config.master_node)
env_nb_atpswd = ""
env_nb_catype = "0"
env_nb_stoken = ""
env_nb_lickey = "{}".format(Netbackup_license)

# Rest
ip = '{}'.format(config.IP_VIP)
api = 'api/v1'
api_url = 'https://{}/{}'.format(ip, api)
auth_url = 'https://{}/authservice/api/v1/login'.format(ip)
etcd_url = 'https://{}/config/v3/kv'.format(ip)
policy_auth_url = 'https://{}/authservice/api/v1'.format(ip)

# RPM
VRTSflex_netbackup_8_1_2_0_x86_64_rpm = "http://artifactory-appliance.engba.veritas.com/artifactory/archive/GA/flex_netbackup/1.0-20180904131453/VRTSflex-netbackup-8.1.2-0.x86_64.rpm"
VRTSflex_netbackup_8_2_0_x86_64_rpm = "http://artifactory-appliance.engba.veritas.com/artifactory/test/VRTSflex-netbackup-8.2-0.x86_64.rpm"
VRTSflex_netbackup_8_3_0027_x86_64_rpm = "https://artifactory-appliance.engba.veritas.com/artifactory/build_deps/thunder/main/internal/NB_8.3.0.1_0027/rpm_for_appliance/VRTSflex-netbackup-8.3.0.1-0027.x86_64.rpm"

VRTSflex_netbackup_8_2_0 = "VRTSflex-netbackup-8.2-0.x86_64.rpm"
VRTSflex_netbackup_8_1_2_0 = "VRTSflex-netbackup-8.1.2-0.x86_64.rpm"
VRTSflex_netbackup_8_3_0027 = "VRTSflex-netbackup-8.3-0027.x86_64.rpm"
application = "application"

# Download path
PORT = 22
BUILD_PATH = "/tmp/flex"
Artifactory_Url = "http://artifactory-appliance.engba.veritas.com/artifactory/"
FLEX_ISO = "http://artifactory-appliance.engba.veritas.com/artifactory/release/thunder_cloud/main/"
