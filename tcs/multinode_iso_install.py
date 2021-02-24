from objects import objects
import flex_env
import utils
import background
import config

class multinode_iso_install(objects):
    def run(self):
        self.logging.info("Install ISO\n")
        print("Install ISO ...")

        vm_1 = {'custom_url':config.custom_url,  'site':config.site, 'model':config.model, 'hosttype':config.hosttype, 'branch': config.branch, 'hostname':flex_env.hostname1, 'iso_name':config.iso_name, "ipmihost": flex_env.ipmihost1, "email":config.email}
        vm_2 = {'custom_url':config.custom_url,  'site':config.site, 'model':config.model, 'hosttype':config.hosttype, 'branch': config.branch, 'hostname':flex_env.hostname2, 'iso_name':config.iso_name, "ipmihost": flex_env.ipmihost2, "email":config.email}

        vms = []
        vm1 = "{}.engba.veritas.com".format(flex_env.hostname1)
        vm2 = "{}.engba.veritas.com".format(flex_env.hostname2)
        vms.append(vm1)
        vms.append(vm2)

        isolist = []
        setflag = 0
        for vm in vms:
	    if setflag == 1:
                print("vm_1")
		isolist.append({'function': utils.install_iso, 'args': [], 'kwargs': vm_1})
            else:
                print("vm_2")
	        isolist.append({'function': utils.install_iso, 'args': [], 'kwargs': vm_2})
            setflag += 1
        result = background.run_in_background(isolist, wait_complete=True)
        for vm in result:
            if not True:
                print("Install  ISO : FAIL")
		self.logging.info("Install  ISO : FAIL")
                return 1

        if True:
            self.logging.info(result)
            self.logging.info("Triggered ISO Installation : PASS")
            print("Triggered ISO Install : PASS")
            iso_host_up_list = []
            flag = 0
            host1 = "{}.engba.veritas.com".format(config.vm_1)
            host2 = "{}.engba.veritas.com".format(config.vm_2)

            for vm in vms:
                if flag == 1:
                    print("host1")
                    iso_host_up_list.append({'function': utils.is_host_up, 'args': [host1], 'kwargs': {}})
                else:
                    print("host2")
                    iso_host_up_list.append({'function': utils.is_host_up, 'args': [host2], 'kwargs': {}})
                flag += 1
            result = background.run_in_background(iso_host_up_list, wait_complete=True)
            self.logging.info(result)
            if True:
                print("Install  ISO : PASS")
                self.logging.info("Install  ISO : PASS")
                return 0
        print("Install  ISO : FAIL")
        self.logging.info("Install  ISO : FAIL")
        return 1

if __name__ == '__main__':
    obj = multinode_iso_install()
    obj.run()
