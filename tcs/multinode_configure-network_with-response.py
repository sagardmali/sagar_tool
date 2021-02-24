from objects import objects
import flex_env
import config
import utils
import background

class multinode_setup_configure_network_with_response(objects):
    def run(self):
        self.logging.info('Setup Configure Network With Response\n')
        print("Setup Configure Network With Response")

        configure_network1 = "setup configure-network with-response host_ip={} host_hostname={}.{} host_gw={} subnet_mask={} dns_ip={} dns_domain={} search_domain={}".format(config.ip1, config.vm_1, flex_env.domain, config.gateway, config.netmask, config.nameserver, flex_env.domain, flex_env.domain)
        configure_network2 = "setup configure-network with-response host_ip={} host_hostname={}.{} host_gw={} subnet_mask={} dns_ip={} dns_domain={} search_domain={}".format(config.ip2, config.vm_2, flex_env.domain, config.gateway, config.netmask, config.nameserver, flex_env.domain, flex_env.domain)

        vm_1 = {'answers':'yes', 'host':config.ip1, 'username':'hostadmin', 'password':flex_env.password, 'timeout':300}
        vm_2 = {'answers':'yes', 'host':config.ip2, 'username':'hostadmin', 'password':flex_env.password, 'timeout':300}

        vms = []
        vm1 = "{}.engba.veritas.com".format(flex_env.hostname1)
        vm2 = "{}.engba.veritas.com".format(flex_env.hostname2)
        vms.append(vm1)
        vms.append(vm2)

        configure_setup_list = []
        flag = 0
        for vm in vms:
            if flag == 1:
                print("vm_1")
                configure_setup_list.append({'function': utils.flex_shell, 'args': [configure_network1], 'kwargs': vm_1})
            else:
                print("vm_2")
                configure_setup_list.append({'function': utils.flex_shell, 'args': [configure_network2], 'kwargs': vm_2})
            flag += 1

        print(configure_setup_list)
        result = background.run_in_background(configure_setup_list, wait_complete=True)
        print(result)
        for vm in result:
            if "Operation completed successfully" in vm.out:
                self.logging.info(vm.out)
                print("Set User Password : PASS")
                self.logging.info("Set User Password : PASS")
            else:
                print("Set User Password : FAIL")
                self.logging.info('Set User Password : FAIL')
                return 1

if __name__ == '__main__':
    obj = multinode_setup_configure_network_with_response()
    obj.run()
