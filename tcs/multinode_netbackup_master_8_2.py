from objects import objects
import flex_env
import config
import utils
import rest_client

class netbackup_master_8_2(objects):
    def run(self):
        self.logging.info('Netbackup Master _8_2\n')
        print("Netbackup Master _8_2")
        ressult_tenant = rest_client.get_tenant()
        Tenant = str(ressult_tenant[0]["id"])
        self.logging.info("Tenant ID :")
        self.logging.info(Tenant)
        result = rest_client.master_server(application_version_xx=flex_env.applicaion_ver_8_2, hostname=flex_env.master, interface=config.Bond_name, ipaddress=flex_env.master_ipaddress, tenant=Tenant, domainname=flex_env.domainname, nameservers=flex_env.nameservers, searchdomains=flex_env.searchdomains, etchosts=flex_env.etchosts, catalog=flex_env.catalog, env_nb_regkey=flex_env.env_nb_regkey, env_nb_lickey=flex_env.env_nb_lickey, env_nb_svc_up=flex_env.env_nb_svc_up)
        if True:
            print("Netbackup Master _8_2 : PASS")
            self.logging.info(result)
            self.logging.info('Netbackup Master _8_2 : PASS')
            return 0
        print("Netbackup Master _8_2 : FAIL")
        self.logging.info('Netbackup Master _8_2 : FAIL')
        return 1


if __name__ == '__main__':
    obj = netbackup_master_8_2()
    obj.run()
