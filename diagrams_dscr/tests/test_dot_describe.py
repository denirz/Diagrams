import pytest

from diagrams_dscr.dot_describe import DescribeDiagram


from .AS17_1prom import diag


@pytest.fixture
def diagram_true():
    return diag


from .test_diagrams import diagram_init


def test_describe_digaram(capsys, diagram_true):
    dd = DescribeDiagram(diagram_true)
    print(dd.filename)
    assert isinstance(dd, DescribeDiagram)
    dd.get_subgraphs()
    print(f"{len(dd.nodes)} Nodes detected")
    print(f"{len(dd.edges)} Edges detected")
    assert len(dd.nodes) > 0
    assert len(dd.edges) > 0
    # print(dd.nodes)
    # print(dd.edges)
    for n in dd.nodes:
        print(n["id"])
        if n["id"] in ("graph", "node", "edge"):
            print(n)
            continue


def test_describe_digaram_enrichedges(capsys, diagram_true):
    with capsys.disabled():
        dd = DescribeDiagram(diagram_true)
        assert isinstance(dd, DescribeDiagram)
        dd.get_subgraphs()
        print(f"{len(dd.nodes)} Nodes detected")
        print(f"{len(dd.edges)} Edges detected")
        dd.enrichedges_with_node_names()
        for edge in dd.edges:
            assert "source_name" in edge.keys()
            assert "dest_name" in edge.keys()
            print(edge)
            if edge["source_name"] in ("graph", "node", "edge"):
                print(edge)
                continue


def test_output_edges(capsys, diagram_true):
    with capsys.disabled():
        dd = DescribeDiagram(diagram_true)
        dd.outputEdges()


def test_outputEdges_fieldlist(capsys, diagram_true):
    with capsys.disabled():
        dd = DescribeDiagram(diagram_true)
        res = dd.outputEdges(listFields=True)
        print(res)
        assert isinstance(res, list)
        dd.outputEdges(
            Fields=["source_name", "dest_name", "headlabel", "label", "description"]
        )


def test_outputEdges_fieldlist(capsys, diagram_init):
    with capsys.disabled():
        dd = DescribeDiagram(diagram_init)
        res = dd.outputEdges(listFields=True)
        print(res)
        assert isinstance(res, list)
        dd.outputEdges(
            Fields=["source_name", "dest_name", "headlabel", "label", "description"]
        )
