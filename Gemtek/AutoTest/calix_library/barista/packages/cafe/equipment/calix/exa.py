import re
import time
from cafe.core.logger import CLogger as Logger
from cafe.topology.topo import get_topology
from cafe.core.signals import EXA_SESSION_ERROR
from cafe.resp.response_map import ResponseMap
from cafe.core.db import teststep

logger = Logger(__name__)
debug = logger.debug
error = logger.error
debug("importing module %s" % __name__)


def get_exa_class(name, session, session_type="ssh", release=None):
    return CalixExaBase(name, session, session_type, release)

class CalixExaBase(object):
    """
    base class of EXA interfaces
    """
    LOGIN_PROMPT = "login:\s+$"
    PASSWORD_PROMPT = "assword:\s+$"
    EXA_PROMPT = "\S+#\s*$"
    BASH_PROMPT = "\S+@\S+:\S+#\s+$"
    CONFIG_PROMPT = "\S+\(config\)#\s+$"

    def __init__(self, name, session, session_type="ssh", release=None):
        """
        """
        self.name = name
        self.session = session
        self.session.prompt.extend([self.LOGIN_PROMPT, self.PASSWORD_PROMPT, self.EXA_PROMPT,
                                    self.BASH_PROMPT, self.CONFIG_PROMPT])
        self.session_type = session_type
        self.release = release

    def command(self, cmd="", timeout=30):
        if self.session_type == "ssh":
            r = self.session.expect_prompt(timeout=0)

        self.session.write(cmd)
        # return tuple (prompt index, <prompt re match object>, text)
        r = self.session.expect_prompt(timeout=timeout)

        if "error:" in r[2]:
            status = False
        else:
            status = True
        if r[0] < 0:
            return {"status": status, "prompt": None, "response": r[2]}
        else:
            return {"status": status, "prompt": r[1].group(), "response": r[2]}

    def __prompt_matches(self, prompt, regex):
        ret = True

        if (prompt is None) or (re.match(regex, prompt) is None):
            ret = False

        return ret

    def login(self):
        if self.session_type != "telnet":
            self.session.login()

        prompt = self.command(cmd="\x03")['prompt']
        self.cli(prompt)

    def cli(self, prompt):
        # print("[[[[[%s|%s]]]]]" % (prompt, self.EXA_PROMPT))
        if self.__prompt_matches(prompt, self.CONFIG_PROMPT):
            self.command("top")
            next_prompt = self.command(cmd="exit")['prompt']
        elif self.__prompt_matches(prompt, self.LOGIN_PROMPT):
            next_prompt = self.command(cmd=self.session.user)['prompt']
        elif self.__prompt_matches(prompt, self.PASSWORD_PROMPT):
            next_prompt = self.command(cmd=self.session.password)['prompt']
        elif self.__prompt_matches(prompt, self.BASH_PROMPT):
            next_prompt = self.command(cmd="cli")['prompt']
        elif self.__prompt_matches(prompt, self.EXA_PROMPT):
            return
        else:
            error(" - attempt to get to CLI level resulted in an undefined state. Prompt: %s" % prompt)
            return

        self.cli(next_prompt)

    def in_known_state(self, prompt):
        known_states = [self.LOGIN_PROMPT, self.BASH_PROMPT, self.CONFIG_PROMPT, self.EXA_PROMPT, self.PASSWORD_PROMPT]

        match = False

        for i in known_states:
            if self.__prompt_matches(prompt, i):
                match = True
                break

        return match

    def reload(self):
        prompt = self.command(cmd="\x03")['prompt']
        self.cli(prompt)
        print(self.command("reload"))
        print(self.command("y"))

        reboot_successful = True

        if self.session_type == "telnet":
            num_retries = 15
            wait_time = 30

            while (not self.in_known_state(self.command(timeout=wait_time)['prompt'])) and (num_retries > 0):
                time.sleep(wait_time)
                num_retries -= 1

            if num_retries <= 0:
                reboot_successful = False
        elif self.session_type == "ssh":
            num_retries = 20
            wait_time = 20

            time.sleep(5)

            disconnected = True

            initial_disconnect = False

            while disconnected and (num_retries >= 0):
                try:
                    self.login()
                    disconnected = False
                except Exception as e:
                    #print(e.message)
                    initial_disconnect = True

                time.sleep(wait_time)
                # print("retries left: %s" % num_retries)
                num_retries -= 1

            reboot_successful = not disconnected

        if reboot_successful:
            c = self.command(cmd="\x03")
            #print(c)
            prompt = c['prompt']
            self.cli(prompt)
            debug(" - reloaded successfully")
        else:
            error(" - failed to reload device!")

    def reconnect(self):
        reboot_successful = True

        if self.session_type == "telnet":
            num_retries = 15
            wait_time = 30

            while (not self.in_known_state(self.command(timeout=wait_time)['prompt'])) and (num_retries > 0):
                time.sleep(wait_time)
                num_retries -= 1

            if num_retries <= 0:
                reboot_successful = False
        elif self.session_type == "ssh":
            num_retries = 20
            wait_time = 20

            time.sleep(5)

            disconnected = True

            initial_disconnect = False

            while disconnected and (num_retries >= 0):
                try:
                    self.login()
                    disconnected = False
                except Exception as e:
                    #print(e.message)
                    initial_disconnect = True

                time.sleep(wait_time)
                # print("retries left: %s" % num_retries)
                num_retries -= 1

            reboot_successful = not disconnected

        if reboot_successful:
            c = self.command(cmd="\x03")
            #print(c)
            prompt = c['prompt']
            self.cli(prompt)
            debug(" - reloaded successfully")
        else:
            error(" - failed to reload device!")

    @teststep("get_interface_craft")
    def get_interface_craft(self, intf):
        # E5-520# show interface craft 1 | nomore
        # interface craft 1
        #  status
        #   name            "craft 1"
        #   admin-state     enable
        #   oper-state      unknown
        #   mac-addr        00:02:5D:BA:8D:B7
        #   net-config-type static
        #   ip-address      10.243.19.213
        #   ip-mask         255.255.252.0
        #   ip-gateway      10.243.16.1
        #   craft-cntrs
        #    rx-pkts   586110
        #    rx-octets 170323600
        #    tx-pkts   71836
        #    tx-octets 14459880
        #   dhcp-server     disable
        #(0, <object>, text)
        r = self.command(cmd="show interface craft %s | nomore" % str(intf))
        resp = r["response"]
        m = ResponseMap(resp)
        d = m.parse_key_value_pairs(start_line=1)
        return d










