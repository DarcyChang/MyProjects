__author__ = 'akhanov'

import networkx
from itertools import ifilter, combinations
from cafe.core.utils import Param
from cafe.topology.topo import _Topology
from cafe.topology.topo import TopologyError


class _CriteriaResultCache(object):
    """ Class that is used to search for & cache nodes and edges based on attributes
    """
    def __init__(self, graph):
        """ Initializes the _CriteriaResultCache object

        Args:
            graph (networkx.Graph): The graph which will be used for node & edge search
        """
        self.node_criteria = {}
        self.edge_criteria = {}
        self.graph = graph

    def __add_node_criteria(self, criteria_name):
        if criteria_name not in self.node_criteria:
            self.node_criteria[criteria_name] = networkx.get_node_attributes(self.graph, criteria_name)

    def get_node_criteria_results(self, criteria_name):
        """ Fetch the list of nodes which have the attribute 'criteria_name'

        Args:
            criteria_name (str): The attribute to search for

        Returns:
            list: List of nodes which have the specified attribute
        """
        self.__add_node_criteria(criteria_name)

        return self.node_criteria[criteria_name]

    def match_node_criteria(self, query_dictionary):
        """ Fetch a set of nodes which match the specified dictionary of criteria

        Args:
            query_dictionary (dict): A dictionary of Attribute->AttributeValue pairs that must be matched

        Returns:
            set: A set of nodes in the graph which match ALL of the criteria specified in the dictionary

        Raises:
            AssertionError: if query_dictionary is not an instance of dict
        """
        assert(isinstance(query_dictionary, dict))

        matches = set()

        if len(query_dictionary.keys()) == 0:
            # matches = set(self.graph.nodes)
            matches = set(networkx.nodes(self.graph))
        else:
            for criteria in query_dictionary.keys():
                self.__add_node_criteria(criteria)

                nodelist = self.get_node_criteria_results(criteria)
                match = set(ifilter(lambda x: nodelist[x] == query_dictionary[criteria], nodelist.keys()))

                if len(matches) == 0:
                    matches |= match
                else:
                    matches &= match

        return matches

    def __add_edge_criteria(self, criteria_name):
        if criteria_name not in self.edge_criteria:
            self.edge_criteria[criteria_name] = networkx.get_edge_attributes(self.graph, criteria_name)

    def get_edge_criteria_results(self, criteria_name):
        """ Fetch the list of edges which have the attribute 'criteria_name'

        Args:
            criteria_name (str): The attribute to search for

        Returns:
            list: list of edges which have the specified attribute
        """
        self.__add_edge_criteria(criteria_name)

        return self.edge_criteria[criteria_name]

    def get_edges(self, node1_name, node2_name):
        one_to_one = True

        if isinstance(node1_name, str) or isinstance(node1_name, unicode):
            n1_set = set([node1_name])
        elif isinstance(node1_name, tuple):
            n1_set = node1_name
            one_to_one = False

        if isinstance(node2_name, str) or isinstance(node2_name, unicode):
            n2_set = set([node2_name])
        elif isinstance(node2_name, tuple):
            n2_set = node2_name
            one_to_one = False

        ret = list()

        for n1 in n1_set:
            for n2 in n2_set:
                ret.append(self.graph[n1][n2].keys())

        # ret = self.graph[node1_name][node2_name].keys()
        return ret

    def get_neighbor_nodes(self, node_name):
        if isinstance(node_name, str) or isinstance(node_name, unicode):
            nodes = [node_name]
        elif isinstance(node_name, tuple) or isinstance(node_name, list):
            nodes = node_name

        neighbor_list = []
        for i in nodes:
            neighbor_list.append(set(self.graph[i].keys()))

        neighbors = reduce(lambda x, y: x & y, neighbor_list)

        return neighbors




    def match_edge_criteria(self, query_dictionary, node1_name, node2_name):
        """ Fetch a set of edges between two nodes which match the specified dictionary of criteria

        Args:
            query_dictionary (dict): A dictionary of Attribute->AttributeValue pairs that must be matched
            node1_name (str): The identifier of the first node attached to the edges
            node2_name (str): The identifier of the second node attached to the edges

        Returns:
            set: a set of edges between the specified nodes in the graph which match ALL of the criteria in the
                specified dictionary.

        Raises:
            AssertionError: if query_dictionary is not an instance of dict
        """
        assert(isinstance(query_dictionary, dict))
        neighbor_links = sort_edge_set(set(map(lambda x: (node1_name, node2_name, x),
                                               # self.get_edges(node1_name, node2_name))))
                                               self.graph[node1_name][node2_name].keys())))

        matches = set()

        if len(query_dictionary.keys()) == 0:
            # matches = set(networkx.edges(self.graph))
            matches = set(self.graph.edges(None, False, True))
        else:
            for criteria in query_dictionary.keys():
                self.__add_edge_criteria(criteria)

                nodelist = self.get_edge_criteria_results(criteria)
                match = set(ifilter(lambda x: nodelist[x] == query_dictionary[criteria], nodelist.keys()))

                if len(matches) == 0:
                    matches |= match
                else:
                    matches &= match

        ret = set()

        for m in matches:
            ret |= sort_edge_set([tuple(m)])

        return neighbor_links & ret


class Query(Param):
    """ Base class for storing & performing queries on a graph
    """
    def __init__(self, **kwargs):
        """ Query constructor

        Args:
            kwargs: named arguments which describe the filter. Can be any keyword defined in the topology.
        """
        super(Query, self).__init__(self)

        for i in kwargs.keys():
            self.__setitem__(i, kwargs[i])

    def __str__(self):
        val = []

        for i in self.keys():
            val.append("%s: %s" % (i, self[i]))

        return "%s(%s)" % (self.__class__.__name__, ", ".join(val))

    def matches(self, criteria_cache):
        """ Return a set of objects matching this query from the specified criteria cache

        Args:
            criteria_cache (_CriteriaResultCache): the criteria cache object to interface with
        """
        pass

    def add(self, key, value):
        """ Add a set of criteria to the query. This method can be used to dynamically add criteria, or to specify
        criteria which conflicts with Python's argument naming restrictions

        Args:
            key (str): the criteria name
            value (str): the value of the criteria

        Returns:
            Query: the method returns itself, so you can easily chain

        Example:
            ::

                query = Query().add("key", "value").add("another_key", "value")

        """
        self[key] = value

        return self

    def __eq__(self, other):
        if other is self:
            return True

        return False


class NodeQuery(Query):
    """ A Query class that queries nodes
    """
    def __init__(self, node_name, **kwargs):
        """ NodeQuery constructor

        Args:
            node_name (str): The name to give the found node in the final logical topology
            kwargs: named arguments which describe the filter. Can be any keyword defined in the topology.
        """
        super(NodeQuery, self).__init__(**kwargs)
        object.__setattr__(self, '__node_name', node_name)

    def set_node_name(self, node_name):
        """ Sets the node name. This name will be given to the found node in the final logical topology.

        Args:
            node_name (str): The name to give the found node in the final logical topology
        """
        object.__setattr__(self, '__node_name', node_name)

    def get_node_name(self):
        """ Returns the node name. This name is given to the found node in the final logical topology.

        Returns:
            str: the node name
        """
        return object.__getattribute__(self, '__node_name')

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.get_node_name())

    def matches(self, criteria_cache, pool=None):
        """ Fetch a set of nodes from criteria_cache's graph which matches the query's criteria

        Args:
            criteria_cache (_CriteriaResultCache): The CriteriaResultCache object to search

        Returns:
            set: set of nodes from criteria cache's graph which matches the query's criteria

        Raises:
            AssertionError: if criteria_cache is not an instance of _CriteriaResultCache
        """
        assert(isinstance(criteria_cache, _CriteriaResultCache))

        ret = criteria_cache.match_node_criteria(self)

        if (pool is not None) and isinstance(pool, set):
            ret = ret & pool

        return ret


class MultiNodeQuery(NodeQuery):
    def __init__(self, node_name, num_nodes, **kwargs):
        super(MultiNodeQuery, self).__init__(node_name, **kwargs)
        object.__setattr__(self, '__num_nodes', num_nodes)

    def set_num_nodes(self, num_nodes):
        object.__setattr__(self, '__num_nodes', num_nodes)

    def get_num_nodes(self):
        return object.__getattribute__(self, '__num_nodes')

    def matches(self, criteria_cache, pool=None):
        total_nodes = super(MultiNodeQuery, self).matches(criteria_cache, pool)

        ret = set()

        if self.get_num_nodes() is None:
                combo_range = range(1, len(total_nodes)+1)
        else:
            combo_range = [self.get_num_nodes()]

        for r in combo_range:
            all_combos = combinations(total_nodes, r)

            for i in all_combos:
                ret.add(tuple(sorted(i)))

        return ret


class LinkQuery(Query):
    """ A Query class that queries links
    """
    def __init__(self, link_name, **kwargs):
        """ LinkQuery constructor

        Args:
            link_name (str): The name to give the found link in the final logical topology
            kwargs: named arguments which describe the filter. Can be any keyword defined in the topology
        """
        super(LinkQuery, self).__init__(**kwargs)
        self.set_link_name(link_name)

    def set_link_name(self, link_name):
        """ Sets the link name. This name will be given to the found link in the final logical topology.

        Args:
            link_name (str): The name to give the found node in the final logical topology
        """
        object.__setattr__(self, '__link_name', link_name)

    def get_link_name(self):
        """ Returns the link name. This name is given to the found link in the final logical topology.

        Returns:
            str: the link name
        """
        return object.__getattribute__(self, '__link_name')

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.get_link_name())

    def matches(self, criteria_cache, node_a_name, node_b_name):
        """ Fetch a set of edges that are between the two specified nodes from criteria_cache's graph which matches
        the query's criteria

        Args:
            criteria_cache (_CriteriaResultCache): The CriteriaResultCache object to search
            node_a_name (str): The first node
            node_b_name (str): The second node

        Returns:
            set: set of nodes from criteria cache's graph which matches the query's criteria and are between the two
                specified nodes

        Raises:
            AssertionError: if criteria_cache is not an instance of _CriteriaResultCache
        """
        assert(isinstance(criteria_cache, _CriteriaResultCache))

        copy = self.copy()

        if 'link.node_a' in copy:
            val = copy['link.node_a']
            del copy['link.node_a']
            copy['link.%s' % node_a_name] = val

        if 'link.node_b' in copy:
            val = copy['link.node_b']
            del copy['link.node_b']
            copy['link.%s' % node_b_name] = val

        node_a_set = node_a_name
        node_b_set = node_b_name

        if isinstance(node_a_set, str) or isinstance(node_a_set, unicode):
            node_a_set = [node_a_set]

        if isinstance(node_b_set, str) or isinstance(node_b_set, unicode):
            node_b_set = [node_b_set]

        ret = []

        for na in node_a_set:
            for nb in node_b_set:
                matching_edges = criteria_cache.match_edge_criteria(copy, na, nb)
                ret.append(matching_edges)
        # ret = map(lambda x: [x], matching_edges)

        return ret

    @staticmethod
    def get_edge_data(graph, edge_list):
        """ Static method for retrieving edge data from a graph based on a edge list

        Args:
            graph (networkx.Graph): The graph to search
            edge_list (list): The list of edges to retrieve data for

        Returns:
            dict: The dictionary of the first edge in the edge_list
        """
        edge = edge_list

        edge_data = graph.get_edge_data(*edge)

        return unflatten_dictionary(edge_data)


class MultiLinkQuery(LinkQuery):
    """ A query that matches multiple links
    """
    def __init__(self, link_name, num_links, **kwargs):
        """ MultiLinkQuery constructor

        Args:
            link_name (str): The name to give the found link in the final logical topology
            num_links (int): The number of links to request. If set to None, requests maximum available links
            kwargs: named arguments which describe the filter. Can be any keyword defined in the topology
        """
        super(MultiLinkQuery, self).__init__(link_name, **kwargs)
        self.set_num_links(num_links)

    def set_num_links(self, num_links):
        """ Sets the number of links to request

        Args:
            link_name (int): The number of links to request. If None, maximum available links will be taken
        """
        object.__setattr__(self, '__num_links', num_links)

    def get_num_links(self):
        """ Fetch the number of links to request

        Returns:
            int: number of links to request
        """
        return object.__getattribute__(self, '__num_links')

    def matches(self, criteria_cache, node_a_name, node_b_name):
        """ Fetch a set of edges that are between the two specified nodes from criteria_cache's graph which matches
        the query's criteria

        Args:
            criteria_cache (_CriteriaResultCache): The CriteriaResultCache object to search
            node_a_name (str): The first node
            node_b_name (str): The second node

        Returns:
            set: set of nodes from criteria cache's graph which matches the query's criteria and are between the two
                specified nodes

        Raises:
            AssertionError: if criteria_cache is not an instance of _CriteriaResultCache
        """
        #all_links = map(lambda x: x[0], super(MultiLinkQuery, self).matches(criteria_cache, node_a_name, node_b_name))
        all_links = super(MultiLinkQuery, self).matches(criteria_cache, node_a_name, node_b_name)[0]
        ret = []

        if self.get_num_links() is None:
            combo_range = range(1, len(all_links)+1)
        else:
            combo_range = [self.get_num_links()]

        for r in combo_range:
            all_combos = combinations(all_links, r)

            for i in all_combos:
                ret.append(list(i))

        return [ret]

    @staticmethod
    def get_edge_data(graph, edge_list):
        """ Static method for retrieving edge data from a graph based on a edge list

        Args:
            graph (networkx.Graph): The graph to search
            edge_list (list): The list of edges to retrieve data for

        Returns:
            dict: The list of dictionaries of the edges in the edge_list
        """
        ret = []

        for i in edge_list:
            # ret.append(super(MultiLinkQuery, MultiLinkQuery).get_edge_data(graph, [i]))
            ret.append(super(MultiLinkQuery, MultiLinkQuery).get_edge_data(graph, i))

        return ret


class QueryException(BaseException):
    """ Exception class for query-related issues
    """
    def __init__(self, message):
        """ QueryException constructor

        Args:
            message (str): The error message
        """
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.message)


def flatten_dictionary(dictionary):
    """ Method to 'flatten' the dictionary to one-level-deep dictionary, adding '.' as necessary.
    For example, it will convert the dictionary

      {
          "a": "val1",
          "b": {
              "c": "val2",
              "d": "val3",
              "e": {
                  "f": "val4"
              }
          }
      }

    to

      {
          "a": "val1",
          "b.c": "val2",
          "b.d": "val3",
          "b.e.f": "val4"
      }

    This method is needed for graph search by attribute, which only works on one-level-deep dictionaries.

    Args:
        dictionary (dict): The dictionary to flatten

    Returns:
        dict: The flattened version of the dictionary
    """
    def __helper(subdictionary, subdict_name):
        hret = {}

        for i in subdictionary:
            if subdict_name is None:
                name = i
            else:
                name = "%s.%s" % (subdict_name, i)

            if isinstance(subdictionary[i], dict):
                hret.update(__helper(subdictionary[i], name))
            else:
                hret.update({name: subdictionary[i]})

        return hret

    return __helper(dictionary, None)


def unflatten_dictionary(flat_dictionary):
    """ Unflatten the dictionary. This reverses the result of flatten_dictionary()

    Args:
        flat_dictionary (dict): The flat dictionary previously generated by flatten_dictionary()

    Returns:
        dict: The unflattened dictionary
    """
    ret = {}

    for i in flat_dictionary:
        path = i.split(".")

        p_dict = ret

        for l in path[:-1]:
            try:
                p_dict[l]
            except KeyError:
                p_dict[l] = {}

            p_dict = p_dict[l]

        p_dict[path[-1]] = flat_dictionary[i]

    return ret


def sort_edge_set(edge_set):
    """ Returns a set with edge tuples in the set sorted alphabetically. Fixes issues with edge node specification, for
    example ("node1", "node2", 0) is the same edge as ("node2", "node1", 0), but are not treated as such because they
    are tuples.

    Args:
        edge_set (set): set in the format set([(n1, n2, i), ...])

    Returns:
        set: edge_set with edge tuples sorted alphabetically
    """
    ret = set()
    for i in edge_set:
        e1, e2 = tuple(sorted(i[0:2]))
        e3 = i[2]
        ret.add((e1, e2, e3))

    return ret


def _unpack_name(tree_node_name):
        ret = tree_node_name.split(":")[2]

        if ret.startswith("GRP="):
            ret = tuple(ret[4:].split(","))

        return ret


def maximum_multinodes(paths):
    def mnode_counter(path):
        ret = 0

        for node in path:
            n = _unpack_name(node)

            if isinstance(n, tuple) or isinstance(n, list):
                ret += len(n)

        return ret

    max_path = paths[0]
    mnode_count = mnode_counter(max_path)

    for p in paths[1:]:
        size = mnode_counter(p)

        if size > mnode_count:
            max_path = p
            mnode_count = size

    return max_path


def get_node_chain(topology, *args, **kwargs):
    """ Generates a logical topology from the specified physical topology and a chain of NodeQuery's and LinkQuery's

    Args:
        topology: the physical topology to search
        args: An argument list of queries. Format: NodeQuery[, LinkQuery, NodeQuery[,LinkQuery, NodeQuery...]]

    Returns:
        a logical topology that matches the criteria specified by the queries

    Raises:
        QueryException: if the requested topology could not be generated
    """
    if 'path_select_method' in kwargs:
        path_select_method = kwargs['path_select_method']
    else:
        path_select_method = maximum_multinodes

    # Check that the number of arguments is correct
    try:
        assert(len(args) % 2 != 0)
    except AssertionError:
        raise QueryException("Incorrect number of arguments. Number of Queries must be odd. Format: "
                             "(NodeQuery, LinkQuery, NodeQuery[, LinkQuery, NodeQuery [, ...]]")

    # Check that the arguments are correct types
    assert(isinstance(topology, _Topology))

    links_and_nodes = zip(args[1::2], args[2::2])

    for pair in links_and_nodes:
        link = pair[0]
        node = pair[1]

        assert(isinstance(link, LinkQuery))
        assert(isinstance(node, NodeQuery))

    # Construct graph from topology
    topo_graph = networkx.MultiGraph()

    for i in topology['nodes']:
        if not topology.is_node_reserved(i):
            topo_graph.add_node(i, dict(topology['nodes'][i]))

    for i in topology['links']:
        n1 = i['link'].keys()[0]
        n2 = i['link'].keys()[1]
        attrs = flatten_dictionary(i)
        topo_graph.add_edge(n1, n2, attr_dict=attrs)

    # Define some helper methods
    def _get_level():
        try:
            _get_level.__level__
        except AttributeError:
            _get_level.__level__ = 0

        return _get_level.__level__

    def _increase_level():
        try:
            _get_level.__level__ += 1
        except AttributeError:
            _get_level.__level__ = 1

    def _pack_name(node_name, index, level=None):
        if isinstance(node_name, str) or isinstance(node_name, unicode):
            pass
        elif isinstance(node_name, tuple) or isinstance(node_name, list):
            node_name = "GRP=" + ",".join(node_name)

        if level is None:
            level = _get_level()

        return "%s:%s:%s" % (level, index, node_name)

    def _add_node(name, index, **kwargs):
        dict = {'__level': _get_level(), '__data': kwargs}

        if isinstance(name, str) or isinstance(name, unicode):
            dict.update(topo_graph.node[name])
        elif isinstance(name, tuple):
            for seg in name:
                dict[seg] = topo_graph.node[seg]

        tree.add_node(_pack_name(name, index), dict)

    def _get_level_candidates(level):
        prev_found = networkx.get_node_attributes(tree, '__level')
        return set(ifilter(lambda x: prev_found[x] == level, prev_found.keys()))

    def _get_prev_node_candidates():
        return _get_level_candidates(_get_level() - 1)

    def _get_level_of(node):
        """Returns the level of the FIRST time this node is mentioned
        """
        level = 0

        for i in args:
            level += 1
            if node is i:
                break

        return level

    # Done with helper methods. Lets get started!!!
    # Initialize the tree graph for searching
    tree = networkx.MultiDiGraph()

    # Create root node in the tree
    ROOT_NAME = _pack_name('__root_node', 0)
    tree.add_node(ROOT_NAME, {'__level': _get_level(), '__data': {}})

    criteria_cache = _CriteriaResultCache(topo_graph)
    # Fetch & Find the first node
    _increase_level()
    start_node = args[0]

    assert(isinstance(start_node, NodeQuery))
    matching_nodes = start_node.matches(criteria_cache)

    if len(matching_nodes) == 0:
        raise QueryException("Could not find nodes to satisfy the condition '%s'" % str(start_node))

    count = 0
    for i in matching_nodes:
        _add_node(i, count)
        tree.add_edge(ROOT_NAME, _pack_name(i, count))
        count += 1

    # Loop through links and chains
    for link, node in links_and_nodes:
        _increase_level()
        link_index = args.index(link)

        count = 0
        # query_result = node.matches(criteria_cache)

        # Iterate over nodes found in the search for previous chain candidates
        for i in _get_prev_node_candidates():
            # Get the path you need to take to this node
            exclude_set = set(map(lambda x: _unpack_name(x), set(networkx.shortest_path(tree, ROOT_NAME, i))))
            name = _unpack_name(i)
            # neighbors = topo_graph[name]
            neighbor_set = criteria_cache.get_neighbor_nodes(name)

            # neighbor_set = set(neighbors.keys())

            # Lets's check if this node object has already been specified - This is important for setting up loops
            prev_instance = _get_level_of(node)
            need_prev_link = False

            if prev_instance < _get_level():
                possible_instances = map(lambda x: _unpack_name(x), _get_level_candidates(prev_instance))
                new_candidates = set(possible_instances)
                need_prev_link = True
            else:
                # new_candidates = (neighbor_set & query_result) - exclude_set
                new_candidates = neighbor_set - exclude_set

            # Check links of the possible candidates to weed out the ones with bad links
            # neighbor_links = _sort_edge_set(set(topo_graph.edges([name], False, True)))

            # for c in (new_candidates & neighbor_set):
            for c in node.matches(criteria_cache, new_candidates):
                matching_links = link.matches(criteria_cache, _unpack_name(i), c)

                if len(matching_links) > 0:
                    # for match in matching_links:
                    #     # match_data = topo_graph.get_edge_data(*match)
                    #     match_data = {'edges': match}
                    #
                    #     if need_prev_link:
                    #         _add_node(c, count, link_level=prev_instance)
                    #     else:
                    #         _add_node(c, count)
                    #
                    #     tree.add_edge(i, _pack_name(c, count), attr_dict=match_data)

                    match_data = {'edges': matching_links}

                    if need_prev_link:
                        _add_node(c, count, link_level=prev_instance)
                    else:
                        _add_node(c, count)

                    tree.add_edge(i, _pack_name(c, count), attr_dict=match_data)

                    count += 1

        # Test if we found anything
        if count == 0:
            raise QueryException("Could not find link and node combination to satisfy the condition '%s' and '%s'" %
                                 (str(link), str(node)))

    # Time to wrap up. Add the "Finish" node
    _increase_level()
    FINISH_NAME = _pack_name('__finish_node', 0)

    for i in _get_prev_node_candidates():
        tree.add_node(FINISH_NAME, attr_dict={'__level': _get_level(), '__data': {}})
        tree.add_edge(i, FINISH_NAME)

    # Find all possible paths
    paths = networkx.all_simple_paths(tree, ROOT_NAME, FINISH_NAME)

    # Post-Processing
    # Apply node equivalence constraints

    all_paths = []
    good_paths = []

    for p in paths:
        path = p
        all_paths.append(map(lambda x: _unpack_name(x), p[1:-1]))
        good = True

        for i in path[1:-1]:
            # Check for linked (same) node equivalence:
            if 'link_level' in tree.node[i]['__data']:
                that_node = path[tree.node[i]['__data']['link_level']]

                if _unpack_name(i) != _unpack_name(that_node):
                    good = False

        if good:
            good_paths.append(path[1:-1])

    if len(good_paths) == 0:
        raise TopologyError("Could not find & reserve a logical topology with the specified criteria. Paths found and"
                            " rejected due to constraints: %s" % all_paths)

    final_path = []

    # for p in good_paths:
    #     final_path = p
    #     break

    final_path = path_select_method(good_paths)

    logical_topology = Param({"nodes":{}, "links":{}})
    index = 0

    # Final Steps - Find the corresponding node in topology, reserve node, and fill out logical topology
    for node_query in args[0::2]:
        found_node_name = _unpack_name(final_path[index])

        if node_query.get_node_name() not in logical_topology.nodes:
            # logical_topology.nodes[node_query.get_node_name()] = Param()
            # logical_topology.nodes[node_query.get_node_name()].node = Param(topology.nodes[found_node_name])

            if isinstance(found_node_name, str) or isinstance(found_node_name, unicode):
                logical_topology.nodes[node_query.get_node_name()] = Param(topology.nodes[found_node_name])
                topology.reserve_node(found_node_name)
            elif isinstance(found_node_name, tuple) or isinstance(found_node_name, list):
                logical_topology.nodes[node_query.get_node_name()] = Param()
                counter = 0

                for i in found_node_name:
                    logical_topology.nodes[node_query.get_node_name()][counter] = Param(topology.nodes[i])
                    topology.reserve_node(i)
                    counter += 1

        index += 1

    final_path_index = 0

    for link_query in args[1::2]:
        index = args.index(link_query)

        node1 = args[index - 1]
        node2 = args[index + 1]

        # n1_name = _unpack_name(final_path[final_path_index])
        # n2_name = _unpack_name(final_path[final_path_index + 1])
        n1_name = final_path[final_path_index]
        n2_name = final_path[final_path_index + 1]

        possible_edges = tree[n1_name][n2_name]
        chosen_edge_index = max(possible_edges, key=lambda x: len(possible_edges[x]['edges']))
        chosen_edge = possible_edges[chosen_edge_index]['edges']

        #link_dicts = link_query.get_edge_data(topo_graph, chosen_edge['edges'])
        link_dicts = []

        for group in chosen_edge:
            chosen_link = list(group)[0]
            link_dict = link_query.get_edge_data(topo_graph, chosen_link)
            link_dicts.append(link_dict)


        # if isinstance(link_dicts, dict):
        #     link_dict_list = [link_dicts]
        # else:
        #     link_dict_list = link_dicts

        for link_dict in link_dicts:
            unpacked_n1 = _unpack_name(n1_name)

            if isinstance(unpacked_n1, str) or isinstance(unpacked_n1, unicode):
                # l1 = link_dict['link'][_unpack_name(n1_name)]
                # del link_dict['link'][_unpack_name(n1_name)]

                if isinstance(link_dict, dict):
                    l1 = link_dict['link'][_unpack_name(n1_name)]
                    del link_dict['link'][_unpack_name(n1_name)]
                elif isinstance(link_dict, list):
                    l1 = []
                    for i in range(len(link_dict)):
                        l1.append(link_dict[i]['link'][_unpack_name(n1_name)])
                        del link_dict[i]['link'][_unpack_name(n1_name)]

            elif isinstance(unpacked_n1, tuple) or isinstance(unpacked_n1, list):
                l1 = []

                for i in unpacked_n1:
                    try:
                        l1.append(link_dict['link'][i])
                        del link_dict['link'][i]
                    except IndexError:
                        pass
                    except KeyError:
                        pass


            unpacked_n2 = _unpack_name(n2_name)

            if isinstance(unpacked_n2, str) or isinstance(unpacked_n2, unicode):
                # l2 = link_dict['link'][_unpack_name(n2_name)]
                # del link_dict['link'][_unpack_name(n2_name)]

                if isinstance(link_dict, dict):
                    l2 = link_dict['link'][_unpack_name(n2_name)]
                    del link_dict['link'][_unpack_name(n2_name)]
                elif isinstance(link_dict, list):
                    l2 = []
                    for i in range(len(link_dict)):
                        l2.append(link_dict[i]['link'][_unpack_name(n2_name)])
                        del link_dict[i]['link'][_unpack_name(n2_name)]

            elif isinstance(unpacked_n2, tuple) or isinstance(unpacked_n2, list):
                l2 = []

                for i in unpacked_n2:
                    try:
                        l2.append(link_dict['link'][i])
                        del link_dict['link'][i]
                    except:
                        pass

            # l2 = link_dict['link'][_unpack_name(n2_name)]
            # del link_dict['link'][_unpack_name(n2_name)]




            if isinstance(link_dict, dict):
                if isinstance(l1, list):
                    l1 = l1[0]

                if isinstance(l2, list):
                    l2 = l2[0]

                link_dict['link'][node1.get_node_name()] = l1
                link_dict['link'][node2.get_node_name()] = l2
            elif isinstance(link_dict, list):
                for i in range(len(link_dict)):
                    link_dict[i]['link'][node1.get_node_name()] = l1[i]
                    link_dict[i]['link'][node2.get_node_name()] = l2[i]

        multinode = True
        multilink = True

        if (isinstance(unpacked_n1, str) or isinstance(unpacked_n1, unicode)) and (isinstance(unpacked_n2, str) \
            or isinstance(unpacked_n2, unicode)):
                multinode = False

        if isinstance(link_query, MultiLinkQuery):
            multilink = True
        elif isinstance(link_query, LinkQuery):
            multilink = False

        if link_query.get_link_name() not in logical_topology.links:
            if isinstance(link_dicts, list):
                if multinode:
                    logical_topology.links[link_query.get_link_name()] = map(lambda x: Param(x), link_dicts)
                elif multilink:
                    logical_topology.links[link_query.get_link_name()] = map(lambda x: Param(x), link_dicts[0])
                else:
                    logical_topology.links[link_query.get_link_name()] = Param(link_dicts[0])
            else:
                logical_topology.links[link_query.get_link_name()] = Param(link_dicts)

        final_path_index += 1

    ret = logical_topology

    try:
        get_node_chain.__debug
    except AttributeError:
        get_node_chain.__debug = False
    finally:
        if get_node_chain.__debug:
            ret = (logical_topology, tree, final_path)

    return ret

if __name__ == "__main__":
    from cafe import get_topology
    import os
    os.environ['DISPLAY'] = ":0.0"
    import matplotlib.pyplot as plot
    from networkx import graphviz_layout

    get_topology().load("../../experiment_code/subgraphs/gfast.json")

    # tst = NodeQuery("mmm", tag="m1")
    # get_node_chain(get_topology(), tst)

    stc = NodeQuery("stc", type="stc")
    link1 = LinkQuery("stc_node1").add("attrs.speed", "10g")
    e5_1 = NodeQuery("node1", type="exa", subtype="e5-520")
    link2 = LinkQuery("node1_node2")
    dpu = NodeQuery("node2", type="exa", subtype="gfast")
    link3 = LinkQuery("node2_modems").add("attrs.speed", "1g")
    # modem = NodeQuery("modems", type="modem")
    modem = MultiNodeQuery("modems", None, type="modem")
    link4 = LinkQuery("modems_node3")
    e5_2 = NodeQuery("node3", type="exa", subtype="e5-520")
    link5 = LinkQuery("node3_stc")
    get_node_chain.__debug = True
    ret, res, path = get_node_chain(get_topology(), stc, link1, e5_1, link2, dpu, link3, modem, link4, e5_2, link5, stc)



    # get_topology().load("../../experiment_code/subgraphs/ring.json")
    # dut1 = NodeQuery("node1", type="exa", subtype="e5-520")
    # l1 = LinkQuery("l1")
    # dut2 = NodeQuery("node2", type="exa", subtype="e5-520")
    # l2 = LinkQuery("l2")
    # dut3 = NodeQuery("node3", type="exa", subtype="e5-520")
    # l3 = LinkQuery("l3")
    # dut4 = NodeQuery("node4", type="exa", subtype="e5-520")
    # l4 = LinkQuery("l4")
    # get_node_chain.__debug = True
    # ret, res, path = get_node_chain(get_topology(), dut1, l1, dut2, l2, dut3, l3, dut4, l4, dut1)



    # get_topology().load("../../experiment_code/subgraphs/multilink.json")
    # n1 = NodeQuery("node1", type="exa")
    # l = MultiLinkQuery("links", 2).add("attrs.type", "copper")
    # n2 = NodeQuery("node2", type="exa")
    # get_node_chain.__debug = True
    # ret, res, path = get_node_chain(get_topology(), n1, l, n2)



    # 'circo', 'dot'
    pos = graphviz_layout(res, prog='dot', args='')
    networkx.draw_networkx(res, pos, node_size=1200)
    networkx.draw_networkx_nodes(res, pos, nodelist=path, node_color='b', node_size=1200)

    plot.axis('off')
    #plot.savefig('my_graph.png')
    plot.show()

    ret.bp()

