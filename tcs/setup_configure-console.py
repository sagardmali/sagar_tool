from objects import objects
import flex_env
import config
import utils

class setup_configure_console(objects):
    def run(self):
        self.logging.info('Setup Configure Console\n')
        print('Setup Configure Console')
        result = utils.flex_shell("system storage-reset", answers=['yes','DELETE DATA'], host=config.IP_VIP, username='hostadmin', password=flex_env.password, timeout=300)
        self.logging.info(result)
        if "Operation completed successfully" in result:
            result = utils.flex_shell("setup configure-console", answers='yes', host=config.IP_VIP, username='hostadmin', password=flex_env.password, timeout=700)
            if "Operation completed successfully" in result:
                print("Setup Configure Console : PASS")
                self.logging.info(result)
                self.logging.info('Setup Configure Console : PASS')
                return 0
        print("Setup Configure Console : FAIL")
        self.logging.info('Setup Configure Console : FAIL')
        return 1

if __name__ == '__main__':
    obj = setup_configure_console()
    obj.run()
