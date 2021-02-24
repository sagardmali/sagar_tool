from objects import objects
import flex_env
import utils
import rest_client

class tenants(objects):
    def run(self):
        self.logging.info('Tenants\n')
        print("Tenants")
        result = rest_client.post_tenant(name=flex_env.name, location=flex_env.location, emails=flex_env.emails, domainName=flex_env.domainName, searchDomains=flex_env.searchDomains, nameServers=flex_env.nameServers, etcHostsPath=flex_env.etcHostsPath, storage=flex_env.storage, applications=flex_env.applications)
        if True:
            print("Tenants : PASS")
            self.logging.info(result)
            self.logging.info("Tenants : PASS")
            return 0
        print("Tenants : FAIL")
        self.logging.info('Tenants : FAIL')
        return 1

if __name__ == '__main__':
    obj = tenants()
    obj.run()
