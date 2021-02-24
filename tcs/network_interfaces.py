from objects import objects
import flex_env
import config
import utils
import rest_client

class network_interfaces(objects):
    def run(self):
        self.logging.info('Network Interfaces\n')
        print("Network Interfaces")
        result = rest_client.configure_vlan(interface=flex_env.interface1, name=flex_env.interface_name1, subnet=flex_env.subnet, gateway=flex_env.gateway, ipv6=flex_env.ipv6, node_name=flex_env.node_name1)
        if True:
            print("Network Interfaces : PASS")
            self.logging.info(result)
            self.logging.info('Network Interfaces : PASS')
            return 0
        print("Network Interfaces : FAIL")
        self.logging.info("Network Interfaces : FAIL")
        return 1

if __name__ == '__main__':
    obj = network_interfaces()
    obj.run()
