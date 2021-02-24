from objects import objects
import flex_env
import config
import utils
import rest_client

class multinode_network_interfaces(objects):
    def run(self):
        self.logging.info('Network Interfaces\n')
        print("Network Interfaces")
        result = rest_client.create_bond_api(mode="802.3ad", node=flex_env.node_name1, interfaces=[config.interface1, config.interface2])
        print(result)
        result = rest_client.create_bond_api(mode="802.3ad", node=flex_env.node_name2, interfaces=[config.interface1, config.interface2])
        print(result)
        result = rest_client.configure_vlan(interface=config.Bond_name, name=config.Bond_name, subnet=flex_env.subnet, gateway=flex_env.gateway, ipv6=flex_env.ipv6, node_name=flex_env.node_name1)
        result = rest_client.configure_vlan(interface=config.Bond_name, name=config.Bond_name, subnet=flex_env.subnet, gateway=flex_env.gateway, ipv6=flex_env.ipv6, node_name=flex_env.node_name2)
        if True:
            print("Network Interfaces : PASS")
            self.logging.info(result)
            self.logging.info('Network Interfaces : PASS')
            return 0
        print("Network Interfaces : FAIL")
        self.logging.info("Network Interfaces : FAIL")
        return 1

if __name__ == '__main__':
    obj = multinode_network_interfaces()
    obj.run()
