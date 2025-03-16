"""
This module contains the DescribeDiagram class, which is used to describe a diagram by extracting its nodes and edges.
It uses the Use Case pattern to represent the diagram as a set of nodes and edges.

Usage pattern:
1. Create an instance of the DescribeDiagram class by passing a Diagram object to the constructor.
2. Optional: Call the `get_subgraphs` method to retrieve all subgraphs from the diagram and add them to the `nodes` and `edges` lists.
3. Optional: Call the `enrichedges_with_node_names` method to enrich all edges with the node names.
4. check .nodes and .edges for the nodes and edges respectively
5. Call the `outputEdges` method to output all edges with the node names to a CSV file.

Attributes:
    filename (str): The name of the file containing the diagram.
    dot (str): The dot representation of the diagram.
    nodes (list): A list of nodes in the diagram.
    edges (list): A list of edges in the diagram.

"""
import logging

import pandas as pd
import pydot
from diagrams import Diagram

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DescribeDiagram:
    """
    This class is used to describe a diagram by extracting its nodes and edges.
    It uses the Use Case pattern to represent the diagram as a set of nodes and edges.

    Usage pattern:
    1. Create an instance of the DescribeDiagram class by passing a Diagram object to the constructor.
    2. Optional: Call the `get_subgraphs` method to retrieve all subgraphs from the diagram and add them to the `nodes` and `edges` lists.
    3. Optional: Call the `enrichedges_with_node_names` method to enrich all edges with the node names.
    4. Call the `outputEdges` method to output all edges with the node names to a CSV file.

    Attributes:
        filename (str): The name of the file containing the diagram.
        dot (str): The dot representation of the diagram.
        nodes (list): A list of nodes in the diagram.
        edges (list): A list of edges in the diagram.
    """
    def __init__(self, diagram: Diagram):
        # print(diagram.dot)
        self.filename = diagram.filename
        self.dot = diagram.dot
        self.nodes = []
        self.edges = []
        self.get_subgraphs()
        self.enrichedges_with_node_names()

    def get_subgraphs(self, subgraph=None):
        """
        This method retrieves all subgraphs from the given diagram and adds them to the `nodes` and `edges` lists.
        If a subgraph is provided, it will be used instead of the main diagram.

        :param subgraph: A pydot subgraph object (default: None)
        """
        if subgraph is None:
            diagdata = pydot.graph_from_dot_data(str(self.dot))
            if len(diagdata) != 1:
                logger.error("More than one diagram detected")
                raise ValueError("More than one diagram detected")
            diagitem = diagdata[0]
        else:
            diagitem = subgraph

        logger.debug("diagram*****")
        logger.debug(diagitem.get_attributes())
        logger.debug("nodes*****")
        for node in diagitem.get_node_list():
            # print(f"Node: {node.get_attributes()}")
            logger.debug(f"Node:{node.get_name()}:{node.get_attributes()}")
            nodetoadd = node.get_attributes()
            nodetoadd.update({"id": node.get_name()})
            logger.debug(f"nodetoadd:{nodetoadd['id']}")
            self.nodes.append(nodetoadd)
        # print("subgraphs*****")
        for subgraphs in diagitem.get_subgraph_list():
            logger.debug(f"Subgraph: {subgraphs.get_attributes()}")
            self.get_subgraphs(subgraph=subgraphs)
        logger.debug("edges*****")
        for edges in diagitem.get_edge_list():
            logger.debug(f"Edge {edges.get_attributes()}")
            logger.debug(f"{edges.get_source()}->{edges.get_destination()}")
            edgetoadd = edges.get_attributes()
            edgetoadd.update(
                {"source_id": edges.get_source(), "dest_id": edges.get_destination()}
            )
            self.edges.append(edgetoadd)

    def enrichedges_with_node_names(self):
        """
        This method enriches all edges with the node names
        :return:
        """
        node_dict = {node["id"]: node.get("label", "-") for node in self.nodes}
        for edge in self.edges:
            edge["source_name"] = node_dict.get(edge["source_id"], "")
            edge["dest_name"] = node_dict.get(edge["dest_id"], "")

    def outputEdges(
        self, filename=None, listFields=False, Fields=None
    ):
        """
        This method outputs all edges with the node names to a CSV file.

        :param filename: The name of the CSV file to output the edges to (default: self.filename + "-edges.csv")
        :param listFields: A boolean indicating whether to return a list of column names instead of writing to a file (default: False)
        :param Fields: A list of column names to include in the output (default: None)

        :return: A list of column names if listFields is True, otherwise None
        """
        assert len(self.edges) > 0
        if filename is None:
            filename = self.filename + "-edges.csv"
        if listFields:
            df = pd.DataFrame(self.edges)
            return list(df.columns)

        df = pd.DataFrame(self.edges)
        if Fields is not None:
            df[Fields].to_csv(filename)
        else:
            df.to_csv(filename)
