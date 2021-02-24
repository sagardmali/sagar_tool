"""
   Common functions, utilities used in core 
   framework and in testcases
"""

import logging
import os
import sys
import platform
import time
import socket
import re
import json
import requests
import globals
import flex_env
import config
import httplib
import urllib
import commands
import background
import datetime
import traceback
import time,threading,os
from threading import Thread
from Sshoperation import Sshoperation

logger = logging.getLogger('utils')
logger.addHandler(logging.NullHandler())

def pinghost(host):
    """
    Ping host commands
    """
    logger.info(host)
    cmd ="ping -c 2 {}".format(host)
    status, output = commands.getstatusoutput(cmd)
    logger.info(output)
    if status!=0:
        logger.info(output)
    return 0

def is_host_up(host, wait=True):
    """
    Is host up commands
    """
    logger.info(host)
    if wait:
        rflag = False
        time.sleep(60)
        count = 0
        logger.info('Will do 10 attempts after each minute before reboot check terminate')
        while count < 10:
            count += 1
            pingok = pinghost(host)
            logger.info(pingok) 
            if pingok == 0:
                time.sleep(60)
                try:
                    print("Trying to ssh host ...")
                    result = flex_shell('cat /etc/vxos-release', host=flex_env.ip, username='hostadmin', password=flex_env.defaul_password, timeout=120)
                    logger.info('SSH Successfully machine')
                    rflag = True
                    break
                except:
                    pass
            time.sleep(60)
        return rflag
    else:
        logger.info('Reboot without waiting for machine to come up')
    return True

def set_user_password(cmd, **kwargs):
    """
    Run flex-shell commands
    """
    login_prompt = kwargs.get("login_prompt", " > ")
    host = kwargs.get("host", "ip")
    username = kwargs.get("username", "hostadmin")
    password = kwargs.get("password", "P@ssw0rd")
    timeout  = int(kwargs.get("timeout", 100))
    ssh_ = Sshoperation(timeout=100, prompt=login_prompt)
    ssh_.ssh_login(host, username, password)
    output = ""
    ssh_.ssh_write(cmd)
    print("CMD : {}").format(cmd)

    if type(kwargs["answers"]).__name__ == "list":
        answer_list = kwargs["answers"]
    else:
        answer_list = kwargs["answers"].split(',')
    prompt = r">>.*:"
    if kwargs.has_key("answer_prompt"):
        prompt = kwargs["answer_prompt"]
    prompt = r'.*password:.*'
    for answer in answer_list:
        output += ssh_.ssh_read_until_regexp(prompt)
        ssh_.ssh_write(answer)
    output += ssh_.ssh_read_until_prompt()

    output = output.encode('ascii', 'ignore')
    max_len = 32000
    os.environ["CLI_OUTPUT"] = output[-1 * max_len:]
    ssh_.ssh_logout()
    return output

def flex_shell(cmd, **kwargs):
    """
    Run flex-shell commands
    """

    shell_prompt = kwargs.get("shell_prompt", "flex-shell.*>")
    login_prompt = kwargs.get("login_prompt", " > ")
    host = kwargs.get("host", "ip")
    username = kwargs.get("username", "hostadmin")
    password = kwargs.get("password", "P@ssw0rdpassword")
    elevated = False
    if kwargs.has_key("elevate"):
        elevated = kwargs["elevate"]
    if kwargs.has_key("timeout"):
        ssh_ = Sshoperation(timeout=kwargs["timeout"], prompt=login_prompt)
    else:
        ssh_ = Sshoperation(prompt=login_prompt,timeout=300)

    if elevated:
        ssh_.ssh_login(host, username, password)
        ssh_.ssh_write("support elevate")
        ssh_.ssh_read_until_regexp(">>.*:")
        ssh_.ssh_write(password)
        ssh_.change_prompt("#")
        time.sleep(5)
    else:
        ssh_.ssh_login(host, username, password)

    output = ""
    ssh_.ssh_write(cmd)
    print("CMD : {}").format(cmd)

    if kwargs.has_key("answers"):
        if type(kwargs["answers"]).__name__ == "list":
            answer_list = kwargs["answers"]
        else:
            answer_list = kwargs["answers"].split(',')
        prompt = r">>.*:"
        if kwargs.has_key("answer_prompt"):
            prompt = kwargs["answer_prompt"]
        for answer in answer_list:
            logger.info(prompt)
            output += ssh_.ssh_read_until_regexp(prompt)
            ssh_.ssh_write(answer)
            logger.info(answer)
        output += ssh_.ssh_read_until_prompt()
    else:
        output += ssh_.ssh_read_until_prompt()

    output = output.encode('ascii', 'ignore')
    max_len = 32000
    os.environ["CLI_OUTPUT"] = output[-1 * max_len:]
    ssh_.ssh_logout()
    return output

def download_artifactory(artifactory="test", file_="VRTSflex-netbackup-8.2-0.x86_64.rpm"):
    """
    Download Artifactory
    """

    cmd = "wget {}{}/{} --no-verbose -P {}".format(flex_env.Artifactory_Url, artifactory, file_, flex_env.BUILD_PATH)
    logger.info(cmd)
    status, output = commands.getstatusoutput(cmd)
    if (status ==0):
        logger.info(status)
        logger.info(output)
        return 0
    logging.info(cmd)
    return 1

def download_iso(last=3):
    """
    Download iso
    """

    global BUILD
    master_url = "{}".format(flex_env.FLEX_ISO)
    cmd ="curl -s "+master_url+" | tail -n "+ str(last) +" | grep -i '1\.4\-'"
    logger.info(cmd)
    status, output = commands.getstatusoutput(cmd)
    logger.info(output)
    if (status ==0):
        out1=output.split(">")
        build= out1[1].strip("</a")
        BUILD=build
        url = "{}/{}".format(master_url,BUILD)
        cmd = "wget {}/thunder_cloud-{}.iso --no-verbose -P {}".format(url,BUILD, flex_env.BUILD_PATH)
        logger.info(cmd)
        status, output = commands.getstatusoutput(cmd)
        logging.info(cmd)
        if (status ==0):
            logger.info(status)
            return 0
        else:
            logger.info(status)
            return 1
    else:
        logger.info(status)
        return 1

def install_iso(**kwargs):
    """
    Install iso
    """

    data = {}
    data = {'use_http': 'xxxx', 'customized_scenario': {'robot_files_list': []}}
    data["use_http"] = kwargs.get("use_http", "http")
    data["custom_url"] = kwargs.get("custom_url")
    data["robot_download_url"] = kwargs.get("robot_download_url", "http://appliancemockupserver.engba.veritas.com/build/dev_main/robot.tar")
    data["role"] = kwargs.get("role", "None")
    data["ipmi_username"] = kwargs.get("ipmi_username", "sysadmin")
    data["ipmi_password"] = kwargs.get("ipmi_password", "P@ssw0rd")
    data["skip_install"] = kwargs.get("skip_install", "yes")
    data["site"] = kwargs.get("site")
    data["model"] = kwargs.get("model")
    data["hosttype"] = kwargs.get("hosttype")
    data["branch"] = kwargs.get("branch")
    data["hostname"] = kwargs.get("hostname")
    data["modelSaved"] = kwargs.get("modelSaved", "5340")
    data["iso_name"] = kwargs.get("iso_name")
    data["ipmihost"] = kwargs.get("ipmihost")
    data["email"] = kwargs.get("email")
    data["predefined_scenario"] = kwargs.get("predefined_scenario", "no_test")
    params = urllib.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("appvm06.engba.veritas.com:80")
    logger.info(data)
    conn.request("POST", "/acf/install_iso", params, headers)
    response = conn.getresponse()
    logger.info(response.status)
    logger.info(response.reason)
    if response.status != 200:
        raise Exception('Failed To Install ISO {}'.format(response.reason))
    data = response.read()
    logger.info(data)
    conn.close()
    return True

def send_mail(csvfile="file", m_from=config.FROM_ADDR, m_to=config.TO_ADDR):
    import commands
    import smtplib
    from os.path import basename
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    from os.path import basename
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    htmlfile = csvfile.strip('.cvs')+".html"
    print "CSV file is :", csvfile
    print "HTML  file is :", htmlfile

    make_html_from_csv(csvfile, htmlfile)
    flex_ver = 'Flex_{}'.format(config.iso)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "{}, Build : {}".format(config.SUBJECT_PREFIX, flex_ver)

    msg['From'] = m_from
    msg['To'] = ", ".join(m_to)

    cmd = 'cat < {}'.format(htmlfile)
    status, output = commands.getstatusoutput(cmd)
    html = """\
    <html>
    <head></head>
    <body>
    <p>Hi All,<br>
    <br>This is Automated Veritas Flex Test Execution Report.<br>
    {}
    <br>Regards,<br>
    Team Veritas Flex\n
    </p>
    </body>
    </html>
    """.format(output)

    part2 = MIMEText(html, 'html')
    msg.attach(part2)

    s = smtplib.SMTP(config.SMTP_SERVER)
    s.sendmail(m_from, m_to, msg.as_string())
    s.quit()

def make_html_from_csv(csv_file, html_file):
    result_file = html_file
    out_file = open(result_file, 'w')

    out_file.write("<h3>Build Information :-</h3>")
    table_header = '<table border="1">\
                    <tr>\
                    <th>Build No. </th>\
                    </tr>'
    out_file.write(table_header)
    line_num = 0
    table_row = '<tr>\
                     <td>{}</td>\
                </tr>'.format(config.iso)
    out_file.write(table_row)
    out_file.write('</table>')

    out_file.write("<h3>Automation Report :-</h3>")
    table_header = '<table border="1">\
                    <tr>\
                    <th>Sr.No.</th>\
                    <th>Testcase</th>\
                    <th>Status</th>\
                    <th>Start Time</th>\
                    <th>End Time</th>\
                    <th>Time Taken</th>\
                    <th>Logfile</th>\
                    </tr>'
    out_file.write(table_header)
    test_pass = 0
    test_fail = 0
    test_skip = 0
    test_total = 0
    line_num = 0
    #log_link = flex_env.LOG_SERVER + flex_env.LOG_DIR/"
    #TO DO
    log_link = config.LOG_DIR

    with open(csv_file, 'r') as filep:
        for line in filep:
            if line_num == 0:
                line_num = line_num + 1
                continue
            line = line.split(',')
            log_file = line[0]
            status = line[1].strip()
            if status == 'Pass':
                test_pass = test_pass+1
                bgcolor = "#008000"
            elif status == 'Skip':
                test_skip = test_skip+1
                bgcolor = "#FFC300"
            else:
                test_fail = test_fail+1
                bgcolor = "#FF0000"
            url = log_link+line[5]
            print "Log  file is :", url
            table_row = '<tr>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td bgcolor={}><center>{}</center></td>\
                        <td><center>{}</center></td>\
                        <td><center>{}</center></td>\
                        <td><center>{}</center></td>\
                        <td><a href={}>{}</a></td>\
                        </tr>'.format(line_num, line[0], bgcolor, status, line[2], line[3], line[4], url, log_file)
            out_file.write(table_row)
            line_num = line_num + 1
    out_file.write('</table>')

    out_file.write("<h3>Result Summary :-</h3>")
    table_header = '<table border="1">\
                    <tr>\
                    <th>Pass TCs</th>\
                    <th>Fail TCs</th>\
                    <th>Skip TCs</th>\
                    <th>Total TCs</th>\
                    <th>Overall Build Status</th>\
                    </tr>'
    out_file.write(table_header)
    test_total = test_pass+test_fail+test_skip
    overall_status = get_overall_status(
        test_pass, test_fail, test_skip, test_total)
    if overall_status == "RED":
        bgcolor = "#FF0000"
    elif overall_status == "GREEN":
        bgcolor = "#008000"
    else:
        bgcolor = "#FFC300"
    table_row = '<tr>\
                 <td bgcolor="#008000"><b><center>{}</center></b></td>\
                 <td bgcolor="#FF0000"><b><center>{}</center></b></td>\
                 <td bgcolor="#FFC300"><b><center>{}</center></b></td>\
                 <td><b><center>{}</center></b></td>\
                 <td bgcolor={}><b><center>{}</center></b></td>\
                 </tr>'.format(test_pass, test_fail, test_skip, test_total, bgcolor, overall_status)
    out_file.write(table_row)
    out_file.write('</table>')
    out_file.write("<h3>  Setup Configuration :- </h3>")
    out_file.write("<p><b>Machine Details</b> : {} <br>\
    UI Credential : {}<br>\
    <b>NOTE</b> : Please copy logs <br>\
    </p>".format(config.IP_VIP, "demo"))

def get_overall_status(test_pass, test_fail, test_skip, test_total):
    pass_per = test_pass*100/test_total
    fail_per = test_fail*100/test_total
    skip_per = test_skip*100/test_total
    if pass_per >= 90:
        return "GREEN"
    elif fail_per >= 10:
        return "RED"
    else:
        return "YELLOW"

#if __name__ == '__main__':
#    fexobj = send_mail(csvfile = '/tmp/flex/Report-10-Aug-2020-1597041599.csv')
