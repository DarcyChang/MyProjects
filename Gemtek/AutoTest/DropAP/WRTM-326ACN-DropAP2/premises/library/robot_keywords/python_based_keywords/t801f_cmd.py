import os,sys
import re
from caferobot.command.adapter import CliAdapter

class t801f_cmd(object):
    __meta_prompt="metacli>"
    __shell_prompt="#"

    def __init__(self):
        pass

    def meta_set(self,connection_name,*args):
        """Execute metcli set command to configure parameter on 801F

        args lists the 'parameter:value' pair to be set

        Example:
        | meta_set | 801f | psntpdate_debug_level=6 |
        | meta_set | 801f | cwmp_acs_url=http://10.245.250.98:8080/testmin | cwmp_acs_username=tr069 | cwmp_acs_request_password=tr069 |
        """
        variable_list=list(args)
        #metcli set
        for commands in variable_list:
            c_list = commands.split('=')
            meta_set_cmd = "set "+c_list[0]+" "+c_list[1]
            CliAdapter.cli(connection_name, meta_set_cmd, self.__meta_prompt, None, None)
        #metacli commit
        res=CliAdapter.cli(connection_name, "commit", self.__meta_prompt, None, None)
        #verify if commit successfully
        p = re.compile("commiting.+done")
        ret = p.search(res)
        if ret.group():
            return 1
        else:
            return 0

#   def meta_get(self,connection_name,*args):
#         variable_list=list(args)

    def t801f_get_version(self, connection_name):
        """Execute cat version cmd to get 801f software version
        return value is the version string
        """
        res = CliAdapter.cli(connection_name, "cat version", self.__shell_prompt, None, None)
        p = re.compile("version=(\d+\.\d+\.\d+\.\d+)")
        version = p.search(res)
        if version.group():
            return version.group(1)
        else:
            raise ValueError('Get software version failed')
            # return 0
