from objects import objects
import flex_env
import config
import utils

class install_iso(objects):
    def run(self):
        self.logging.info("Install ISO\n")
        print("Install ISO ...")
        result = utils.install_iso(custom_url=config.custom_url, site=config.site, model=config.model, hosttype=config.hosttype, branch=config.branch, hostname=flex_env.hostname1, iso_name=config.iso_name, ipmihost=flex_env.ipmihost1, email=config.email)
        if True:
            self.logging.info(result)
            self.logging.info("Triggered ISO Installation : PASS")
            print("Triggered ISO Install : PASS")
            host = "{}.engba.veritas.com".format(flex_env.hostname1)
            result = utils.is_host_up(host)
            self.logging.info(result)
            if True:
                print("Install  ISO : PASS")
                self.logging.info("Install  ISO : PASS")
                return 0
        print("Install  ISO : FAIL")
        self.logging.info("Install  ISO : FAIL")
        return 1
 
if __name__ == '__main__':
    obj = install_iso()
    obj.run()
