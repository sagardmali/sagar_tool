from objects import objects
import flex_env
import config
import utils

class setup_configure_network_with_response(objects):
    def run(self):
        self.logging.info('Setup Configure Network With Response\n')
        print("Setup Configure Network With Response")
        configure_network = "setup configure-network with-response host_ip={} host_hostname={}.{} host_gw={} subnet_mask={} dns_ip={} dns_domain={} search_domain={}".format(flex_env.ip, flex_env.hostname1, flex_env.domain, config.gateway, config.netmask, config.nameserver, flex_env.domain, flex_env.domain)
        result = utils.flex_shell(configure_network, answers='yes', host=flex_env.ip, username='hostadmin', password=flex_env.password, timeout=300)
        if "Operation completed successfully" in result:
            print("Setup Configure Network With Response : PASS")
            self.logging.info(result)
            self.logging.info('Setup Configure Network With Response : PASS')
            return 0
        print('Setup Configure Network With Response : FAIL')
        self.logging.info('Setup Configure Network With Response : FAIL')
        return 1

if __name__ == '__main__':
    obj = setup_configure_network_with_response()
    obj.run()
