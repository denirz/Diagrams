import pytest
import pydot


from .AS17_1prom import diag
@pytest.fixture
def diagram_true():
    return diag

def test_rea(capsys,diagram_true):
    with capsys.disabled():
        # print(diagram_true.dot)
        graphs = pydot.graph_from_dot_data(str(diagram_true.dot))
        print(graphs)
        g = graphs[0]
        print(type(g))
        for noder in g.get_node_list():
            print(noder.get_attributes())
            print(noder)
        for subgraphs in g.get_subgraph_list():
            print(subgraphs.get_attributes())



        # for i in g.get_subgraph_list():
        #     print(f"attrs_string = {i.get_name()}")
        #     print(i.get_node_list())
        #     for  j in i.get_subgraph_list():
        #         print(j.get_label())
        #         print(j.get_node_list())
        #         for k in j.get_node_list():
        #             print(k.get_label())
        # print(graphs[0])
        # print(graphs[0].get_nodes())
        # for i,node  in enumerate(graphs[0].get_node_list()):
        #     print(i)
        #     print(node.get_name())