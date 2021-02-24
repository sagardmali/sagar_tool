from objects import objects
import flex_env
import config
import utils

class multinode_setup_add_node(objects):
    def run(self):
        self.logging.info('Multinode Setup Add Node\n')
        print('Multinode Setup Add Node')
        add_node = "setup add-node with-response new_node={}.engba.veritas.com".format(config.vm_2)
        result = utils.flex_shell(add_node, answers=['yes', flex_env.password], host=config.ip1, username='hostadmin', password=flex_env.password, timeout=900)
        if "Operation completed successfully" in result:
                print("Multinode Setup Add Node : PASS")
                self.logging.info(result)
                self.logging.info('Multinode Setup Add Node : PASS')
                return 0
        print("Multinode Setup Add Node : FAIL")
        self.logging.info('Multinode Setup Add Node : FAIL')
        return 1

if __name__ == '__main__':
    obj = multinode_setup_add_node()
    obj.run()
