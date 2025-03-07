import pytest
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.ml import MachineLearning
from diagrams.saas.logging import NewRelic


@pytest.fixture
def diagram_init():
    with Diagram("diagram_init", show=False) as diag:
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
                >> Edge(label="Поток логов", description="some test EDGE decritpions ")
                >> d
            )
        pass

        return diag


def test_diagrams(capsys, diagram_init):
    with capsys.disabled():
        print("Hello, diagrams!")
        print(diagram_init)
