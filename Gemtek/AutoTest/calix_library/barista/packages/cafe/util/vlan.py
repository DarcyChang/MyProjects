__author__ = 'kelvin'

from cafe.core.utils import Param, ParamAttributeError

class Vlan(Param):
    def get_vlan_info(self, node, port):
        """
        Args:
            node (str): "node" key in the vlan data structure
            port (str): "port" :key in the vlan data structure

        Return:
            possible return
                dict{"vlan_type": "transport, "vlan_list": [<1-4095,>]}
                dict{"vlan_type": "unknown"}
        Raise:
            ParamAttributeError - when node or port is not found in the vlan data structure

        """
        if not node in self["vlan"]:
            raise ParamAttributeError("node not found (%s)" % node)
        if not port in self["vlan"][node]:
            raise ParamAttributeError("port not found (%s)" % port)

        return self["vlan"][node][port]

    def print_table(self):
        """
        Print the vlan parameter object to console in tabular format
        """
        print ("*** vlan print table ***")
        nodes = self["vlan"]
        for node, v in nodes.items():
            ports = nodes[node]
            for p in ports:
                print ("%s, %s, %s " % (node, p, nodes[node][p]))

    def _summarized(self,vlans):
        lst = sorted(vlans)
        ret = []
        a = b = lst[0]                           # a and b are range's bounds

        for el in lst[1:]:
            if el == b+1: b = el                 # range grows
            else:                                # range ended
                ret.append(a if a==b else (a,b)) # is a single or a range?
                a = b = el                       # let's start again with a single
        ret.append(a if a==b else (a,b))         # corner case for last single/range
        return ret

    def summarized(self, vlans):
        """
        Summarize a list of vlan numbers into cli vlan range string
        Args:
            vlans: list of vlans

        Returns
            cli vlan range string

        Example:
            >>> v = Vlan()
            >>> v.summarized([1,2,3, 6,7,8, 10])
            >>> # "1-3,6-8,10"
        """
        lst = self._summarized(vlans)
        ret = ""
        for _v in lst:
            if isinstance(_v, tuple):
                ret = ret + "%d-%d" % (_v[0], _v[1]) + ","
            if isinstance(_v, int):
                ret = ret + "%d" % (_v) + ","
        return ret[:-1]

    def expand(self, r):
        """
        Convert cli vlan range string to list of vlan number
        Args:
            vlans (str): list of vlans

        Returns
            cli vlan range string

        Example:
            >>> v = Vlan()
            >>> v.expand("1-3,6-8,10")
            >>> #[1,2,3, 6,7,8, 10]
        """
        lst = r.split(",")
        ret = []
        for _l in lst:
            if "-" in _l:
                _s0 = int(_l.split("-")[0])
                _s1 = int(_l.split("-")[1])
                ret.extend(range(_s0, _s1+1))
                continue
            _s = int(_l)
            ret.extend([_s])
        return sorted(ret)

# if __name__ == "__main__":
#
#     v = Vlan()
#     v.load("vlan.json")
#     v.print_table()
#     print (v.get_vlan_info("node1", "1/1/5"))
#     #print (v.get_vlan_info("node1", "1/2/5"))
#     print (v.summarized([2001,2002,2003, 1,2,3 ,6 ]))
#     print (v.expand("100-108,200-203,600,567"))




