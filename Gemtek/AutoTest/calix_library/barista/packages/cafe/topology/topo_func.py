__author__ = 'kelvin'
from cafe.topology.topo import _Topology as Topology
from cafe.topology.topo import TopologyError
from cafe.core.utils import Param
from tinydb import TinyDB, where
import os

def get_exa_2node_simple(d, link_num=2, link_speed="1g", link_type="copper"):

    node_type = "exa"
    num = 2
    t = Topology(d)
    t.create_graph()
    _nodes = t.nodes_attrs(type=node_type)
    if len(_nodes) < num:
        raise TopologyError("fail to get nodes: available nodes less than %d" % num)
    # pick out the 1st 2 nodes has fulfill the requirements
    r = len(_nodes)
    match_found = False
    for i in range(r-1):
        node1 = _nodes[i]
        node2 = _nodes[i+1]
        _link = t.links_from_nodes_attrs(node1, node2, type=link_type, speed=link_speed)
        if len(_link) >= link_num:
            match_found = True
            break

    if match_found:
        links = _link[:link_num]
    else:
        raise TopologyError("fail to get nodes: available links less than %d" % link_num)

    ret = {}
    ret["nodes"] = []
    ret["nodes"].append(node1)
    ret["nodes"].append(node2)
    ret["links"] = []
    ret["links"].extend(links)

    return Param(ret)

def _delete_topo_db(db_file):
    try:
        os.remove(db_file)
    except OSError:
        pass

def _get_topo_db(d, db_file="topo_tmp.json"):
    d = Param(d)
    try:
        os.remove(db_file)
    except OSError:
        pass
    db = TinyDB(db_file)
    #db.insert({"desc": d.desc})
    for k, v in d.nodes.items():
        v.name = k
        db.insert({"node": v.dictionary()})

    for l in d.links:
        _l = Param(l['link'])
        _l.update(l['attrs'])
        #print _l
        db.insert({"link": _l.dictionary()})
    return db

def get_2nodes_exa_topo(topo, link_num=2, link_speed='1g', link_type='copper'):
    """
    find the logical 2 node exa topo from physical topo
    :param links:
    :param link_speed:
    :param link_type:
    :return: Param object "d"

    d.node1.node - dict of node1 information
    d.node2.node - dict of node2 information
    d.node1.ports - list of node1 ports
    d.node2.ports - list of node2 ports

    """

    #create tiny db and use its query features to find the logical topo

    tmp_file = 'topo_db.json'
    db = _get_topo_db(topo, tmp_file)

    node_query = where('node').has('type') == 'exa'
    nodes = db.search(node_query)

    d = Param()

    ln = None
    for i in range(len(nodes) -1) :

        d.node1 = Param()
        d.node2 = Param()
        d.node1.node = Param(nodes[i]['node'])
        d.node2.node = Param(nodes[i+1]['node'])

        name1 = nodes[i]['node']['name']
        name2 = nodes[i+1]['node']['name']
        link_query = where('link').has(name1) & where('link').has(name2) & \
                      (where('link').has('speed') == link_speed) & \
                      (where('link').has('type') ==  link_type)
        #print(link_query)
        ln = db.search(link_query)
        if ln >= link_num:
            ln = ln[:2]
            break
        else:
            ln = None

    #close tmp db and remove the db file
    db.close()
    _delete_topo_db(tmp_file)

    d.node1.ports = []
    d.node2.ports = []

    if ln:
        for l in ln:
            d.node1.ports.append(l['link'][d.node1.node.name])
            d.node2.ports.append(l['link'][d.node2.node.name])
    else:
        raise TopologyError("fail to get nodes: available links less than %d" % link_num)
        pass

    return d

def get_e7_node_topo(topo):
    """
    find the logical 2 node exa topo from physical topo
    :param links:
    :param link_speed:
    :param link_type:
    :return: Param object "d"

    d.node1.node - dict of node1 information
    d.node2.node - dict of node2 information
    d.node1.ports - list of node1 ports
    d.node2.ports - list of node2 ports

    """

    #create tiny db and use its query features to find the logical topo

    tmp_file = 'topo_db.json'
    db = _get_topo_db(topo, tmp_file)

    #node_query = where('node').all('type') == 'e7'
    #nodes = db.search(node_query)
    nodes = db.search(where('node').has('type') == 'e7')
    db.close()
    _delete_topo_db(tmp_file)

    d = Param(nodes[0]['node'])

    return d


def get_n_nodes(topo, num_nodes, **kwargs):
    """Find & Reserve N nodes matching the specified criteria from the physical topology, and return them as a logical
    topology.

    Args:
        topo (Topology): The topology tree to search
        num_nodes (int): N; the number of nodes to allocate.
        **kwargs (dict): A set of key-value pairs describing the criteria that needs to be matched. Any property key
            defined in the topology file can be used

    Raises:
        AssertionError: if num_nodes is not an int or None
        AssertionError: if topo is not an instance of Topology
        TopologyError: if the required number of nodes could not be allocated

    Returns:
        Param: a parameter set describing the logical topology
    """
    assert((type(num_nodes) is int) or (num_nodes is None))
    assert(isinstance(topo, Topology))

    tmp_file = 'topo_db.json'
    db = _get_topo_db(topo, tmp_file)

    # Retrieve matches from TinyDB
    query = where('node')

    for i in kwargs:
        query &= (where('node').has(i) == kwargs[i])

    nodes = db.search(query)

    db.close()
    _delete_topo_db(tmp_file)

    # Verify number of nodes found
    if len(nodes) < num_nodes:
        raise TopologyError("Could not allocate %s node(s). Found only %s node(s) that match the criteria." %
                            (num_nodes, len(nodes)))

    # Fill out the return dictionary
    ret = Param()

    to_find = num_nodes

    for i in nodes:
        node_name = i['node']['name']
        topo_name = "node%s" % (num_nodes - to_find + 1)

        if not topo.is_node_reserved(node_name):
            ret[topo_name] = Param({'node': i['node']})
            topo.reserve_node(node_name)
            to_find -= 1

        if to_find == 0:
            break

    # Verify that all nodes are accounted for
    if len(ret) < num_nodes:
        raise TopologyError("Could not allocate %s node(s). Of %s found node(s), %s were already reserved." %
                            (num_nodes, len(nodes), len(nodes) - len(ret)))

    return ret


def get_node(topo, **kwargs):
    """Find & Reserve a node matching the specified criteria from the physical topology, and return it as a logical
    topology.

    Args:
        topo (Topology): The topology tree to search
        **kwargs (dict): A set of key-value pairs describing the criteria that needs to be matched. Any property key
            defined in the topology file can be used

    Raises:
        AssertionError: if topo is not an instance of Topology
        TopologyError: if the node could not be allocated

    Returns:
        Param: a parameter set describing the logical topology
    """
    return get_n_nodes(topo, 1, **kwargs)


def get_all_nodes(topo, **kwargs):
    """Find & Reserve N nodes matching the specified criteria from the physical topology, and return them as a logical
    topology.

    Args:
        topo (Topology): The topology tree to search
        num_nodes (int): N; the number of nodes to allocate.
        **kwargs (dict): A set of key-value pairs describing the criteria that needs to be matched. Any property key
            defined in the topology file can be used

    Raises:
        AssertionError: if num_nodes is not an int or None
        AssertionError: if topo is not an instance of Topology
        TopologyError: if the required number of nodes could not be allocated

    Returns:
        Param: a parameter set describing the logical topology
    """
    assert(isinstance(topo, Topology))

    tmp_file = 'topo_db.json'
    db = _get_topo_db(topo, tmp_file)

    # Retrieve matches from TinyDB
    query = where('node')

    for i in kwargs:
        query &= (where('node').has(i) == kwargs[i])

    nodes = db.search(query)

    db.close()
    _delete_topo_db(tmp_file)

    # Verify number of nodes found
    if len(nodes) == 0:
        raise TopologyError("Could not find any nodes that match the criteria")

    # Fill out the return dictionary
    ret = Param()
    index = 1

    for i in nodes:
        node_name = i['node']['name']
        topo_name = "node%s" % index

        if not topo.is_node_reserved(node_name):
            ret[topo_name] = Param({'node': i['node']})
            index += 1
            topo.reserve_node(node_name)

    # Verify that some nodes were returned
    if len(ret) == 0:
        raise TopologyError("Could not find any free nodes that match the criteria")

    return ret

if __name__ == "__main__":
    pass
    g_topo = Topology()
    g_topo.load("~/repo/calix/src/demo/data/topo4.json")
    #g_topo.bp()

    d = get_2nodes_exa_topo(g_topo)
    d.bp()

    g_topo.reset()

    g_topo.load("~/repo/calix/src/demo/data/topo_e7.json")
    #g_topo.bp()

    d = get_e7_node_topo(g_topo)
    d.bp()
    #print(g_topo)
    #print(g_topo.links_from_nodes_attrs("exa1", "exa2"))
    #print(g_topo.links_from_nodes_attrs("exa1", "exa2", type="copper", speed="1g"))
    #print(g_topo.links_from_nodes(node1, node2))
    #d = get_exa_2node_simple(g_topo)

    #print(d.nodes)
    #print(d.links)
