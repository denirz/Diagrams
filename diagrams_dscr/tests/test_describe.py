import logging

import pytest
from diagrams_dscr.describe import DiagramDescription
from test_diagrams import  diagram_init

def test_diagram_description(capsys,diagram_init):
    with capsys.disabled():
        d = DiagramDescription(diagram_init)
        print(d.__dict__)

teststrings = (
    ('		bab0f2c4afa94f5cb26f92b0ccc93229 [label=a color=red decsription="some test decritpions "]',"Node"),
    ('bab0f2c4afa94f5cb26f92b0ccc93229 [label=a color=red decsription="some test decritpions "]',"Node"),
    ('		c1b5778ea5c04664a8f1f0dbd99d6f85 [label="SOME Mltool" height=1.9 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/aws/ml/machine-learning.png" shape=none]',
     "Node"),
    ('	ff2516462f824ca1a81ea188142e7014 -> c1b5778ea5c04664a8f1f0dbd99d6f85 [dir=forward fontcolor="#2D3436" fontname="Sans-Serif" fontsize=13]',"Edge"),
    ('		"707375bb5b3045088c2dba1abe7a342c" [label=b]',"Node"),
    ('		"4bc4ba3792d94c60a680a9b1fc76f398" [label="SOME Mltool" height=1.9 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/aws/ml/machine-learning.png" shape=none]\n',"Node"),
    ('		"4bc4ba3792d94c60a680a9b1fc76f398" [label="SOME Mltool" height=1.9 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/aws/ml/machine-learning.png" shape=none]\n',"Node"),
    ('		"7d36e765d36744d88462b9c5c09dd604" -> cac277eb79be4f6f8765d4dc0553e900 [dir=forward fontcolor="#2D3436" fontname="Sans-Serif" fontsize=13]',"Edge"),
    ('	subgraph cluster_A {',"Other"),
    ('graph [bgcolor="#E5F5FD" fontname="Sans-Serif" fontsize=12 label=A labeljust=l pencolor="#AEB6BE" rankdir=LR shape=box style=rounded]',"Graph"),
    ('''"6047fe0c7c1a4627aa02f476efef29fc" [label="testfaq.infra.sbt
 vsp-ac17.1-app 
 10.44.18.8" height=2.7 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/programming/language/python.png" ip="10.44.18.8" shape=none]''','Node'),
('''"6047fe0c7c1a4627aa02f476efef29fc" [label="testfaq.infra.sbt 
vsp-ac17.1-app 10.44.18.8" height=2.7 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/programming/language/python.png" ip="10.44.18.8" shape=none]''','Node')
               )
@pytest.mark.parametrize("string",teststrings)
def test_detect_item(capsys,diagram_init,string):
    with capsys.disabled():

        d = DiagramDescription(None)
        res = d._detect_item(string[0])
        assert res.name == string[1]
        print(res)



teststringnodes = (
    ('bab0f2c4afa94f5cb26f92b0ccc93229 [label=a color=red decsription="some test decritpions "]',''),
    ('"bab0f2c4afa94f5cb26f92b0ccc93229" [label=a color=red decsription="some test decritpions "]',''),
    ('		c1b5778ea5c04664a8f1f0dbd99d6f85 [label="SOME Mltool" height=1.9 image="/Users/denirz/Development/Diagrams/venv/lib/python3.12/site-packages/resources/aws/ml/machine-learning.png" shape=none]',''),
                   )

@pytest.mark.parametrize("stringnode",teststringnodes)
def test_parsenodes(capsys,diagram_init,stringnode):
    with capsys.disabled():
        d = DiagramDescription(None)
        nodeattr = d._parse_node(stringnode[0])
        print(nodeattr)
        assert isinstance(nodeattr,dict)

teststringedge = ((
    '	"7d36e765d36744d88462b9c5c09dd604" -> cac277eb79be4f6f8765d4dc0553e900 [dir=forward fontcolor="#2D3436" fontname="Sans-Serif" fontsize=13]',''
                  ),
                  ('	d2e6d61157f847af90cb143a64080ea1 -> bbc5659f881f4dfeb856fe42b9c9fb5c [label="Поток логов" dir=forward fontcolor="#2D3436" fontname="Sans-Serif" fontsize=13]',''),

                  )
@pytest.mark.parametrize("stringedge",teststringedge)
def test_parsenodes(capsys,diagram_init,stringedge):
    with capsys.disabled():
        d = DiagramDescription(None)
        nodeattr = d._parse_edge(stringedge[0])
        print(nodeattr)
        assert isinstance(nodeattr,dict)


def test__enrich_edges_with_node_names(capsys,caplog,diagram_init):
    with capsys.disabled():
        caplog.set_level(logging.INFO)
        d = DiagramDescription(diagram_init)
        for e in d.edges:
            # caplog(e)
            pass
        initialedge = d.edges[0]
        print(initialedge)
        ee = d._enrich_edges_with_node_names(initialedge)
        assert  isinstance(ee,dict)
        print(ee)
        for k in initialedge:
            assert  k in ee.keys()
            assert  initialedge[k]== ee[k]


def test_enrich_all_edges_with_node_names(capsys,caplog,diagram_init):
    with capsys.disabled():
        d = DiagramDescription(diagram_init)
        # print(d.edges)
        origlen = len(d.edges)
        print(f"{origlen} Edges detected")
        for e in d.edges:
            assert "dest_id" in e.keys()
            assert "dest_name" not in e.keys()
            assert  "source_id" in e.keys()
            assert "source_name" not in e.keys()
        d.enrichedges_with_node_names()
        print(d.edges)
        assert len(d.edges)==origlen
        for e in d.edges:
            assert "dest_id" in e.keys()
            assert "dest_name" in e.keys()
            assert "source_id" in e.keys()
            assert "source_name" in e.keys()

def test_outputedges(capsys,diagram_init):
    with capsys.disabled():
        d = DiagramDescription(diagram_init)
        d.enrichedges_with_node_names()
        d.outputEdges()


from AS17_1prom import diag
@pytest.fixture
def diagram_true():
    return diag
from unittest.mock import patch, call

def test_outputedges2(capsys,diagram_true):
    """
    test output Edge with actual diagram from the real life
    :param caplog
    :param capsys:
    :param diagram_true:
    :return:
    """
    with patch('diagrams_dscr.describe.logger') as mock_logger:
        with capsys.disabled():
            d = DiagramDescription(diagram_true)
            print(mock_logger.mock_calls)
            for n in d.nodes:
                print(f"node -{n['label']}\n===\n")
            print(f"number of nodes found: {d.n_nodes}")

            d.enrichedges_with_node_names()
            print(d.edges)
            print(d.nodes)
            d.outputEdges()


