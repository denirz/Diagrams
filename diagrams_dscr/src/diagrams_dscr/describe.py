import shlex
from string import Template
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from diagrams import Diagram
from enum import Enum
import re


class ItemType(Enum):
    Node = "Node"
    Edge = "Edge"
    Graph = "Graph"
    Other = "Other"


class DiagramDescription(object):
    """
    This class is used to describe the diagram
    """

    def __init__(self, diag: Diagram):
        if diag is None:
            return
        self.n_nodes = 0
        self.nodes = []
        self.n_edges = 0
        self.edges = []
        self.n_others = 0
        self.n_graphs = 0
        for i in enumerate(diag.dot.body):
            print(f"{self._detect_item(i[1])}  --> {i[0]}:{i[1]}")
            logger.warning(f"{self._detect_item(i[1])}  --> {i[0]}:{i[1]}")
            itemtype = self._detect_item(i[1])
            match itemtype:
                case ItemType.Node:
                    self.n_nodes += 1
                    self.nodes.append(self._parse_node(i[1]))
                case ItemType.Edge:
                    self.n_edges += 1
                    self.edges.append(self._parse_edge(i[1]))
                case ItemType.Other:
                    self.n_others += 1
                case ItemType.Graph:
                    self.n_graphs += 1

    def _detect_item(self, string: str) -> ItemType:
        graphpattern = re.compile("\s*graph\s*\[.*\]")
        g = graphpattern.match(string)
        if g:
            return ItemType.Graph
        nodepattern = re.compile('\s*"?\w*"?\s*\[.*\]', flags=re.DOTALL)
        g = nodepattern.match(string)
        if g:
            return ItemType.Node
        edgepattern = re.compile('\s*"?\w*"?\s*->\s*"?\w*"?\s*\[.*\]', flags=re.DOTALL)
        g = edgepattern.match(string)
        if g:
            return ItemType.Edge
        return ItemType.Other

    def _parse_node(self, stringnode: str) -> dict:
        # print(stringnode)
        s = shlex.split(stringnode)
        nodeattrs = {}
        nodeattrs["id"] = s[0]
        quotedstring = []
        # There should be more elegang way  to retrieve  these data
        print(s[1:])
        for item in s[1:]:
            item = item.replace("=", '="')
            item = item.replace("]", '"]')
            item = item + '"'
            quotedstring.append(item)
        attrstring = ",".join(quotedstring).strip('"').strip("[]")
        print(f"Attrstring: {attrstring}")
        d = eval(f"dict({attrstring.replace('\n','\\n')})")
        nodeattrs.update(d)
        return nodeattrs

    def _parse_edge(self, stringedge: str) -> dict:
        # print(stringedge)
        s = shlex.split(stringedge)
        assert s[1] == "->"
        edgeattrs = {}
        edgeattrs["source_id"] = s[0]
        edgeattrs["dest_id"] = s[2]
        quotedstring = []
        for item in s[3:]:
            item = item.replace("=", '="')
            item = item.replace("]", '"]')
            item = item + '"'
            quotedstring.append(item)
        attrstring = ",".join(quotedstring).strip('"').strip("[]")
        d = eval(f"dict({attrstring.replace('\n','\\n')})")
        edgeattrs.update(d)
        return edgeattrs

    def _enrich_edges_with_node_names(self, edge: dict) -> dict:
        """
        This method enriches the edge with the node names
        :param edge:
        :return: dict: enriched edge
        """
        enricheddata = {}
        for node in self.nodes:
            if node["id"] == edge["source_id"]:
                enricheddata["source_name"] = node["label"]
            if node["id"] == edge["dest_id"]:
                enricheddata["dest_name"] = node["label"]
        edge.update(enricheddata)
        return edge

    def enrichedges_with_node_names(self):
        """
        This method enriches all edges with the node names
        :return:
        """
        for edge in self.edges:
            self._enrich_edges_with_node_names(edge)

    def outputEdges(self):
        # Todo Use Pandas Here
        fields = ["source_name", "dest_name", "label", "description"]
        t = Template("$source_name|$dest_name|$label|$description")
        for edge in self.edges:
            print(t.safe_substitute(edge))
