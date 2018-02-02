__author__ = 'kelvin'
import json
import sys
import os
import copy
#import warnings

#import networkx as nx
from cafe.core.utils import Param
from cafe.core.decorators import SingletonClass
from cafe.core.logger import CLogger
from cafe.core.signals import TOPOLOGY_ERROR

_logger = CLogger(__name__)
debug = _logger.debug
error = _logger.error

#nx.MultiGraph()

class TopologyError(Exception):
    # def __init__(self, message):
    #     # Call the base class constructor with the parameters it needs
    #     super(TopologyError, self).__init__(message)
    #     # Now for your custom code..
    #     if sys.exc_info()[0]:
    #         debug(sys.exc_info()[:2])
    #     error("- " + message, signal=TOPOLOGY_ERROR)
    def __init__(self, msg=""):
        self.msg = msg
        _logger.exception(msg, signal=TOPOLOGY_ERROR)

    def __str__(self):
        return self.msg


class _Topology(Param):
    #data = Param({"nodes": {}, "links": []})
    #graph = None
    def __init__(self, d={}):
        Param.__init__(self, d)
        self.graph = None
        self.used_nodes = []
        self.used_links = []

    def reset(self):
        self.clear()
        self.graph = None
        self.used_nodes = []
        self.used_links = []

    #overloading load method
    def load(self, json_file):
        filename = os.path.expanduser(json_file)
        filename = os.path.normpath(filename)

        if not os.path.isfile(filename):
            raise TopologyError("topology: json file not found - %s" % json_file)
        fp = open(filename,'r')
        s = fp.read()
        try:
            self.update(json.loads(s))
        except:
            raise TopologyError("fail to load json file(%s)" % json_file)

        finally:
            fp.close()

        #self.graph = nx.from_edgelist(self.get_edgelist(), create_using=nx.MultiGraph())
        self.create_graph()

    def reserve_node(self, node_name):
        """Reserve the node, locking it from being reserved by other logical topology methods (if the method respects
        reservations by calling this function first).

        Args:
            node_name (str): The name of the node to reserve

        Raises:
            TopologyError: if node 'node_name' does not exist
            TopologyError: if the node 'node_name' is already reserved
        """
        if node_name not in self._nodes():
            raise TopologyError("node '%s' does not exist" % node_name)

        if node_name in self.used_nodes:
            raise TopologyError("node '%s' is already reserved" % node_name)

        self.used_nodes.append(node_name)

    def free_node(self, node_name):
        """Un-reserves the previously reserved node, allowing it to be reserved again

        Args:
            node_name (str): The name of the node to un-reserve

        Raises:
            TopologyError: if node 'node_name' does not exist
            TopologyError: if node 'node_name' has not been yet reserved
        """
        if node_name not in self._nodes():
            raise TopologyError("node '%s' does not exist" % node_name)

        if node_name not in self.used_nodes:
            raise TopologyError("node '%s' has not been reserved" % node_name)

        self.used_nodes.remove(node_name)

    def is_node_reserved(self, node_name):
        """Find out if a node is reserved or not

        Args:
            node_name (str): The name of the node to check

        Raises:
            TopologyError: if node 'node_name' does not exist

        Returns:
            bool: true if the node is reserved, false if it isn't
        """
        if node_name not in self._nodes():
            raise TopologyError("node '%s' does not exist" % node_name)

        return node_name in self.used_nodes

    def reserve_link(self, link_dict):
        """Reserve the node, locking it from being reserved by other logical topology methods (if the method respects
        reservations by calling this function first).

        Args:
            link_dict (dict): The link dictionary to reserve

        Raises:
            TopologyError: if node 'node_name' does not exist
            TopologyError: if the node 'node_name' is already reserved
        """
        if link_dict not in self.links():
            raise TopologyError("node '%s' does not exist" % link_dict)

        if link_dict in self.used_links:
            raise TopologyError("node '%s' is already reserved" % link_dict)

        self.used_links.append(link_dict)

    def free_link(self, link_dict):
        """Un-reserves the previously reserved node, allowing it to be reserved again

        Args:
            link_dict (dict): The name of the node to un-reserve

        Raises:
            TopologyError: if node 'link_dict' does not exist
            TopologyError: if node 'link_dict' has not been yet reserved
        """
        if link_dict not in self.links():
            raise TopologyError("node '%s' does not exist" % link_dict)

        if link_dict not in self.used_links:
            raise TopologyError("node '%s' has not been reserved" % link_dict)

        self.used_links.remove(link_dict)

    def is_link_reserved(self, link_dict):
        """Find out if a node is reserved or not

        Args:
            link_dict (str): The name of the node to check

        Raises:
            TopologyError: if node 'link_dict' does not exist

        Returns:
            bool: true if the node is reserved, false if it isn't
        """
        if link_dict not in self.links():
            raise TopologyError("node '%s' does not exist" % link_dict)

        return link_dict in self.used_links

    def create_graph(self):
        #self.graph = nx.from_edgelist(self.get_edgelist(), create_using=nx.MultiGraph())
        pass

    #@classmethod
    def get_edgelist(self):
        links = self["links"]
        x = []
        for i in links:
            y = []
            #get nodes
            (node1, node2) = i["link"].keys()
            y.append(node1)
            y.append(node2)
            #get label
            if "label" not in i["attrs"]:
                i["attrs"]["label"] = "%s..%s" % (i["link"][node1], i["link"][node2])
            y.append(i["attrs"])
            x.append(y)
        return x

    #@classmethod
    def _nodes(self):
        """return all nodes"""
        return self["nodes"].keys()

    #@classmethod
    def node(self,node):
        """return node attributes"""
        if node in self["nodes"]:
            return self["nodes"][node]
        else:
            return

    def nodes_attrs(self, **attrs):
        if len(attrs) == 0:
            return self["nodes"].keys()

        ret = []
        for node in self['nodes'].items():
            print (node[1])
            match = set(node[1].items()) & set(attrs.items())
            print(match)
            if len(list(match)) is 0:
                pass
            else:
                ret.append(node[0])
        return ret

    #@classmethod
    def links(self):
        """return all links"""
        return self["links"]

    #@classmethod
    def neighbours(self, node):
        """return all neigbours connected to node"""
        if self.graph is not None:
            return self.graph.neighbors(node)
        else:
            return []

    #@classmethod
    def links_from_nodes(self, node1, node2):
        """return list of links between node1 and node2"""
        if self.graph is None:
            return []
        ret = []
        for link in self["links"]:
            if node1 in link["link"] and node2 in link["link"]:
                ret.append(link)
        return ret

    #@classmethod
    def neighbour_from_node_port(self, node, port):
        """
        get neighbor port from node+port
        :param node: source node
        :param port: source port
        :return: tuple of (<neighbor node>, <neighbor port>)
        """
        if self.graph is None:
            return (None, None)

        neighbors = self.neighbours(node)
        match = {node: port}
        for link in self["links"]:
            for (key, value) in set(link["link"].items()) & set(match.items()):
                for n in neighbors:
                    if n in link["link"]:
                       return (n, link["link"][n])

    #@classmethod
    def links_from_nodes_attrs(self, node1, node2, **attrs):
        """
        get links from node+port+attributes match
        :param node1: source node
        :param node2: destination node
        :param attrs: keyword of attribute/value pairs
        :return: list of  (<node1 port>, <node2 port>)
        """
        links = self.links_from_nodes(node1, node2)

        if len(attrs) is 0:
            return links

        ret = []
        for link in links:
            match = set(link["attrs"].items()) & set(attrs.items())
            #print(match)
            if len(list(match)) is 0:
                pass
            else:
                ret.append((link["link"][node1], link["link"][node2]))

        return ret

    #@classmethod
    def ports(self, node, *ignore, **attrs):
        links = self.links()
        ports = []
        for link in links:
            if node in link["link"]:
                if len(attrs) is 0:
                    ports.append(link["link"][node])
                else:
                    d = dict(set(link["attrs"].iteritems()).intersection(attrs.iteritems()))
                    #print(d)
                    if len(list(d)) is len(attrs):
                        ports.append(link["link"][node])

        return ports

    #@classmethod
    def save_dot_file(self, filename="topology.dot"):
        """
        save DOT (graph description language) file from the topology data.
        :param filename: dot file name
        :return: None
        """
        #nx.write_dot(self.graph, filename)
        pass

    def backup(self):
        """Returns a dictionary containing all topology and state values stored in the singleton object.
        Useful for rolling back changes to topology

        Returns:
            dict: dictionary containing a snapshot of the Topology singleton object's current state
        """
        return copy.deepcopy(dict(locals()['self']))

    def restore(self, backup_dict):
        """Restores the Topology singleton object to a previously saved state

        Args:
            backup_dict (dict): The snapshot of a previous Topology state (usually created by Topology.backup() method)
                to restore.

        Raises:
            AssertionError: if backup_dict is not of type dict
        """
        assert(type(backup_dict) is dict)

        for i in self.keys():
            del(self[i])

        for i in backup_dict:
            self[i] = copy.deepcopy(backup_dict[i])



@SingletonClass
class Topology(_Topology): pass

def get_topology():
    return Topology()
if __name__ == "__main__":
    pass

    # @SingletonClass
    # class Topology(_Topology):
    #     pass
    # g_topo = Topology()
    # g_topo.load("/home/kelvin/repo/calix/src/cafe/demo/topo/topo3.json")
    # print(g_topo)
    # #print(g_topo['nodes']['host'])
    # #print(g_topo.nodes.blm1)
    # print(g_topo.links())
    # print(g_topo._nodes())
    # print(g_topo.get_edgelist())
    # print("link %s" % g_topo.links_from_nodes("blm1", "blm2"))
    # print(g_topo.node("blm1"))
    # print(g_topo.neighbours("blm1"))
    # print(g_topo.neighbour_from_node_port("blm1", "g1"))
    # print(g_topo.neighbour_from_node_port("blm1", "g3"))
    # print(g_topo.links_from_nodes_attrs("blm1", "blm2"))
    # print(g_topo.links_from_nodes_attrs("blm1", "blm2", type="copper"))
    # print(g_topo.save_dot_file())
    # print("search 1g port of blm1 %s" % g_topo.ports("blm1", speed="1g"))
    # print("search 10g & fiber port of blm1 %s"  % g_topo.ports("blm1", type="fiber", speed="10g"))
    #
    #
    # print(g_topo.nodes_attrs(type="BLM1500"))
    # print(g_topo)