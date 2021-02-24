from objects import objects
import flex_env
import utils
import background
import config

class multinode_set_user_password(objects):
    def run(self):
        self.logging.info('Set User Password\n')
        print("Set User Password")

        vm_1 = {'answers':[flex_env.defaul_password, flex_env.password, flex_env.password], 'host':config.ip1, 'username':'hostadmin', 'password':flex_env.defaul_password, 'timeout':50}
        vm_2 = {'answers':[flex_env.defaul_password, flex_env.password, flex_env.password], 'host':config.ip2, 'username':'hostadmin', 'password':flex_env.defaul_password, 'timeout':50}

        vms = []
        vm1 = "{}.engba.veritas.com".format(flex_env.hostname1)
        vm2 = "{}.engba.veritas.com".format(flex_env.hostname2)
        vms.append(vm1)
        vms.append(vm2)

        set_user_password_list = []
        flag = 0
        for vm in vms:
            if flag == 1:
                print("vm_1")
                set_user_password_list.append({'function': utils.set_user_password, 'args': ["set user password"], 'kwargs': vm_1})
            else:
                print("vm_2")
                set_user_password_list.append({'function': utils.set_user_password, 'args': ["set user password"], 'kwargs': vm_2})
            flag += 1

        result = background.run_in_background(set_user_password_list, wait_complete=True)
        print(result)
        for vm in result:
            if "Operation completed successfully" in vm.out:
                self.logging.info(vm.out)
                print("Set User Password : PASS")
                self.logging.info("Set User Password : PASS")
            else:
                print("Set User Password : FAIL")
                self.logging.info('Set User Password : FAIL')
                return 1

if __name__ == '__main__':
    obj = multinode_set_user_password()
    obj.run()
