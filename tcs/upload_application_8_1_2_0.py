from objects import objects
import flex_env
import utils
import rest_client

class upload_application_8_1_2_0(objects):
    def run(self):
        self.logging.info('Upload Application 8_1_2_0\n')
        print('Upload Application 8_1_2_0')
        VRTSflex_netbackup = ("wget {} -P /mnt/data/infra/mgmt/upload/".format(flex_env.VRTSflex_netbackup_8_1_2_0_x86_64_rpm))
        print(VRTSflex_netbackup)
        result = utils.flex_shell(VRTSflex_netbackup, host=flex_env.ip, username='hostadmin', password=flex_env.password, timeout=600, elevate=True, shell_prompt='#')
        self.logging.info(result)
        result = rest_client.install_applications(flex_env.VRTSflex_netbackup_8_1_2_0, flex_env.application)
        if True:
            print("Upload Application 8_1_2_0 : PASS")
            self.logging.info(result)
            self.logging.info('Upload Application 8_1_2_0 : PASS')
            return 0
        print("Upload Application 8_1_2_0 : FAIL")
        self.logging.info('Upload Application 8_1_2_0 : FAIL')
        return 1

if __name__ == '__main__':
    obj = upload_application_8_1_2_0()
    obj.run()
