# diagrams_dscr

[![PyPI - Version](https://img.shields.io/pypi/v/diagrams-dscr.svg)](https://pypi.org/project/diagrams-dscr)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/diagrams-dscr.svg)](https://pypi.org/project/diagrams-dscr)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## General
`diagrams-dscr` is a small addition to  [Diagram Package](https://github.com/mingrammer/diagrams)

which allows to extract the nodes and edges from the diagram and output them to a CSV file.

## Installation

```console
pip install diagrams
pip install diagrams-dscr
```

## Usage

This module contains the DescribeDiagram class, which is used to describe a diagram by extracting its nodes and edges.
It uses the Use Case pattern to represent the diagram as a set of nodes and edges.

Usage pattern:
1. Create an instance of the DescribeDiagram class by passing a Diagram object to the constructor.
2. Optional: Call the `get_subgraphs` method to retrieve all subgraphs from the diagram and add them to the `nodes` and `edges` lists.
3. Optional: Call the `enrichedges_with_node_names` method to enrich all edges with the node names.
4. check `.nodes` and `.edges` for the nodes and edges respectively
5. Call the `outputEdges` method to output all edges with the node names to a CSV file.

Attributes:
    filename (str): The name of the file containing the diagram.
    dot (str): The dot representation of the diagram.
    nodes (list): A list of nodes in the diagram.
    edges (list): A list of edges in the diagram.

"""

```python
## Basic import 
from diagrams import Diagram
from diagrams_dscr import DescribeDiagram
# Create a Sample diagram:
from diagrams import Diagram, Cluster, Edge, Node
with Diagram("diagram_sample", show=False, filename="test_initialdiagram") as diag:
    with Cluster("A"):
        b = Node("b")
        c = Node("SOME tool")
        d = Node("Some ogging")
        f = Node("Some other tool")
        b >> c
        c >> f
        a = Node("a", color="red", description="some test decritpions ")
        a >> Edge(label="Connect tools to each othert", des="special tags") >> b

# Get list of atttributes of the Edges for  the diagram: 
listfields = DescribeDiagram(diag).outputEdges(listFields=True)
print(listfields)
#['dir', 'fontcolor', 'fontname', 'fontsize', 'source_id', 'dest_id', 'source_name', 'dest_name', 'label', 'des']
# Generate csv file with the edges of the diagram:
DescribeDiagram(diag).outputEdges(Fields=['source_name', 'dest_name', 'label', 'des'])
# produces a csv file with the following content    
# `source_name,dest_name,label,des` 

```

Be careful: to work with diagrams   package, you need to install the package  itself and graphwiz package . 

```console
## License

`diagrams-dscr` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
