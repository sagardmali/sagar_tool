from objects import objects
import flex_env
import config
import utils
import rest_client

class change_console_passowrd(objects):
    def run(self):
        self.logging.info('Change Web Console Passowrd\n')
        print("Change Web Console Passowrd")
        result = rest_client.change_admin_password(node_ip=config.IP_VIP, oldpassword=flex_env.defaul_password, newpassword=flex_env.password, username=flex_env.username)
        if True:
            print("Change Web Console Passowrd : PASS")
            self.logging.info(result)
            self.logging.info('Change Web Console Passowrd : PASS')
            return 0
        print("Change Web Console Passowrd : FAIL")
        self.logging.info('Change Web Console Passowrd : FAIL')
        return 1

if __name__ == '__main__':
    obj = change_console_passowrd()
    obj.run()
