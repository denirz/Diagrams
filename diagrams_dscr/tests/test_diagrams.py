import pytest
from diagrams import Cluster, Diagram, Edge, Node
from diagrams.aws.ml import MachineLearning
from diagrams.saas.logging import NewRelic


@pytest.fixture
def diagram_init():
    with Diagram("diagram_init", show=False, filename="testini_tialdiagram") as diag:
        with Cluster("A"):
            b = Node("b")
            c = MachineLearning("SOME Mltool")
            d = NewRelic("Some Logging")
            f = Node()
            b >> c
            c >> f
            a = Node("a", color="red", description="some test decritpions ")
            a >> Edge(label="some Lablel", des="sdfff") >> b
            (
                a
                >> Edge(label="Поток логов", description="some test EDGE decritpions ",headlabel="HEAD", color="red", style="dashed", fontcolor="red", fontname="Verdana")
                >> d
            )

        return diag


def test_diagrams(capsys, diagram_init):
    with capsys.disabled():
        print("Hello, diagrams!")
        print(diagram_init)
