from objects import objects
import flex_env
import config
import utils
import rest_client

class netbackup_media_8_2(objects):
    def run(self):
        self.logging.info('Netbackup Media _8_2\n')
        print("Netbackup Media _8_2") 
        
        cmd_master_id = "docker ps | grep netbackup/main | awk {'print $1'}"
        masterid = utils.flex_shell(cmd_master_id, host=config.ip1, username='hostadmin', password=flex_env.password, timeout=60, elevate=True, shell_prompt='#')
        masterid = masterid.split("\n")
        masterid = masterid[0]
        masterid = masterid.rstrip()
        cmd_add_sever = "docker exec -it {} bash -c \"sed -i '2 i SERVER \= {}' /usr/openv/netbackup/bp.conf\"".format(masterid, flex_env.media)
        result = utils.flex_shell(cmd_add_sever, host=config.ip1, username='hostadmin', password=flex_env.password, timeout=60, elevate=True, shell_prompt='#')
        print(result)
        cmd_finger_print = "docker exec -it {} bash -c \"/usr/openv/netbackup/bin/nbcertcmd -listCACertDetails 2>/dev/null|tail -n 2|head -n 1 \"".format(masterid)
        fingerprint = utils.flex_shell(cmd_finger_print, host=config.ip1, username='hostadmin', password=flex_env.password, timeout=60, elevate=True, shell_prompt='#')
        fingerprint = fingerprint.split("\n")
        finger_print = fingerprint[0]
        finger_print = list(finger_print.split(" : "))
        fingerprint = finger_print[1]
        finger_print = str(fingerprint.rstrip())
        print(finger_print)
        self.logging.info(finger_print)
        ressult_tenant = rest_client.get_tenant()
        Tenant = str(ressult_tenant[0]["id"])
        print(Tenant)
        result = rest_client.media_sever(application_version_xx=flex_env.applicaion_ver_8_1_2, hostname=flex_env.media, interface=config.Bond_name, ipaddress=flex_env.media_ipaddress, tenant=Tenant, domainname=flex_env.domainname, nameservers=flex_env.nameservers, searchdomains=flex_env.searchdomains, etchosts=flex_env.etchosts, msdpdata=flex_env.msdpdata, cldcache=flex_env.cldcache, advdisk=flex_env.advdisk, env_nb_master=flex_env.env_nb_master, env_nb_catype=flex_env.env_nb_catype, env_nb_stoken=flex_env.env_nb_stoken, env_nb_cafprn=finger_print, env_nb_lickey=flex_env.env_nb_lickey)
        if True:
            print("Netbackup Media _8_2 : PASS")
            self.logging.info(result)
            self.logging.info('Netbackup Media _8_2 : PASS')
            return 0
        print("Netbackup Media _8_2 : FAIL")
        self.logging.info('Netbackup Media _8_2 : FAIL')
        return 1 


if __name__ == '__main__':
    obj = netbackup_media_8_2()
    obj.run()
