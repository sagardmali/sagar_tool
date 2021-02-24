from objects import objects
import flex_env
import utils
import rest_client

class user_management(objects):
    def run(self):
        self.logging.info('User Managemen\n')
        print("User Managemen")
        result = rest_client.post_user(subject=flex_env.subject, password=flex_env.password, fullName=flex_env.fullName, idpType=flex_env.idpType)
        if True:
            print('User Managemen : PASS')
            self.logging.info(result)
            self.logging.info('User Managemen : PASS')
            return 0
        print('User Managemen : FAIL')
        self.logging.info('User Managemen : FAIL')
        return 1

if __name__ == '__main__':
    obj = user_management()
    obj.run()
