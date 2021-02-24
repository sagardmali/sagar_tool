from objects import objects
import flex_env
import utils

class set_user_password(objects):
    def run(self):
        self.logging.info('Set User Password\n')
        print("Set User Password")
        result = utils.flex_shell('cat /etc/vxos-release', host=flex_env.ip, username='hostadmin', password=flex_env.defaul_password, timeout=120)
        self.logging.info(result)
        result = utils.set_user_password("set user password", answers=[flex_env.defaul_password, flex_env.password, flex_env.password], host=flex_env.ip, username='hostadmin', password=flex_env.defaul_password, timeout=50)
        if "Operation completed successfully" in result:
            self.logging.info(result)
            print("Set User Password : PASS")
            self.logging.info('Set User Password : PASS')
            return 0
        print("Set User Password : FAIL")
        self.logging.info('Set User Password : FAIL')
        return 1

if __name__ == '__main__':
    obj = set_user_password()
    obj.run()
