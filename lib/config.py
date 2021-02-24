import os
import sys
import time

email = "sagar.mali@veritas.com"
LOG_DIR = "/tmp/flex/"

# Install iso
model = "5150"
site = "EAGAN"
hosttype = "VMs-IN-rsvdevvc01"
branch = "thunder_cloud-2.0.1"
###  Flag for default ISO installation  ###
#iso = "thunder_cloud-2.0.1-20210101161609.iso"
#iso_name = "http://10.84.176.122/{}/".format(iso)
#custom_url = "false"
###  Flag for Custom ISO installation  ###
iso = "thunder_cloud-2.1-999-1.iso"
iso_name = "http://10.85.16.93:8080/{}/".format(iso)
custom_url = "true"

vm_1 = "davidcl02vm131"
IP_VIP = "10.85.16.209"

master_ipaddress = "10.85.17.118"
master_node = "davidcl02vm131app1.engba.veritas.com"
media_ipaddress = "10.85.17.119"
media_node = "davidcl02vm131app2.engba.veritas.com"

name_servers = "172.16.8.12, 172.16.8.13"
nameserver =  "172.16.8.12"
netmask = "255.255.248.0"
gateway = "10.85.16.1"
subnet = "10.85.16.0/21"
Bond_name = "bond"
interface1 = "nic0"
interface2 = "nic2"

# Variables related to sending email
VIRTUAL_INSTALL =  True
#SMTP_SERVER = 'pnv86smtp01.pne.ven.veritas.com'
SMTP_SERVER = 'tus3hub-relay.community.veritas.com'
FROM_ADDR = 'sagar.mali@veritas.com'
SUBJECT_PREFIX = 'Flex Automation Test Case Report'
TO_ADDR = ['sagar.mali@veritas.com']

try:
    TO_ADDR = TO_ADDR + os.environ['EMAIL'].split(',')
except:
    pass
