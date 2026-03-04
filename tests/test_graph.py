import pytest
from app.graph.workflow import graph

def test_graph_compilation():
    assert graph is not None
    assert hasattr(graph, 'ainvoke')
